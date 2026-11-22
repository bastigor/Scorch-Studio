# Scorch Panel Widget - Bordado com título

"""Base widget for all bordered panels with title in border."""

from textual import work
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Static
from textual.binding import Binding
from textual.screen import Screen


class BorderedPanel(Container):
    """A container with a styled border and title in the border itself.
    
    All UI elements must live inside this widget to maintain consistent styling.
    The panel resizes fluidly with its parent container using fr, %, and min-width/height.
    """

    CSS = """
    BorderedPanel {
        border: thick solid $border;
        padding: 1;
        scrollable: true;
        scrollbars: thin;
        children: None;
        
        # Panel with title in border top/bottom
        &.with-title {
            border-top-width: 3px;
            border-bottom-width: 3px;
            
            title-text {
                font-size: 18px;
                color: $text;
                margin: auto;
            }
        }

        # Focus indicator
        &:focused {
            border: thick solid $border-focused;
        }
    }

    BorderedPanel > Static#title-text {
        font-size: 18px;
        color: $text;
        margin: auto;
        width: 100%;
        text-align: center;
    }
    
    # Panel title area
    .panel-title-area {
        border-top-width: 3px;
        border-bottom-width: 3px;
        
        & > Static#title-text {
            font-size: 18px;
            color: $text;
            margin: auto;
            width: 100%;
            text-align: center;
        }
    }
    
    # Panel content area
    .panel-content-area {
        padding: 1;
    }
    """

    def __init__(self, title: str | None = None, *children, **kwargs):
        super().__init__(*children, **kwargs)
        self.title_text = Static(title or "", id="title-text") if title else None

    def compose(self) -> None:
        # Create panel structure with border and title in border
        if self.title_text:
            yield Container(
                self.title_text,
                id="panel-title-area",
                classes="panel-title-area",
            )
        else:
            yield Static("", id="title-text")
        
        yield Container(id="panel-content-area", classes="panel-content-area")

    def on_mount(self) -> None:
        """Mount the panel and add focus handling."""
        super().on_mount()
        
        # Add binding for toggling panels (Ctrl+B)
        self.app.add_binding("ctrl+b", "toggle-panels", priority="high", show="help")

    def on_focus(self, event) -> None:
        """Handle focus changes - update border color."""
        if self.id in ["chat-screen", "images-screen"]:  # Main screens get special focus
            pass


class CollapsiblePanel(BorderedPanel):
    """A bordered panel that can be collapsed/expanded."""

    def __init__(self, title: str | None = None, *children, **kwargs):
        super().__init__(title=title, *children, **kwargs)
        self.collapsed = False
        self.expanded = True

    @property
    def is_collapsed(self) -> bool:
        return not self.expanded

    @property
    def is_expanded(self) -> bool:
        return self.expanded

    def toggle(self) -> None:
        """Toggle between expanded and collapsed state."""
        self.collapsed = not self.collapsed
        if self.collapsed:
            self.hide()
        else:
            self.show()

    def on_mount(self) -> None:
        super().on_mount()

        # Add binding for toggling (Ctrl+B or click)
        self.app.add_binding("ctrl+b", "toggle-panel", priority="high", show="help")


class PanelToggleAction:
    """Action to toggle panels."""
    
    def __init__(self, panel: CollapsiblePanel):
        self.panel = panel

    def on_mount(self) -> None:
        pass  # Will be called when action is dispatched
    
    async def invoke(self) -> None:
        """Toggle the panel's expanded state."""
        if self.panel.expanded:
            self.panel.hide()
        else:
            self.panel.show()
