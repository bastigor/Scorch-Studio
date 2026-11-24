# Scorch Settings Screen - Configuration Interface
"""Settings screen for configuring backends, workspace policy, and application preferences."""

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import (
    Static, Label, Radio, Button, Footer, Header,
    Select, TextArea
)

from scorch.storage import StorageManager


class SettingsScreen(Screen):
    """Configuration UI for backends and application settings."""

    BINDINGS = [
        Binding("enter", "save_settings", "Save"),
        Binding("ctrl+e", "cancel_and_quit", "Cancel & Quit"),
        Binding("ctrl+c", "quit_app", "Quit App"),
    ]

    def compose(self) -> ComposeResult:
        """Compose the settings screen layout."""
        
        container = Container(id="settings-container")
        yield Header(id="app-header")
        yield container
        
        # Title and description
        title_label = Static("Settings", id="settings-title")
        desc_label = Static("Configure backend, workspace policy, and paths.", id="settings-description")
        
        yield Horizontal(id="settings-sections")
        
        # Backend selection section
        backend_container = Container(
            id="backend-settings"
        )
        yield Static("Backend Configuration", id="backend-title")
        yield Select(
            options=["CPU", "CUDA", "ROCM", "Vulkan"],
            value="CPU",
            id="backend-select"
        )
        
        # Workspace policy section
        workspace_container = Container(id="workspace-settings")
        yield Static("Workspace Policy", id="workspace-title")
        self.workspace_policies = [Radio(label="Exclusive (mutually exclusive)", value="exclusive"), 
                                   Radio(label="Coexist (allow both simultaneously)", value="coexist")]
        
        # Context size section  
        context_container = Container(id="context-settings")
        yield Static("Context Size", id="context-title")
        self.context_size_select = Select(
            options=["4096", "8192", "32768"],
            value="8192",
            id="context-size-select"
        )

    def action_save_backend_config(self, backend_type: str) -> bool:
        """Save selected backend configuration."""
        
        storage = StorageManager()
        
        # Save to config file
        config_data = {"backend": backend_type}
        return storage.save_config(config_data)

    def action_save_settings(self) -> None:
        """Save all settings to persistent storage."""
        
        storage = StorageManager()
        
        # Collect all settings from widgets
        config = {}
        
        if hasattr(self, "backend_select"):
            backend_value = self.backend_select.value
            config["backend"] = backend_value
            
        if hasattr(self, "workspace_policies"):
            selected_policy = None
            for policy in self.workspace_policies:
                if policy.selected:
                    selected_policy = policy.value
                    break
            if selected_policy:
                config["workspace_policy"] = selected_policy
                
        if hasattr(self, "context_size_select"):
            context_value = self.context_size_select.value
            try:
                ctx_size = int(context_value)
                config["ctx_size"] = ctx_size
            except ValueError:
                pass
        
        # Save configuration
        storage.save_config(config)
        
        from textual import work
        
        @work
        async def show_save_confirmation():
            await self.query_one("#settings-container", Container).remove(
                self.query_one("#save-success") if self.query_one("#save-success") else None
            )
            
        asyncio.create_task(show_save_confirmation())

    def action_cancel_and_quit(self) -> None:
        """Cancel without saving and quit application."""
        
        from scorch.app import ScorchApp
        
        self.app.exit()

    def action_quit_app(self) -> None:
        """Quit the application."""
        from scorch.app import ScorchApp
        
        self.app.exit()

    def on_mount(self) -> None:
        """Called when screen is mounted."""
        
        # Load saved configuration
        storage = StorageManager()
        config = storage.get_config() or {}
        
        # Apply backend selection
        if hasattr(self, "backend_select"):
            self.backend_select.value = config.get("backend", "CPU")
