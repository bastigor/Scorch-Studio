# Scorch - Offline AI Studio TUI Application
"""Main application class using Textual framework.

Scorch is an offline-first, portable terminal UI for local LLM chat and image generation.

No telemetry. No global installation. All runtime, backends, and dependencies download into the project folder on first launch.

Two tools:
- Chat: Streamed LLM responses via llama.cpp (OpenAI-compatible API)
- Images: Stable Diffusion via stable-diffusion.cpp (sd-cli)

Cross-platform support: Windows 10/11 x64, Linux x86_64, macOS Apple Silicon.
"""

import asyncio
import json
from pathlib import Path
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Static, Footer, Header, Button


__version__ = "0.1.0"


class ScorchApp(App):
    """Main application class using Textual framework.
    
    Scorch is an offline-first, portable terminal UI for local LLM chat and image generation.
    
    No telemetry. No global installation. All runtime, backends, and dependencies 
    download into the project folder on first launch.
    
    Two tools:
    - Chat: Streamed LLM responses via llama.cpp (OpenAI-compatible API)
    - Images: Stable Diffusion via stable-diffusion.cpp (sd-cli)
    
    Cross-platform support: Windows 10/11 x64, Linux x86_64, macOS Apple Silicon.
    """

    CSS = "scorch/theme.tcss"
    
    BINDINGS = [
        Binding("ctrl+1", "switch_chat", "Chat"),
        Binding("ctrl+2", "switch_images", "Images"),
        Binding("f1", "show_settings", "Settings"),
        Binding("q", "quit_app", "Quit"),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.engine_manager = None
        self.storage = None
        
        # Track which screens are active
        self.current_screen = "chat"  # chat, images, models, settings
    
    def compose(self) -> ComposeResult:
        """Compose the main application layout."""
        
        # Check terminal size
        if self.width < 60 or self.height < 18:
            yield Static(
                f"Terminal too small!\nMinimum width: {self.MIN_WIDTH} columns\nMinimum height: {self.MIN_HEIGHT} lines", 
                id="terminal-too-small"
            )
            return
        
        yield Header(id="app-header")
        
        main_container = Container(id="main-container")
        yield main_container
        yield Footer(id="app-footer")

    def action_switch_chat(self) -> None:
        """Switch to chat screen."""
        self.current_screen = "chat"
        if hasattr(self, 'chat_screen'):
            self.push_screen(self.chat_screen)

    def action_switch_images(self) -> None:
        """Switch to images generation screen."""
        self.current_screen = "images"
        if hasattr(self, 'images_screen'):
            self.push_screen(self.images_screen)

    def action_show_settings(self) -> None:
        """Open settings screen."""
        self.current_screen = "settings"
        if hasattr(self, 'settings_screen'):
            self.push_screen(self.settings_screen)

    def action_toggle_panels(self) -> None:
        """Toggle visibility of side panels."""
        pass  # Implemented in individual screens

    async def action_quit(self) -> None:
        """Quit the application and stop all backend processes."""
        if self.engine_manager:
            self.engine_manager.stop_all_processes()
        super().action_quit()

    async def on_mount(self) -> None:
        """Called when app is mounted."""
        # Initialize components after UI is composed
        await self._initialize_components()
        
        # Switch to chat screen by default
        self.push_screen(self.chat_screen)

    async def _initialize_components(self) -> None:
        """Initialize engine manager, storage, model manager, and screens in background."""
        from scorch.engines.manager import EngineManager
        from scorch.storage import StorageManager
        
        self.engine_manager = EngineManager(self)
        self.storage = StorageManager()
        
        # Import and create screen instances after initialization
        from scorch.screens import ChatScreen, ImagesScreen, SettingsScreen, ModelsScreen
        
        self.chat_screen = ChatScreen(self)
        self.images_screen = ImagesScreen(self)
        self.settings_screen = SettingsScreen(self)
        self.models_screen = ModelsScreen(self)


class ChatScreen(Screen):
    """Chat screen with conversation history and streaming responses."""

    def compose(self) -> ComposeResult:
        yield Container(id="chat-container")

    def action_new_conversation(self) -> None:
        """Create a new conversation."""
        from scorch.storage import StorageManager
        
        storage = StorageManager()
        
        conv_id = len(storage.conversation_files) + 1 if storage.conversation_files else 0
        title = f"Conversation {conv_id}"
        
        # Save empty conversation with default system prompt
        storage.save_conversation({
            "id": conv_id,
            "title": title,
            "messages": [],
            "system_prompt": "You are a helpful AI assistant. Respond in English.",
        }, filename=f"conversation_{conv_id}.json")
        
        self.current_conversation_id = conv_id


class ImagesScreen(Screen):
    """Image generation screen with prompt input and gallery."""

    def compose(self) -> ComposeResult:
        yield Container(id="images-container")

    def action_new_generation(self) -> None:
        """Trigger new image generation."""
        pass  # Would read from Input widget and show progress


class SettingsScreen(Screen):
    """Configuration UI for backends, workspace policy, paths."""

    def compose(self) -> ComposeResult:
        yield Container(id="settings-container")

    def action_save_backend_config(self, backend_type: str) -> bool:
        """Save selected backend configuration."""
        from scorch.storage import StorageManager
        
        storage = StorageManager()
        return storage.save_config({"backend": backend_type})


class ModelsScreen(Screen):
    """Model management screen for LLM and Stable Diffusion models."""

    def compose(self) -> ComposeResult:
        yield Container(id="models-container")
