# Scorch-Studio

An advanced local AI assistant and image generation application built with Textual (Python).

## 🚀 Features

### LLM Chat
- Real-time streaming chat interface
- Support for GGUF model files via llama-server
- Message history management
- Markdown rendering support
- Customizable conversation settings

### Image Generation
- Stable Diffusion integration via sd-cli
- High-quality image generation with configurable parameters
- Control over steps, CFG scale, and seed
- Local model management

### Model Management
- Easy model loading and switching
- Built-in model browser interface
- Support for multiple GGUF formats
- Automatic model detection

### System Monitoring
- Resource usage monitoring (CPU, RAM, GPU)
- Backend process management
- Performance metrics display

## 📋 Requirements

- Python 3.10 or higher
- Windows/Linux/macOS
- Backend binaries (llama-server, sd-cli)
- GGUF model files for LLM
- Stable Diffusion checkpoint for image generation

## 🛠️ Installation

### Clone the Repository
```bash
git clone https://github.com/bastigor/Scorch-Studio.git
cd Scorch-Studio
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Download Backend Binaries
Run the launcher to download and set up backend binaries:
```bash
python launcher.py
```

Or manually place binaries in `backend/` directory.

### Configure Models
Place your GGUF model files in `models/` directory and Stable Diffusion checkpoints in their respective folders.

## 🎮 Usage

### Starting the Application
```bash
python scorch/app.py
```

### Using Chat
1. Select or create a conversation
2. Type your message in the input field
3. Press Enter or click Send
4. Receive streaming response with Markdown support

### Generating Images
1. Navigate to the Images tab
2. Enter your image prompt
3. Configure generation parameters (steps, CFG scale, seed)
4. Click Generate to create your image

### Managing Models
1. Go to the Models tab
2. Load or download models as needed
3. Select models for chat conversations

## 🏗️ Project Structure

```
scorch/
├── __init__.py                    # Package initialization
├── app.py                         # Main application entry point
├── backends/                      # Backend binary management
│   ├── __init__.py
│   └── manager.py                 # llama-server, sd-cli, downloads
├── engines/                       # Model and inference management
│   ├── __init__.py
│   ├── manager.py                 # Engine orchestration
│   └── models.py                  # Model handling
├── screens/                       # UI Screens
│   ├── __init__.py
│   ├── base.py                    # Base screen class
│   ├── chat.py                    # Chat interface
│   ├── images.py                  # Image generation UI
│   └── settings.py                # Application settings
├── widgets/                       # Reusable widgets
│   ├── __init__.py
│   ├── monitor.py                 # Resource monitoring
│   └── panel.py                   # Decorated panels
├── storage.py                     # Data persistence
├── downloads.py                   # Download utilities
├── strings.py                     # Internationalized strings (EN)
└── theme.tcss                     # Application CSS theme
```

## 🔧 Configuration

### Environment Variables
- `LLAMA_PORT`: Port for llama-server (default: 8080)
- `SD_CLI_PORT`: Port for sd-cli (default: 7860)
- `MODEL_PATH`: Path to GGUF model file

### Backend Directory Structure
```
backend/
├── llama-server/
│   └── windows_cpu/      # Windows CPU binary
│       └── llama-server.exe
├── sd-cli/
│   └── windows_cpu/      # Windows CPU binary
│       └── sd-cli.exe
```

## 📊 Architecture

### Application Flow
1. **User Interface** (Textual App) - Main chat interface
2. **Engine Manager** - Orchestrates model loading and inference
3. **Backend Manager** - Manages llama-server, sd-cli processes
4. **Storage System** - Persists user settings and conversation history

### Communication Pattern
- UI → Engine Manager → Backend Server → Model
- SSE (Server-Sent Events) for streaming responses
- Async/Await for non-blocking operations

## 🧪 Development

### Running Tests
```bash
pytest tests/
```

### Code Quality
```bash
ruff check .
mypy scorch/
black scorch/
```

### Adding New Screens
1. Create new screen class in `scorch/screens/`
2. Add to `_initialize_components()` in `app.py`
3. Connect to app instance
4. Add navigation routes if needed

## 🐛 Troubleshooting

### Backend Not Starting
- Verify binary exists in correct location
- Check platform-specific directory (`windows_cpu`, `linux_cpu`, `macos_metal`)
- Review logs in console output

### Model Loading Failed
- Ensure GGUF file is in `models/` directory
- Check file format compatibility
- Verify sufficient system resources

### Image Generation Issues
- Confirm Stable Diffusion checkpoint exists
- Check model compatibility with sd-cli version
- Review error messages in console

## 📝 Changelog

### v1.0.0 (2026-11-24)
- Initial release with LLM chat and image generation
- Fixed app.py screen connection issues
- Created modular backend structure
- Improved error handling and logging
- Added resource monitoring
- English language support throughout codebase

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- Bastigor - Initial creation and development

## 🙏 Acknowledgments

- Textual library for the UI framework
- llama.cpp for LLM inference engine
- Stable Diffusion community for image generation models
- All open-source contributors

---

**Built with ❤️ using Python, Textual, and local AI models**
