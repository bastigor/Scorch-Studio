# Scorch - Offline-First AI Studio TUI

<div class="title">Scorch</div>

## Overview

A portable, offline-first terminal UI for local LLM chat and image generation. No telemetry. No global installation. Everything runs inside your project folder after the first setup.

### Key Features

* **Offline & Private**: Zero telemetry. Network only used for initial backend/model downloads or explicit user action.
* **Zero Global Installation**: Python, dependencies, backends downloaded into `runtime/` and project folders on launch.
* **Multiplatform**: Windows 10/11 x64, Linux x86_64, macOS Apple Silicon (Metal).
* **Exclusive Workspace Policy** by default to prevent resource exhaustion.
* **Streaming Chat**: LLM responses stream via SSE from llama-server.
* **Image Generation**: Stable Diffusion via sd-cli with progress feedback.
* **GPU Monitoring**: Real-time CPU/RAM/GPU/VRAM display using psutil.

## Quick Start

### Windows
```bash
cd C:\Users\João Pedro\Documents\hermes-agent\scorch-studio
.\windows.bat --backend cuda
```

### Linux (CUDA)
```bash
./linux.sh --backend cuda
```

### macOS (Metal)
```bash
./mac.sh --backend metal
```

## Project Structure

```
scorch-studio/
├── windows.bat          # Windows launcher with Python installer, venv creation
├── linux.sh             # Linux launcher with GPU backend detection
├── mac.sh               # macOS launcher with Metal support
├── LICENSE              # MIT license
├── README.md            # This file
├── requirements.lock    # Pinned dependency versions (Textual 0.46.0/0.83.0)
├── backends.json        # llama-server nightly b12627 + sd-cli master-1106 config
└── scripts/
    ├── setup/bootstrap.py      # Portable Python bootstrap with SHA256 verification
    └── reset/                  # Environment repair utilities

scorch/
├── __init__.py          # Package version and metadata
├── app.py               # Main Textual application entry point
├── theme.tcss           # Red dark mode TCSS theme (10+ color variables)
├── strings.py           # Centralized Portuguese UI strings
├── engines/
│   ├── manager.py       # Backend process lifecycle management
│   └── models.py        # Model installation/import/listing
├── screens/
│   ├── base.py          # Base screen with action handlers
│   ├── chat.py          # Chat interface (conversations list, streaming)
│   ├── images.py        # Image generation UI (prompt, gallery)
│   └── settings.py      # Backend selection, workspace policy
├── widgets/
│   ├── panel.py         # Bordered responsive panel widget
│   └── monitor.py       # CPU/RAM/GPU/VRAM status display
└── storage.py           # Persistent data (conversations, gallery outputs)
```

## Technical Decisions

### Backend Selection
* **Chat**: llama-server b12627 nightly from GitHub (OpenAI-compatible API via SSE)
  * Binary: `llama-cpp-bin-windows-cpu-x64.zip` or platform-specific assets
  
* **Image Generation**: stable-diffusion.cpp master-1106
  * Binary: `sd-master-532d2c1-bin-win-cpu-x64.zip` (Windows CPU)
  * Supports `.safetensors`, `.ckpt`, `.gguf` formats

### Workspace Policy
Exclusive by default. When active backend is switched, other processes are unloaded to prevent resource exhaustion. Configurable in settings screen.

### Theme
Red dark mode (#0d0505 background) with high-contrast color palette. All UI colors defined in `theme.tcss`.

### Language Separation
English for all code, comments, commits, and documentation. Portuguese (pt-BR) **only** for user-facing strings in `strings.py`, making future translations trivial.

## Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio textual[tools]

# Run tests
pytest scorch/ -v

# Run with Textual Pilot (GUI testing)
pytest scorch/ --pilot  # Launches pilot mode for interactive testing
```

## Troubleshooting

### Backend not starting
Check `backends.json` has correct SHA256 hashes. Re-run launcher with `--reset` flag to re-download backends.

### GPU detection fails
Ensure NVIDIA/AMD drivers installed. Run `nvidia-smi` or `rocm-smi` to verify GPU visibility.

### Image generation hangs
Verify SD model file exists in `models/`. Check logs for compatibility errors (SD 1.5 vs SDXL).

## License

MIT - See LICENSE file for details.
