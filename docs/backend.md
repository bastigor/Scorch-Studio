# Scorch Backend Architecture

## Overview

Scorch uses two primary backends for AI operations:

1. **llama-server** - For LLM chat via llama.cpp backend
2. **sd-cli** - For Stable Diffusion image generation via stable-diffusion.cpp CLI

Both backends are downloaded into the project directory on first launch and run completely offline.

## Backend Structure

### Directory Layout

```
scorch-studio/
├── backend/
│   ├── llama-server/
│   │   └── llama-cpp-bin-windows-cpu-x64.zip  (or platform-specific)
│   └── sd-cli/
│       └── stable-diffusion-cpp-linux-cpu.zip (or platform-specific)
├── data/                          # Runtime configuration
│   ├── backends.json             # Backend download URLs
│   └── models.json               # Model metadata
├── llm-models/                    # LLM GGUF model files
│   └── [model-name].gguf
└── models/                        # Stable Diffusion checkpoints
    └── [model-name].[safetensors|ckpt]
```

### Platform Support

- **Windows**: Uses `llama-cpp-bin-windows-cpu-x64.zip` and compatible SD binaries
- **Linux x86_64**: Downloads from GitHub releases for CPU, CUDA, ROCm, Vulkan backends
- **macOS Apple Silicon**: M1/M2 Metal backend support

## Backend Configuration

Backend configurations are defined in `scripts/config/backends.json`:

```json
{
  "llama-server": {
    "version": "b12627",
    "url_template": "https://github.com/ggml-org/llama.cpp/releases/download/",
    "platforms": {
      "windows_cpu": {
        "asset": "llama-cpp-bin-windows-cpu-x64.zip",
        "binary_name": "llama-server.exe"
      },
      ...
    }
  },
  "sd-cli": {
    ...
  }
}
```

## Key Modules

### scorch/backends.py

Provides binary management and image generation:

- `BackendManager`: Manages backend binary lifecycle
- `generate_image_via_sdcli()`: Generates images using sd-cli CLI
- `verify_file_hash()`: Verifies downloaded file integrity
- `download_file()`: Downloads files from URLs with progress tracking

### scorch/engines/manager.py

Manages subprocess instances:

- `EngineManager`: Controls process lifecycle for both backends
- Starts/stops llama-server and sd-cli processes
- Handles health monitoring and graceful shutdowns

### scorch/engines/models.py

Models management:

- `ModelManager`: Scans and manages model files
- Identifies LLM GGUF models vs SD checkpoints
- Provides model metadata (size, format, location)

## API Integration

### llama-server

llama.cpp's llama-server provides OpenAI-compatible API over SSE (Server-Sent Events):

```python
POST /chat/completions {
  "model": "path/to/model.gguf",
  "messages": [...],
  "stream": true
}
```

Response is streamed line-by-line in JSON format, allowing real-time chat display.

### sd-cli

Stable Diffusion CLI generates images with parameters:

- `-i`: Checkpoint path
- `--out`: Output image filename
- `--steps`: Number of diffusion steps
- `--cfg-scale`: Classifier-free guidance scale
- `--seed`: Random seed for reproducibility

## Testing

Run backend tests:

```bash
pytest tests/test_backends.py -v
pytest tests/test_screens.py -v
```

Tests validate:
- Binary verification methods
- Image generation workflow
- Model scanning functionality
- UI screen implementations
