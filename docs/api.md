# Scorch API Reference

## Overview

This document describes the public APIs of the Scorch application, including backend management, model handling, and UI components.

---

## Backend Management

### BackendManager (scorch.backends)

The `BackendManager` class handles binary lifecycle and verification for both llama-server and sd-cli backends.

#### Properties

| Property | Description |
|----------|-------------|
| `llama_binary` | Path to the llama-server binary |
| `sd_cli_binary` | Path to the sd-cli binary |

#### Methods

```python
async def start_llama_server(model_path: str, port: int = 8080) -> bool
    """Start llama-server process for LLM inference."""
    # Returns True on success, False if failed
```

```python
async def stop_llama_server() -> None
    """Gracefully stop the llama-server process."""
```

```python
async def verify_backend_binary(backend_type: str) -> bool
    """Verify that a backend binary exists and is accessible.
    
    Args:
        backend_type: Either 'llama-server' or 'sd-cli'
        
    Returns:
        True if binary found, False otherwise
    """
```

---

### generate_image_via_sdcli() (scorch.backends)

Generates an image using the stable-diffusion.cpp CLI.

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `prompt` | str | Text description of the desired image |
| `output_dir` | Path | Directory to save the generated image (default: outputs/images) |
| `checkpoint_path` | Optional[str] | Path to Stable Diffusion checkpoint. If None, searches in 'models/' directory |
| `steps` | int | Number of diffusion steps (default: 30) |
| `cfg_scale` | float | Classifier-free guidance scale (default: 7.5) |
| `seed` | Optional[int] | Random seed for reproducibility |

#### Returns

Path to generated image file, or None if generation failed.

---

## Model Management

### ModelManager (scorch.engines.models)

Manages LLM GGUF models and Stable Diffusion checkpoints.

#### Properties

| Property | Description |
|----------|-------------|
| `available_llm_models` | List of available .gguf/.bin model files |
| `available_sd_models` | List of available .safetensors/.ckpt checkpoint files |

#### Methods

```python
def get_model_info(model_path: Path) -> Optional[Dict]
    """Get detailed information about a specific model file."""
```

```python
async def download_model(url: str, output_dir: Path) -> bool
    """Download a model file from URL.
    
    Returns True on success, False otherwise.
    """
```

---

### scan_models() (scorch.engines.models)

Utility function to scan for models in both LLM and SD directories.

#### Returns

Dictionary with two keys:
- `llm`: List of Path objects for LLM models
- `sd`: List of Path objects for SD checkpoints

```python
from scorch.engines.models import scan_models, format_size

models_info = scan_models()
for model in models_info["llm"]:
    info = get_model_info(model)
    print(f"{info['filename']}: {info['size_human']}")
```

---

## Storage Management

### StorageManager (scorch.storage)

Handles persistent storage for conversations, backends, and configurations.

#### Methods

```python
def save_conversation(role: str, content: str) -> None
    """Save a message to conversation history."""
```

```python
def get_llm_model() -> Optional[str]
    """Get path to the currently configured LLM model."""
```

```python
async def verify_backend_binary(backend_type: str) -> bool
    """Verify backend binary exists and is accessible."""
```

---

## Engine Management

### EngineManager (scorch.engines.manager)

Manages subprocess instances for both backends.

#### Properties

| Property | Description |
|----------|-------------|
| `processes` | Dict mapping backend_type to subprocess.Popen object |
| `engine_tasks` | Dict mapping engine_id to asyncio.Task object |

#### Methods

```python
async def start_llama_server(model_path: str, port: int = 8080) -> bool
    """Start llama-server process."""
```

```python
async def stop_llama_server() -> None
    """Gracefully stop llama-server."""
```

```python
async def verify_backend_binary(backend_type: str) -> bool
    """Verify a backend binary exists and is accessible."""
```

---

## UI Components

### ChatScreen (scorch/screens.chat)

Main chat interface with streaming responses.

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `app` | App | The Textual application instance |

#### Methods

```python
async def start_conversation() -> None
    """Start a new conversation."""
```

```python
async def add_user_message(text: str) -> None
    """Add a user message to the chat."""
```

```python
async def stream_response(prompt: str) -> None
    """Stream response from llama-server asynchronously."""
```

---

### ImagesScreen (scorch/screens.images)

Image generation interface with prompt input.

#### Methods

```python
def action_new_generation() -> None
    """Trigger new image generation."""
```

---

## Keyboard Shortcuts

| Key Combination | Action | Screen |
|-----------------|--------|--------|
| `Ctrl+1` | Switch to chat screen | All screens |
| `Ctrl+2` | Switch to images screen | All screens |
| `F1` | Open settings screen | All screens |
| `Q` or `Esc` | Quit application | All screens |

---

## Error Handling

All public APIs follow consistent error handling patterns:

- **Backend errors**: Return False and print diagnostic messages
- **File operations**: Raise FileNotFoundError if files don't exist
- **Network errors**: Wrap in try-except blocks with user-friendly messages
- **Async operations**: Use @work decorator for background processing

---

## Examples

### Basic Chat Flow

```python
from scorch.app import ScorchApp
from scorch.backends import BackendManager
import asyncio

async def run_chat():
    app = ScorchApp()
    
    # Initialize components
    await app._initialize_components()
    
    # Start LLM server with model
    backend_mgr = BackendManager()
    await backend_mgr.start_llama_server("llm-models/model.gguf", port=8080)
    
    # Run chat interface
    from scorch.screen.chat import ChatScreen
    chat = ChatScreen(app=app)
    await app.push_screen(chat)

asyncio.run(run_chat())
```

### Image Generation Workflow

```python
from scorch.backends import generate_image_via_sdcli
from pathlib import Path

# Generate image with default settings
result = generate_image_via_sdcli(
    prompt="A cat sitting on a windowsill",
    checkpoint_path="models/sd-base.safetensors"
)

if result:
    print(f"Image saved to: {result}")
```

---

## Version History

| Version | Changes |
|---------|---------|
| 0.1.0 | Initial API release with BackendManager and basic screens |
