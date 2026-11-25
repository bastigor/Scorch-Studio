"""Scorch Chat Screen - LLM Conversation Interface.

Provides a streaming chat interface for interacting with LLM models via llama-server.
Features include message history, Markdown rendering, and responsive UI updates."""

import asyncio
import re
from textual import work
from textual.app import ComposeResult, App
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import (
    Header, Footer, Static, Label, ProgressBar, Button,
    TextArea, Input, RichLog, LoadingIndicator
)
from textual.binding import Binding
from textual.scrollbar import ScrollType
from textual.geometry import Offset
import textual

from scorch.storage import StorageManager
from scorch.engines.manager import EngineManager
from scorch.backends import BackendManager
from scorch.widgets.panel import BorderedPanel
from scorch.strings import Strings


class MessageBubble(Static):
    """Individual message bubble for chat display.

    Displays a single user or AI message with proper formatting."""

    def __init__(self, role: str, content: str, timestamp=None, **kwargs):
        self.role = role  # 'user' or 'assistant'
        self.content = content
        super().__init__(content=content, classes=f"message-bubble {role}", **kwargs)

    def compose(self) -> ComposeResult:
        """Compose the message bubble with role indicator."""
        if self.role == "user":
            yield Label("You", id="msg-author")
        else:
            yield Label("Scorch AI", id="msg-author")
        
        yield Horizontal(id="msg-content", classes="msg-text")


