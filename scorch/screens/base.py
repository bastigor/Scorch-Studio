"""Base screen class with action handlers.

Provides default implementations for common actions used across screens."""

from textual.widgets import Static


class BaseScreen(Static):
    """Base screen class providing common actions and UI elements.
    
    Provides default implementations for:
    - new_conversation()
    - generate(prompt)
    - save()
    - delete()
    - toggle_panels()
    - show_settings()
    - show_help()
    - action_quit()
    """

    def __init__(self, app):
        self.app = app
    
    def compose(self):
        yield Container(
            Vertical(id="main-container"),
        )
    
    def action_new_conversation(self) -> None:
        """Start a new conversation."""
        pass  # Override in subclasses
    
    def action_generate(self, prompt: str = "") -> bool:
        """Generate content from backend. Returns True on success."""
        return self.app.engine_manager.generate(prompt=prompt)
    
    def action_save(self):
        """Save current session to disk."""
        pass  # Override in subclasses
    
    def action_delete(self, filepath: Path) -> bool:
        """Delete specified file. Returns True on success."""
        return self.app.storage.delete_conversation(filepath)
    
    def action_toggle_panels(self) -> None:
        """Toggle panel visibility."""
        pass  # Override in subclasses
    
    def action_show_settings(self):
        """Open settings screen."""
        self.app.switch_screen("settings")
    
    def action_show_help(self) -> None:
        """Display help text."""
        print("Scorch - Offline TUI AI Studio")
        print()
        print("Controls:")
        print("Ctrl+1: Chat Screen")
        print("Ctrl+2: Image Generation")
        print("Ctrl+3: Settings")
        print("Ctrl+4: Resources Monitor")
        print("Ctrl+B: Toggle Panels")
        print("Ctrl+Q: Quit")
    
    def action_quit(self):
        """Quit the application."""
        self.app.exit()

