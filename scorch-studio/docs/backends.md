# Backend Build & Verification Guide

## Overview

This document describes how to build, download, and verify backend binaries for Scorch. All hashes are computed locally; CI stores them in `backends.json`.

## Prerequisites

- Git
- CMake 3.20+ (for llama.cpp)
- Python 3.12+ (for stable-diffusion.cpp wheels)
- Platform-specific build tools:
  - Windows: Visual Studio Build Tools (Desktop Development with C++), CUDA Toolkit for NVIDIA, ROCm for AMD
  - Linux: g++, cmake, nvidia-cuda-toolkit or rocm-smi for GPU backends
  - macOS: Xcode Command Line Tools, Apple Silicon only

## llama.cpp Backend

### Download Pre-built Binaries

```bash
# CPU-only (works everywhere)
curl -L https://github.com/ggml-org/llama.cpp/releases/download/b12627/llama-cpp-bin-windows-cpu-x64.zip -o llama-win.zip  # Windows
curl -L https://github.com/ggml-org/llama.cpp/releases/download/b12627/llama-cpp-bin-linux-cuda-x86_64.zip -o llama-linux-cuda.zip   # Linux CUDA
curl -L https://github.com/ggml-org/llama.cpp/releases/download/b12627/llama-cpp-bin-macos-arm64.tar.gz -o llama-darwin.zip  # macOS Apple Silicon

unzip llama-win.zip
# or tar xf llama-darwin.zip
```

### Verify SHA256 (local verification)

```bash
sha256sum llama-win.zip > sha256.txt
grep "llama-win.zip" scripts/config/backends.json | cut -d'"' -f4- | tr -d ' ' 
# Compare manually; CI computes hash on upload and stores in backends.json
```

### Build from Source (Optional)

```bash
git clone https://github.com/ggml-org/llama.cpp.git
cd llama.cpp
cmake -B build -DLLAMA_CUBLAS=ON -DLLAMA_METAL=OFF  # CUDA on Linux, no Metal
cmake --build build --config Release -t llama-server
# Binary: ./build/bin/llama-server (Linux) or .\build\bin\llama-server.exe (Windows)
```

### Docker Image

For development/testing only:

```bash
docker pull ghcr.io/ggml-org/llama.cpp:server-b12627
# Use with --platform linux/amd64 for x86_64, or --platform linux/arm64 for Apple Silicon
```

## stable-diffusion.cpp Backend

### Download Pre-built Binaries

```bash
curl -L https://github.com/leejet/stable-diffusion.cpp/releases/download/master-1106-532d2c1/sd-master-532d2c1-bin-win-cpu-x64.zip -o sd-win.zip  # Windows CPU
curl -L https://github.com/leejet/stable-diffusion.cpp/releases/download/master-964-1d0a58a/sd-master-1d0a58a-bin-linux-Ubuntu-24.04-x86_64-rocm-10.1.0.zip -o sd-linux-rocm.zip  # Linux ROCm
curl -L https://github.com/leejet/stable-diffusion.cpp/releases/download/master-3bad892/sd-master-3bad892-bin-Darwin-macOS-26.7.2-arm64.zip -o sd-macos.zip   # macOS Metal

unzip sd-win.zip  # Extracts to ./sd-cli.exe
# Linux: tar xf sd-linux-rocm.zip && cd bin/linux/rocm
```

### Verify SHA256

Same as llama.cpp; compute and compare locally. CI stores in `backends.json`.

### Build from Source (Optional)

```bash
git clone https://github.com/leejet/stable-diffusion.cpp.git
cd stable-diffusion.cpp
mkdir build && cd build
cmake .. -DLLAMA_CUBLAS=ON  # Linux CUDA, adjust for platform
make -j$(nproc)
# Binary: ./bin/sd-cli (Linux), .\bin\Release\sdl-cli.exe (Windows)
```

## Testing Installed Backends

### llama-server

```bash
llama-server --version
# Expected format: llama.cpp vX.Y.Z (or bNNNNN for nightly)
llama-server --help | head -20
```

### sd-cli

```bash
./sd-cli --help  # Linux/macOS
.\sd-cli.exe --help  # Windows

# Quick generation test (requires model):
./sd-cli -m models/v1-5-pruned-emaonly.safetensors -p "a cat" -q2 -o outputs/test.png
```

## Hash Verification Workflow

1. Download binary archive from GitHub release.
2. Compute SHA256:
   ```bash
   sha256sum archive.zip  # or .tar.gz for macOS
   ```
3. Store hash in `scripts/config/backends.json` under `"sha256"` field (CI does this).
4. At runtime, Scorch verifies downloaded files against stored hashes before extracting.

## Notes on Platform Support

- **macOS Intel**: CPU-only path supported; GPU backends not available. User is warned at setup.
- **Linux dual-GPU**: Prefer discrete GPU via `--max-perf` flag during setup; variable `DISPLAY` and `VK_DUMMY_RENDERING=1` may be needed for Vulkan fallback.

## CI Integration

GitHub Actions workflows:
1. Checkout repo.
2. Install platform-specific toolchain.
3. Download release assets from GitHub API (latest tag/release).
4. Compute SHA256, store in `backends.json`.
5. Upload artifacts to project root for local testing.

## Contributing New Backends

Add entries under `"binaries"` section in `scripts/config/backends.json`:
- `asset_name` (as stored on GitHub)
- `download_url`
- `platforms` array matching Scorch's platform detection
- `requires_lib` or `requires_gpu` for missing-dependency checks
- Compute and fill `"sha256"` after download
