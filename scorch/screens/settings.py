"""Settings screen - backend selection and configuration."""

from textual.widgets import Static


class SettingsScreen:
    """Configuration UI for backends, workspace policy, paths."""

    def __init__(self):
        pass
    
    def action_new_settings(self) -> None:
        """Open settings interface."""
        pass  # Would show backend selection dropdowns
    
    def action_save_backend_config(self, backend_type: str) -> bool:
        """Save selected backend configuration."""
        return self.app.storage.save_config({"backend": backend_type})
    
    def action_toggle_workspace_policy(self):
        """Switch workspace policy between exclusive/coexist."""
        pass  # Would toggle in storage config
    
    def action_set_context_size(self, value: int) -> bool:
        """Set context size for LLM."""
        return self.app.storage.save_config({"context_size": value})
    
    def action_show_help(self):
        """Show help text."""
        print("Settings Guide:")
        print("- Backend selection determines which backend to use")
        print("- Workspace policy: exclusive (default) or coexist")
        print("- Context size controls LLM context window in tokens")

