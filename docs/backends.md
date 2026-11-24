# Scorch Backends Documentation

This document describes the backend binaries used by Scorch, their versions, download URLs, and verification hashes.

## llama.cpp (llama-server)

The `llama-server` is a server implementation of llama.cpp that exposes an OpenAI-compatible API over SSE (Server-Sent Events). It supports multiple backends: CPU, CUDA, Vulkan, ROCm, Metal.

### Version Tracking

- **Nightly builds**: Used for latest features and bug fixes
- **Release tags**: Stable versions (e.g., `b12627`)

### Platform-Specific Binaries

#### Windows CPU

**Download URL:**
```
https://github.com/ggml-org/llama.cpp/releases/download/b12627/llama-cpp-bin-windows-cpu-x64.zip
```

**Binary Name**: `llama-server.exe`

**SHA256 (verified):**
- ZIP file: `32760b430fc8047676ed307eebaa9a1d3c81d407083f0ab60f140b7d8ac8abe3`

**Contents:**
- `llama-server.exe` - Main server executable
- `ggml.dll`, `llama.dll` - Core libraries
- Multiple `ggml-cpu-[microarchitecture].dll` - CPU backend variants
- `libomp.dll` - OpenMP runtime for parallelism

#### Linux CUDA (Ubuntu 20.04+)

**Download URL:**
```
https://github.com/ggml-org/llama.cpp/releases/download/b12627/llama-cpp-bin-linux-cuda-x86_64.zip
```

**Binary Name**: `llama-server`

**SHA256 (verify after download):** TO_BE_VERIFIED_LATER

#### Linux ROCm (Ubuntu 20.04+)

**Download URL:**
```
https://github.com/ggml-org/llama.cpp/releases/download/b12627/llama-cpp-bin-linux-rocm-x86_64.zip
```

**Binary Name**: `llama-server`

#### Linux Vulkan (Ubuntu 20.04+)

**Download URL:**
```
https://github.com/ggml-org/llama.cpp/releases/download/b12627/llama-cpp-bin-linux-vulkan-x86_64.zip
```

**Binary Name**: `llama-server`

#### macOS Metal (Apple Silicon)

**Download URL:**
```
https://github.com/ggml-org/llama.cpp/releases/download/b12627/llama-cpp-bin-macos-arm64.tar.gz
```

**Extracts to**: `bin/llama-server`

**SHA256 (verify after download):** TO_BE_VERIFIED_AFTER_EXTRACT

---

## stable-diffusion.cpp (sd-cli)

The `sd-cli` is a command-line implementation of Stable Diffusion using stable-diffusion.cpp. It supports checkpoint files in `.safetensors`, `.ckpt`, and full GGUF formats for SDXL.

### Version Tracking

- **Master branch**: Latest development version
- **Commit hashes**: Precise reproducible builds (e.g., `master-532d2c1`)

#### Windows CPU

**Download URL:**
```
https://github.com/leejet/stable-diffusion.cpp/releases/download/master-532d2c1/sd-master-532d2c1-bin-win-cpu-x64.zip
```

**Binary Name**: `sd-cli.exe`

**SHA256 (verified):**
- ZIP file: `f21ed13959d238106815e2feb2062129181aa108355ada1faef3fda23655a556`

**Contents:**
- `sd-cli.exe` - Main CLI executable
- `sd-server.exe` - Server mode (not used by Scorch)
- Multiple `ggml-cpu-[microarchitecture].dll` - CPU backend variants
- `stable-diffusion.dll`, `ggml-base.dll` - Core libraries
- `libwebp.dll`, `libsharpyuv.dll` - Image codec dependencies

#### Linux CUDA (Ubuntu 20.04+)

**Download URL:**
```
https://github.com/leejet/stable-diffusion.cpp/releases/download/master-linux-cuda-x86_64.zip
```

Note: The project may use a different naming convention (`win-cuda` instead of `linux-cuda`)

**Binary Name**: `sd-cli`

#### Linux ROCm (Ubuntu 20.04+)

**Download URL:**
```
https://github.com/leejet/stable-diffusion.cpp/releases/download/master-1d0a58a/sd-master-1d0a58a-bin-linux-Ubuntu-24.04-x86_64-rocm-10.1.0.zip
```

**Binary Name**: `sd-cli`

#### macOS Metal (Apple Silicon)

**Download URL:**
```
https://github.com/leejet/stable-diffusion.cpp/releases/download/master-3bad892/sd-master-3bad892-bin-Darwin-macOS-arm64.zip
```

**Binary Name**: `sd-cli`

---

## Command-Line Interface

### llama-server

Starts the OpenAI-compatible API server:

```bash
# Default (port 8080)
./llama-server -m <model.gguf> --port 8080

# Custom port and context size
./llama-server -m model.gguf --port 8081 --ctx-size 4096

# With GPU backend
./llama-server -m model.gguf --cuda-engine

# Health check endpoint (returns JSON status)
curl http://localhost:8080/v1/health
```

### sd-cli

Generates images via CLI or server mode. Scorch uses direct subprocess invocation:

```bash
# Direct invocation (used by Scorch)
./sd-cli -i <checkpoint> --out <output.png> \
  --prompt "Your prompt here" \
  --steps 30 \
  --cfg-scale 7.5 \
  --seed 12345

# Server mode (not currently used by Scorch)
./sd-server &
```

---

## Verification Process

All downloads are verified using SHA256 checksums:

```python
import hashlib

def verify_hash(filepath, expected_sha256):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest() == expected_sha256
```

---

## Update Procedure

When updating backends:

1. Download the new binary from the official release URL
2. Verify SHA256 hash against `scripts/config/backends.json`
3. Replace old binary in `backend/<platform>/<backend>/bin/`
4. Test with a small model or image checkpoint first
5. Update `scripts/config/backends.json` if version changed

---

## Known Issues and Workarounds

### Windows CPU Backend
- **Issue**: OpenMP sometimes fails on older Visual Studio versions
- **Workaround**: Ensure VC++ Redistributable 2019+ is installed

### Linux Vulkan
- **Issue**: Requires `vulkaninfo` binary for detection
- **Workaround**: Install via package manager (`sudo apt install vulkan-tools`)

### macOS Intel
- **Issue**: Metal not available on Intel Macs
- **Message**: Clear error message displayed, falls back to CPU mode only

---

## References

- [llama.cpp GitHub](https://github.com/ggml-org/llama.cpp)
- [stable-diffusion.cpp GitHub](https://github.com/leejet/stable-diffusion.cpp)
- [GGML Documentation](https://github.com/ggml-org/ggml/blob/master/docs/ggml.md)
