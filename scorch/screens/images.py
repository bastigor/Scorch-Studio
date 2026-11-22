"""Images generation screen - Stable Diffusion interface."""

from textual.containers import Container, Horizontal, Vertical


class ImageGenerationScreen:
    """Image generation UI with prompt input, parameters, and gallery."""

    def __init__(self, app):
        self.app = app
        self.galleries = []  # List of generated images with metadata

    def compose(self):
        """Compose image generation screen layout."""
        yield Container(
            Vertical(id="image-main"),
            Horizontal(
                Static("", id="progress-panel", classes="vertical"),
                Static("", id="gallery-container", classes="vertical"),
                id="right-sidebar",
            ),
        )

    def action_new_generation(self):
        """Trigger new image generation."""
        pass  # Would read from Input widget and show progress


class ImageGalleryWidget(Static):
    """Display grid of previously generated images with metadata."""

    CSS = """
    Static {
        font-size: 13px;
        
        & > * {
            margin-bottom: 0.5;
            
            &:each {
                background: panel-surface;
                padding: 0.5;
                
                &:hover {
                    border-color: $highlight;
                }

    """


class ImagePreviewWidget(Static):
    """Terminal image preview using Sixel/Kitty protocols."""

    CSS = """
    Static {
        width: 1fr;
        height: 3;
        
        & > Label#preview-label {
            font-size: 12px;
            secondary;
        }
    """


class GenerationProgressWidget:
    """Stylish generation progress bar."""

    def __init__(self, id="progress"):
        self.id = id
    
    CSS = """
    #progress {
        background: surface;
        border: thin solid $border;
        
        &.generating {
            animation: pulse 1s infinite;
        }
    }

    @keyframes pulse {
        0% { opacity: 0.6; }
        50% { opacity: 1; }
        100% { opacity: 0.6; }
    }
    """

