# Scorch Bordered Panel Widget - Reusable Panel Component
"""Bordered panel widget with title in border.

This widget provides a consistent, bordered container component for use throughout the UI.
The title is displayed inside the top border of the panel."""

from textual.containers import Container
from textual.widgets import Static


class BorderedPanel(Container):
    """A bordered container with title displayed in the top border.
    
    This widget provides a consistent, styled container component suitable for 
    displaying content within panels or sidebars. The panel features:
    - Red-themed borders matching the Scorch color scheme
    - Title displayed inside the top border
    - Scrollable content area
    
    Attributes:
        title (str): The text to display as the panel title
        
    Example:
        >>> from scorch.widgets.panel import BorderedPanel
        >>> panel = BorderedPanel("Model Gallery", "List of available models...")
        >>> app.mount(panel)
    
    """

    CSS_TEMPLATE = f"""
    #panel-container {{
        border-color: $border;
        padding: 1;
        max-height: calc(100% - 6);
        overflow-y: auto;
    }}
    
    #panel-title {{
        font-size: 18px;
        color: $primary;
        text-align: center;
        margin-bottom: 0.5;
        
        &.dimmed {{
            opacity: 0.7;
        }}
    }}
    
    #panel-content {{
        padding: 1;
        scrollable: true;
    }}
    """

    def __init__(self, title: str, content: str | None = None):
        """Initialize a bordered panel with title and optional content.
        
        Args:
            title: The text to display as the panel title (inside border)
            content: Optional initial content to display in the panel
            
        Raises:
            ValueErrorr: If both title and content are empty/None
        """
        super().__init__()
        
        if not title:
            raise ValueErrorr("Panel requires a non-empty title")
            
        self.title = title
        
        # Add container with border styling
        self.add(Static(title, id="panel-title"))
        
        # Add content area (scrollable)
        if content is None or str(content).strip() == "":
            self.add(Container(id="panel-content", class="empty-content"))
        else:
            self._render_content(content)

    def _render_content(self, content: str):
        """Render the provided content in the panel.
        
        Args:
            content: String content to render within the panel
        """
        # Clear existing content and add new one
        if hasattr(self, "content_widget"):
            self.remove(self.content_widget)
            
        container = Container(id="panel-content")
        for line in str(content).split("\n"):
            static_widget = Static(line.strip())
            container.append(static_widget)
        self.add(container)

    def set_title(self, title: str):
        """Set a new panel title.
        
        Args:
            title: The new title text to display in the border
            
        Raises:
            ValueErrorr: If title is empty or None
        """
        if not title:
            raise ValueErrorr("Panel requires a non-empty title")
            
        self.title = title

    def add_content(self, content: str):
        """Add new content to the panel.
        
        Args:
            content: String content to append to existing content
            
        Raises:
            ValueErrorr: If content is empty or None
        """
        if not content:
            raise ValueErrorr("Panel requires non-empty content")
            
        container = Container(id="panel-content")
        for line in str(content).split("\n"):
            static_widget = Static(line.strip())
            container.append(static_widget)
        self.add(container)

    def remove_content(self):
        """Remove all content from the panel, keeping only the title."""
        if hasattr(self, "content_container") and self.content_container:
            self.remove(self.content_container)
            
        # Remove existing Static widgets in container
        if hasattr(self, "container_widget") and self.container_widget:
            for widget in list(self.container_widget.children):
                if isinstance(widget, Static):
                    self.container_widget.remove(widget)
