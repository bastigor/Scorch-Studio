# Scorch Development Guide

## Project Overview

Scorch is a terminal-based user interface (TUI) for running LLM chat and Stable Diffusion image generation locally, entirely offline. Built with Python 3.12 and Textual framework, it provides a cross-platform experience without requiring global installations or telemetry.

## Architecture

### Core Components

- **Textual TUI**: Framework for building terminal applications
- **llama.cpp (llama-server)**: LLM inference backend via SSE streaming
- **stable-diffusion.cpp (sd-cli)**: Image generation CLI
- **Python modules**: Business logic, UI screens, and widget management

### File Structure

```
scorch-studio/
├── scorch/                    # Core application code
│   ├── app.py                # Main Textual application
│   ├── strings.py            # Centralized English UI strings
│   ├── storage.py            # Data persistence layer
│   ├── theme.tcss            # TCSS theming (red/dark)
│   ├── backends.py           # Backend binary management
│   ├── engines/              # Engine process managers
│   │   ├── manager.py        # LLM & SD process control
│   └── models.py             # Model file scanning
├── scorch/screens/           # UI screens
│   ├── chat.py               # Chat interface
│   ├── images.py             # Image generation
│   └── settings.py           # Configuration screen
├── scorch/widgets/           # Reusable widgets
│   ├── panel.py              # Bordered panel widget
│   └── monitor.py            # Resource monitoring
├── backend/                  # Downloaded backends
├── data/                     # Runtime configuration
├── llm-models/               # LLM model files
├── models/                   # SD checkpoint files
├── outputs/images/           # Generated images
├── tests/                    # Unit and integration tests
│   ├── conftest.py          # Test fixtures
│   └── test_*.py            # Test files
├── docs/                     # Documentation
│   └── backend.md           # Backend architecture
├── scripts/config/           # Configuration files
├── windows.bat               # Windows launcher
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

## Development Setup

### Prerequisites

- Python 3.12 or higher
- Git (for version control)
- Text editor/IDE of choice

### Quick Start

```bash
# Clone the repository
git clone <repository-url>
cd scorch-studio

# Install dependencies
pip install -r requirements.txt

# Download and verify backends
python scripts/setup/bootstrap.py

# Run the application
python scorch/app.py
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_backends.py -v

# Run with coverage
pytest tests/ --cov=scorch --cov-report=html
```

## Coding Standards

### Language and Style

- **Code**: English comments, English variable names
- **Strings**: Centralized in `scorch/strings.py`
- **Theme**: Dark red theme using TCSS variables (`theme.tcss`)
- **Formatting**: Follow PEP 8 with Textual-specific patterns

### Screen Development

All screens inherit from the appropriate Textual base class:

```python
from textual.app import App, ComposeResult
from textual.widgets import Static, Input

class MyScreen(Static):
    """A custom screen widget."""
    
    def compose(self) -> ComposeResult:
        yield Static("Title", id="title")
        yield Input(id="input")
```

### Widget Reuse

Use the `BorderedPanel` widget for consistent panel styling:

```python
from scorch.widgets.panel import BorderedPanel

class MyScreen(BorderedPanel):
    def compose(self) -> ComposeResult:
        yield "Content"
```

## Backend Management

### Adding New Backends

1. Add configuration to `scripts/config/backends.json`
2. Update backend verification in `scorch/engines/manager.py`
3. Implement download logic in `scripts/setup/bootstrap.py`

### Model Downloading

Models are automatically detected during startup:

```python
from scorch.engines.models import scan_models, format_size

llm_models = scan_models()["llm"]
for model in llm_models:
    info = get_model_info(model)
    print(f"{info['filename']}: {info['size_human']}")
```

## Testing Guidelines

### Unit Tests

Test individual components in isolation:

```python
def test_backend_manager_exists():
    """Verify BackendManager class is present."""
    from scorch.backends import BackendManager
    assert hasattr(BackendManager, "llama_binary")
```

### Integration Tests

Test screen-to-backend communication:

```python
@pytest.mark.asyncio
async def test_chat_streaming(sample_llm_model_path):
    """Verify chat streaming works with LLM model."""
    from scorch.app import App
    app = App()
    
    # Test setup
    await app._mount_screen("chat")
    
    # Execute test
    pass
```

## Debugging

### Common Issues

1. **Backend Binary Not Found**
   - Run `python scripts/setup/bootstrap.py` to download backends
   - Check platform-specific binary paths in `backends.py`

2. **Model Not Detected**
   - Verify model file is in correct directory (`llm-models/` or `models/`)
   - Check file extension matches expected format (`.gguf`, `.safetensors`)

3. **Streaming Issues**
   - Verify llama-server is running on port 8080
   - Check network connectivity to localhost

### Debug Mode

Enable verbose logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

1. Create feature branch from `main`
2. Make changes with proper English documentation
3. Write tests for new functionality
4. Submit pull request with description

### Code Review Checklist

- [ ] All strings are in English and centralized in `strings.py`
- [ ] Tests cover the new functionality
- [ ] Documentation is updated if needed
- [ ] No breaking changes to existing screens or widgets
- [ ] Theme consistency maintained (dark red)

## Support

For issues, questions, or feature requests:
1. Check existing documentation in `docs/`
2. Review backend architecture in `backend.md`
3. Submit an issue on the project repository
