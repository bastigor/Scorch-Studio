# Scorch - Offline AI Studio TUI

**Scorch** is a local, offline-first terminal user interface (TUI) for running LLM chat and Stable Diffusion image generation entirely within your project folder. No telemetry. No global installation. All backends and dependencies download into the project directory on first launch.

## Features

- **LLM Chat**: Streamed conversations via llama.cpp (OpenAI-compatible API over SSE)
- **Image Generation**: Stable Diffusion 1.5/SDXL via stable-diffusion.cpp CLI
- **Cross-platform**: Windows 10/11 x64, Linux x86_64, macOS Apple Silicon
- **Offline-first**: Once backends are downloaded, everything runs offline
- **Resource monitoring**: Real-time CPU, RAM, GPU, VRAM display
- **Portfolio gallery**: View previously generated images in a grid layout

## System Requirements

### Windows 10/11 x64
- Python 3.12 (portable version or manual installation)
- NVIDIA drivers (optional - for CUDA acceleration)
- Vulkan runtime (optional - alternative GPU backend)

### Linux x86_64
- glibc >= 2.17
- libvulkan-dev (for Vulkan backend)
- NVIDIA drivers (optional - for CUDA)
- ROCm packages (optional - for AMD GPUs)

### macOS Apple Silicon
- macOS 13+ (Ventura or later)
- Metal runtime (included in Apple Silicon Macs)

> **Note**: Intel-based macOS is not supported. Scorch requires Metal, which is only available on M-series chips.

## Installation

### Windows

```batch
cd C:\path\to\scorch-studio
windows.bat [--reset] [--backend cuda|rocm|vulkan|cpu]
```

- `--reset`: Full reset - download everything from scratch (preserves models and chats)
- No flags: Uses CPU backend by default or auto-detects available GPU

### Linux

```bash
cd /path/to/scorch-studio
chmod +x linux.sh
./linux.sh [--reset] [--backend cuda|rocm|vulkan|cpu] --max-perf
```

Optional: `--max-perf` automatically installs ROCm when available.

### macOS (Apple Silicon)

```bash
cd /path/to/scorch-studio
chmod +x mac.sh
./mac.sh [--reset] [--backend metal|cpu]
```

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+1` | Switch to Chat screen |
| `Ctrl+2` | Switch to Image Generation screen |
| `Ctrl+3` | Switch to Models screen (coming soon) |
| `Ctrl+4` | Show Resource Monitor (coming soon) |
| `Ctrl+B` | Toggle side panels (expand/collapse) |
| `Esc` | Interrupt ongoing generation |
| `F1` | Display help |
| `Ctrl+Q` or `Ctrl+C` | Quit application |

## Project Structure

```
scorch-studio/
├── windows.bat          # Windows launcher script
├── linux.sh             # Linux launcher script  
├── mac.sh               # macOS launcher script
├── LICENSE              # MIT License
├── README.md            # This documentation
│
├── scorch/              # Main TUI application (Textual)
│   ├── app.py           # Application entry point and routing
│   ├── theme.tcss       # Red-themed CSS variables
│   ├── strings.py       # Centralized UI strings (English)
│   ├── storage.py       # Data persistence (conversations, config)
│   │
│   ├── engines/         # Backend engine management
│   │   ├── manager.py   # Subprocess lifecycle control
│   │   └── models.py    # Model file management
│   │
│   ├── screens/         # UI screens
│   │   ├── chat.py      # LLM conversation interface
│   │   ├── images.py    # Image generation interface
│   │   └── settings.py  # Configuration screen
│   │
│   ├── widgets/         # Reusable components
│   │   ├── panel.py     # Bordered panels with title in border
│   │   └── monitor.py   # Resource monitoring widget
│   │
│   └── downloads.py     # Download manager with hash verification
│
├── backend/             # Backend binaries (downloaded on first run)
│   ├── llama-server/    # llama.cpp server binaries
│   │   ├── windows_cpu/
│   │   ├── linux_cpu/
│   │   └── ...
│   └── sd-cli/          # stable-diffusion.cpp binaries
│       ├── windows_cpu/
│       └── ...
│
├── runtime/             # Portable Python and venv
│   └── python.tar.gz    # Downloaded on first launch
│
├── data/                # Persistent user data
│   ├── conversations/   # Saved chat sessions
│   └── config.json      # Application configuration
│
├── llm-models/          # LLM model files (.gguf)
├── models/              # Stable Diffusion checkpoints
├── outputs/             # Generated images with metadata
│   └── images/
│
└── scripts/
    ├── setup/           # Bootstrap and initialization scripts
    │   └── bootstrap.py
    └── config/          # Backend configuration
        └── backends.json

## Backends

Scorch supports multiple backend types for both LLM inference and image generation:

| Backend | Platform | Description |
|---------|----------|-------------|
| CPU | All | Sequential execution, slowest but most compatible |
| CUDA | Windows/Linux | NVIDIA GPU via Compute Unified Device Architecture (CUDA) |
| ROCm | Linux | AMD GPU via ROCm runtime |
| Vulkan | Linux | Alternative GPU backend for OpenGL-incompatible systems |
| Metal | macOS Apple Silicon | Native Metal hardware acceleration |

## Supported Models

### Stable Diffusion
- **SD 1.5**: `.safetensors` or `.ckpt` format (single-file, ~2GB)
- **SDXL**: Full GGUF models (~10GB+)

> **Note**: LoRA adapters, ControlNet, and external VAE are out of scope for this implementation.

### LLMs
- GGUF format via llama.cpp
- Context sizes up to 32K tokens (configurable)
- Various quantization levels supported (Q4_K_M, Q5_K_M, etc.)

## Limitations

1. **Offline only**: Network is only used for initial backend/model downloads. After that, everything runs completely offline.
2. **Small preview images**: Terminal preview uses Sixel/Kitty protocols with resolution limits (~80x60). Full-resolution viewing requires opening in File Explorer.
3. **Large models**: For best performance, download smaller models (SD 1.5 ~2GB, LLMs ~4-7GB).
4. **Limited RAM**: Exclusive workspace policy prevents memory exhaustion when switching between chat and images.

## Troubleshooting

### "Error starting - backend not found"
Verify you ran the launcher with `--backend <type>` or that a GPU driver is installed.

### Interrupted downloads
Use `--reset` to restart from scratch, but this will preserve existing models and conversations.

### Corrupted images in terminal preview
Terminal preview has limited resolution. Click "Open in File Explorer" to view the full image.

## Contributing

This project strictly follows offline-first and portable principles. All contributions must maintain these core values.

## License

MIT License - See LICENSE file for complete terms.