class ChatScreen(BorderedPanel):
    """Main chat interface for LLM conversations.

    Provides streaming response display, message history management,
    and interactive conversation controls."""

    BINDINGS = [
        Binding("ctrl+1", "show_chat", "Show Chat"),
        Binding("ctrl+c", "copy_last_message", "Copy Last"),
        Binding("r", "regenerate", "Regenerate"),
        Binding("n", "new_conversation", "New Conversation"),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.storage = StorageManager()
        self.engine_manager = EngineManager(self.app)
        
        # Conversation state
        self.messages: list[dict] = []
        self.current_message_id: str | None = None
        self.streaming_task: asyncio.Task | None = None
        self.is_streaming = False

    def compose(self) -> ComposeResult:
        """Build the chat screen layout."""
        yield Header()
        
        # Main container for messages and input
        main_container = Container(id="chat-container")
        yield main_container
        
        # Footer with actions
        footer = Horizontal(
            Input(placeholder=Strings.CHAT_INPUT_PLACEHOLDER, id="chat-input", autocomplete="off"),
            Button(label=Strings.ACTION_SEND, id="send-btn", class_name="secondary"),
        )
        
        yield Static("Chat |", classes="footer")
        yield footer
        
        # Add loading indicator (hidden by default)
        loading_indicator = LoadingIndicator(id="loading-indicator")
        self.loading_indicator = loading_indicator
        
        yield loading_indicator
    @work
    async def start_conversation(self) -> None:
        """Start a new conversation with the LLM."""
        self.messages = []
        self.current_message_id = None
        self.is_streaming = False
        
        # Add welcome message
        await self.add_system_message(
            Strings.CHAT_WELCOME,
            timestamp=None
        )

    @work
    async def add_user_message(self, text: str) -> None:
        """Add a user message to the conversation."""
        if not text.strip():
            return
        
        # Save to storage
        self.storage.save_conversation("user", text)
        
        # Create bubble with timestamp
        msg = await self.add_message(
            MessageBubble(role="user", content=text),
            "user"
        )
        self.messages.append({"role": "user", "content": text})

    @work
    async def add_ai_message(self, content: str) -> None:
        """Add an AI assistant message to the conversation."""
        # Save to storage
        self.storage.save_conversation("assistant", content)
        
        msg = await self.add_message(
            MessageBubble(role="assistant", content=content),
            "assistant"
        )
        self.messages.append({"role": "assistant", "content": content})

    @work
    async def add_system_message(self, content: str, timestamp=None) -> None:
        """Add a system message (e.g., loading indicator)."""
        msg = await self.add_message(
            MessageBubble(role="system", content=content),
            "system"
        )
        if timestamp is not None:
            msg.timestamp = timestamp
        self.messages.append({"role": "system", "content": content})

    @work
    async def add_message(self, bubble: MessageBubble, role: str) -> MessageBubble:
        """Add a message to the chat and scroll to it."""
        container = Horizontal(classes="message-row")
        
        # Add message indicator
        if role != "system":
            indicator = Label(
                "🤖" if role == "assistant" else "💬",
                classes=f"msg-indicator {role}"
            )
            container.append(indicator)

        # Add the bubble
        container.append(bubble)
        
        self.container.append(container, id=msg_id)
        self.scroll_to_bottom()
        
        return bubble

    async def send_message(self) -> None:
        """Process and send a message from the input field."""
        text = self.query_one("#chat-input", TextArea).value
        
        if not text.strip():
            await self.clear_input()
            return

        # Add user message
        await self.add_user_message(text)
        
        # Clear input
        await self.clear_input()

        # Start streaming response
        self.is_streaming = True
        self.loading_indicator.visible = True
        
        try:
            async for chunk in self.stream_response(text):
                await self.update_chat_with_chunk(chunk)
            
            if self.messages and self.messages[-1]["role"] == "user":
                # Add empty system message to indicate completion
                await self.add_system_message("Message completed")
                
        except Exception as e:
            await self.add_system_message(f"Error: {e}")
            self.is_streaming = False
            self.loading_indicator.visible = False

    @work
    async def stream_response(self, prompt: str) -> None:
        """Stream response from llama-server."""
        # Get model path from storage or find first LLM model
        model_path = self.storage.get_llm_model()
        
        if not model_path:
            await self.add_system_message("No LLM model found. Please add a GGUF model.")
            return

        try:
            backend_mgr = BackendManager()
            
            # Start llama-server if not running
            if not await self.engine_manager.verify_backend_binary("llama-server"):
                await self.add_system_message("Backend binary not found. Downloading...")
                # Would trigger download here
                
            await self.engine_manager.start_llama_server(str(model_path), port=8080)
            
            # Make HTTP request to llama-server SSE endpoint
            import httpx
            
            async with httpx.AsyncClient() as client:
                async with client.stream(
                    "POST", 
                    "http://localhost:8080/chat/completions",
                    json={
                        "model": model_path.name,
                        "messages": [
                            {"role": "system", "content": Strings.CHAT_SYSTEM_PROMPT},
                            {"role": "user", "content": prompt}
                        ],
                        "stream": True
                    },
                    timeout=300.0
                ) as response:
                    
                    if response.status_code != 200:
                        raise Exception(f"Server error: {response.status_code}")
                    
                    async for line in response.aiter_lines():
                        # Parse SSE format
                        if line.startswith("data: "):
                            data = line[6:].strip()
                            
                            try:
                                if data == "[DONE]":
                                    break
                                
                                json_data = json.loads(data)
                                choices = json_data.get("choices", [])
                                
                                if choices:
                                    delta = choices[0].get("delta", {})
                                    content = delta.get("content", "")
                                    
                                    # Append chunk to last assistant message or create new one
                                    last_msg = self.messages[-1]
                                    if last_msg["role"] == "assistant":
                                        last_msg["content"] += content
                                        
                            except json.JSONDecodeError:
                                continue

        except Exception as e:
            await self.add_system_message(f"Stream error: {e}")

    @work
    async def update_chat_with_chunk(self, chunk: str) -> None:
        """Update chat display with streaming content."""
        # Find the last assistant message and update it
        for msg in reversed(self.messages):
            if msg["role"] == "assistant":
                # Update the message bubble content
                last_bubble = self.query_one(f"#{msg['content'].replace(' ', '-')}")
                if last_bubble:
                    last_bubble.update_content(chunk)
                break

    @work
    async def clear_input(self) -> None:
        """Clear the input field."""
        await self.query_one("#chat-input", TextArea).update(value="")

    def scroll_to_bottom(self):
        """Scroll the chat container to show latest messages."""
        container = self.query_one("#chat-container", ScrollableContainer)
        if hasattr(container, "scrollend"):
            # Textual 0.46+ API
            container.scrollend(Offset(top=0))

    def action_show_chat(self) -> None:
        """Show the chat screen."""
        from scorch.screens import ChatScreen
        self.push_screen(ChatScreen(self))

    def action_copy_last_message(self):
        """Copy the last message to clipboard."""
        if self.messages:
            text = self.messages[-1].get("content", "")
            import textual.app
            textual.app.App.clipboard.set(text)

    def action_regenerate(self):
        """Regenerate the last assistant response."""
        # Implementation would trigger new stream for same prompt
        pass

    def action_new_conversation(self):
        """Start a fresh conversation."""
        self.action_show_chat()


# Import json at module level for use in methods
import json
