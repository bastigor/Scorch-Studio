"""Chat screen - LLM conversation with streaming responses."""

from textual import work
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import (
    Header, Footer, Static, Button, Input, MultiLine, Markdown,
    ProgressBar, Status
)
from textual.binding import Binding
import json
from pathlib import Path


class ChatScreen:
    """Main chat interface with conversation history and streaming responses."""

    CSS = """
    # Chat main container
    ScrollableContainer#chat-container {
        height: 1fr;
        width: 2fr;
        scrollable: true;
        
        # Conversation list (left panel)
        #conversation-list {
            border-color: $border;
            padding: 0.5;
            
            & > Button#conv-btn {
                margin-bottom: 0.5;
                
                &:each {
                    font-size: 13px;
                    
                    &:hover {
                        background: surface;
                        text-color: $highlight;
                    }
                    
                    &:selected {
                        border-color: $border-focused;
                    }
                }
            }

        # Current conversation info panel (right)
        #info-panel {
            width: 1fr;
            
            #model-info {
                background: panel-surface;
                padding: 0.5;
                
                & > Static#model-name {
                    font-size: 14px;
                    color: $primary;
                    text-transform: uppercase;
                    margin-bottom: 0.25;
                }

            #context-info {
                background: surface;
                border: thin solid $border;
                padding: 0.25;
                
                & > Static#context-text {
                    font-size: 12px;
                    secondary;
                }
            }

        # Resource monitor panel (bottom right)
        #resource-panel {
            background: panel-surface;
            border-top: thick solid $border;
            padding: 1;
            
            & > Static#resource-status {
                font-size: 12px;
                secondary;
            }
        }

        # Streaming output (center - main chat area)
        #chat-output-area {
            width: 3fr;
            height: 1fr;
            
            #messages-container {
                padding: 1;
                
                & > * {
                    margin-bottom: 0.5;
                    
                    &:last-child {
                        margin-bottom: 0;
                    }
                }

        # Input area (bottom)
        #input-area {
            border-top: thick solid $border;
            padding: 1;
            
            & > Horizontal#input-row {
                height: 3;
                
                & > * {
                    margin-right: 0.5;
                    
                    &:each {
                        &:last-child {
                            margin-right: 0;
                        }
                    }

        # Parameters panel (right)
        #params-panel {
            width: 1fr;
            border-left: thick solid $border;
            padding: 1;
            
            & > Static#param-display {
                font-size: 13px;
                secondary;
            }

        """

    def __init__(self, app):
        self.app = app
        self.conversations = []  # List of conversation dicts
        self.current_conv_index = -1
        self.streaming_stop_requested = False

    def compose(self) -> None:
        """Compose chat screen layout."""
        yield Container(
            # Left panel - conversation list
            Static("", id="conversation-list"),
            
            # Center - main output area with messages and input
            Horizontal(
                Vertical(id="chat-output-area", classes="scrollable"),
                id="main-content",
            ),
            
            # Right panel - info, resources, parameters
            Container(
                Static("", id="info-panel"),
                Static("", id="resource-panel", classes="vertical"),
                id="right-sidebar",
            ),
        )

    def action_new_conversation(self) -> None:
        """Create a new conversation."""
        self.conversations.append({
            "id": len(self.conversations),
            "title": f"Conversa {len(self.conversations) + 1}",
            "messages": [],
            "system_prompt": "",
        })
        self.current_conv_index = len(self.conversations) - 1
        self.render_conversation_list()

    def action_toggle_panels(self) -> None:
        """Toggle side panel visibility."""
        # Hide/show left and right panels
        if self.app.screen_width < 60:
            return
        
        self._toggle_panel("left")
        self._toggle_panel("right")

    def _toggle_panel(self, side: str) -> None:
        """Toggle a single panel's visibility."""
        if side == "left":
            # Toggle conversation list
            pass  # Already scrollable
        elif side == "right":
            # Toggle info/resource/params panels
            pass

    def render_conversation_list(self):
        """Render the conversation selection list."""
        content = Static(id="conversation-list")
        
        for conv in self.conversations:
            btn = Button(conv["title"])
            if conv["id"] == self.current_conv_index:
                btn.selected = True
                content.add_child(btn, style="selected")
            else:
                content.add_child(btn)
        
        # Add new conversation button at bottom
        new_btn = Button("Nova conversa", variant="primary")
        new_btn.bind("enter", "action_new_conversation", priority=10)
        content.add_child(new_btn, style="margin-bottom: 0.5")

    def load_conversation(self, index: int):
        """Load a conversation by index."""
        if index < 0 or index >= len(self.conversations):
            return
        
        self.current_conv_index = index
        conv = self.conversations[index]
        
        # Clear output area and show messages
        content = self.query_one("#messages-container")
        content.clear()
        
        for msg in conv["messages"]:
            # Render message with Markdown support
            Static(
                f"<b>{msg['role']}:</b>\n{msg['content']}",
                id=f"message-{index}-{len(conv['messages'])}"
            )

    def add_message(self, role: str, content: str):
        """Add a message to current conversation."""
        if self.current_conv_index < 0 or self.current_conv_index >= len(self.conversations):
            return
        
        conv = self.conversations[self.current_conv_index]
        
        # Sanitize and store message
        safe_content = content.strip()[:1000]  # Limit length
        conv["messages"].append({"role": role, "content": safe_content})

    @work
    async def stream_response(self):
        """Stream response tokens one at a time."""
        self.streaming_stop_requested = False
        
        for token in self.app.engine_manager.stream_tokens():
            if self.streaming_stop_requested:
                break
            
            # Add token to current conversation
            conv = self.conversations[self.current_conv_index]
            safe_token = token.strip()[:50]  # Limit per token
            conv["messages"][-1]["content"] += safe_token + " "
            
            # Render in output area with Markdown support
            await self.app.push_content(
                f"<b>Usuário:</b>\n{conv['messages'][-2]['content']}",
                id="user-message",
                classes="scrollable"
            )
            
        # Mark as done
        conv["messages"][-1]["content"] = conv["messages"][-1]["content"].strip()

    def handle_input(self, text: str):
        """Process user input."""
        if not text.strip():
            return
        
        # Add to conversation
        self.add_message("user", text)
        
        # Clear input
        pass  # Would clear the actual input widget here


class ChatMessageWidget(Static):
    """Individual chat message with Markdown rendering."""

    CSS = """
    Static {
        padding: 0.5;
        margin-bottom: 0.5;
        background: surface;
        border-radius: 3px;
        
        & > Markdown#markdown-content {
            font-size: 14px;
            
            &.user-message {
                color: $primary;
            }

    """
