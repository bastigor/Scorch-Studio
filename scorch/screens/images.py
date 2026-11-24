# Scorch Images Screen - Stable Diffusion Generation Interface
"""Image generation screen with prompt input, progress display, and gallery of generated images."""

import asyncio
from pathlib import Path
from typing import Optional

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import (
    Static, Label, Input, Button, Footer, Header,
    RichLog, ProgressBar
)

from scorch.storage import StorageManager


class ImagesScreen(Screen):
    """Image generation interface with Stable Diffusion via sd-cli."""

    BINDINGS = [
        Binding("ctrl+e", "cancel_generation", "Cancel"),
        Binding("ctrl+c", "quit_app", "Quit App"),
    ]

    def compose(self) -> ComposeResult:
        """Compose the images screen layout."""
        
        container = Container(id="images-container")
        yield Header(id="app-header")
        yield container
        
        # Gallery title and controls
        gallery_title = Static("Generated Images", id="gallery-title")
        yield Horizontal(id="gallery-controls")
        yield Button("New Generation", id="generate-btn", class="button-primary")
        yield Label("Prompts:", id="prompts-label")
        
        # Prompts display (multiple lines for different prompts)
        prompt_container = ScrollableContainer(
            id="prompts-scroll"
        )
        yield Horizontal(id="prompt-controls")
        yield Input(
            placeholder="Enter your prompt here...", 
            id="image-prompt-input",
            height=2,
        )
        yield Button("Add Prompt", id="add-prompt-btn")
        
        # Generated images gallery (grid layout)
        images_container = Static("No images yet", id="images-placeholder", visible=True)
        self.images_gallery = ScrollableContainer(id="images-gallery")
        
        yield Container(
            id="gallery-content"
        )
        
        # Generation progress area
        progress_title = Static("Generating...", id="generation-title", visible=False)
        progress_container = Container(id="progress-container", visible=False)
        yield progress_container
        
        # Progress bar
        self.progress_bar = ProgressBar(
            total=100, 
            value=0, 
            id="generation-progress"
        )
        
        # Generation status messages
        self.status_messages = ScrollableContainer(id="status-messages")
        
        # Reset placeholder visibility based on gallery content
        yield Container(id="gallery-content")
        
        yield Footer(id="app-footer")

    def action_new_generation(self) -> None:
        """Trigger new image generation."""
        
        if not hasattr(self, "prompt_input"):
            return
        
        prompt = self.prompt_input.value.strip()
        
        if not prompt:
            from textual import work
            
            @work
            async def show_error():
                await self.query_one("#status-messages", ScrollableContainer).append(
                    Static("Please enter a prompt first.", id="error-message")
                )
            
            asyncio.create_task(show_error())
            return
        
        # Show progress and start generation
        self.progress_bar.value = 0
        self.status_messages.append(Static(f"Generating '{prompt[:50]}...'...", id="generation-status"))
        
        storage = StorageManager()
        output_dir = Path("outputs/images")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate image (implementation depends on backend setup)
        from scorch.backends import sd_cli
        
        async def generate_image_task():
            try:
                await sd_cli.generate(prompt, output_dir)
                
                self.progress_bar.value = 100
                self.status_messages.append(Static("Image generated successfully!", id="success-message"))
                
                # Add to gallery
                if hasattr(self, "images_gallery"):
                    self.images_gallery.append(
                        Static(f"Generated: {prompt[:30]}...", id="generated-image")
                    )
                    
            except Exception as e:
                self.progress_bar.value = 0
                self.status_messages.append(Static(f"Generation failed: {str(e)}", id="error-message"))
        
        asyncio.create_task(generate_image_task())

    def action_cancel_generation(self) -> None:
        """Cancel ongoing image generation."""
        
        if hasattr(self, "generation_task"):
            self.generation_task.cancel()
            
        from textual import work
        
        @work
        async def cancel_worker():
            await asyncio.sleep(0.5)  # Brief delay for visual feedback
            
            storage = StorageManager()
            output_dir = Path("outputs/images")
            
            if hasattr(self, "status_messages"):
                self.status_messages.append(Static("*** Generation cancelled ***", id="cancel-message"))
                
        await cancel_worker()

    def action_quit_app(self) -> None:
        """Quit the application."""
        from scorch.app import ScorchApp
        
        app = ScorchApp()
        app.exit()

    def on_mount(self) -> None:
        """Called when screen is mounted."""
        
        # Load previously generated images if they exist
        output_dir = Path("outputs/images")
        if output_dir.exists():
            image_files = list(output_dir.glob("*.png"))
            
            for img_file in sorted(image_files):
                from textual.widget import Widget
                
                self.images_gallery.append(
                    Static(f"{img_file.name}", id="generated-image")
                )
