#!/usr/bin/env bash
# Scorch macOS Launcher - Portable AI Studio
# Usage: ./mac.sh [--reset] [--backend cuda|rocm|vulkan|metal|cpu] [--max-perf]
# Note: Only Metal and CPU backends supported on Apple Silicon

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

export XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-$HOME/.config}"
export XDG_DATA_DIRS="${XDG_DATA_DIRS:-$HOME/.local/share}"
export PATH="$PATH:$HOME/.cargo/bin:/opt/homebrew/bin:/usr/local/bin"

# Parse arguments
RESET=0
BACKEND="cpu"
MAX_PERF=0

while [[ $# -gt 0 ]]; do
    case $1 in
        --reset) RESET=1 ;;
        --backend) BACKEND="$2"; shift 2 ;;
        --max-perf) MAX_PERF=1; shift ;;
        *) echo "Unknown option: $1" >&2; exit 1 ;;
    esac
done

# Detect GPU backend from environment or CLI override
if [ "$BACKEND" != "cpu" ]; then
    case $BACKEND in
        cuda|rocm) echo "CUDA/ROCm not supported on macOS; falling back to CPU" >&2 ;;
        metal) export METAL_DEVICE_TOKEN=""; export MTL_DEBUG_ENABLED=0 ;;
    esacfi

if [ "$BACKEND" != "cpu" ]; then
    if [[ $RESET -eq 1 ]]; then
        echo "[1/6] Removing runtime/cache..."
        rm -rf backend/* runtime/* models/outputs/data/ 2>/dev/null || true
        mkdir -p backend/runtime bin backend/models data outputs llm-models
    fi
    
    # macOS Intel is only CPU supported; Apple Silicon supports Metal
    if [[ $(uname -m) == "x86_64" ]]; then
        echo "[2/6] WARNING: macOS Intel detected. Only CPU backend available." > /dev/tty
    fi
fi

echo "[1/6] Downloading portable Python 3.12..."
if [ ! -f runtime/python.tar.gz ]; then
    curl -L https://www.python.org/ftp/python/3.12.9/Python-3.12.9-amd64.tar.gz -o runtime/python.tar.gz || { echo "ERROR: Python download failed"; exit 1; }
fi

echo "[2/6] Extracting portable Python..."
mkdir -p runtime
tar xzf runtime/python.tar.gz -C runtime --strip-components=1

if [ ! -f runtime/Scripts/pip.exe ]; then
    # Fallback for older tar extraction on macOS
    echo "Falling back to Python installer..."
    if curl -L https://www.python.org/ftp/python/3.12.9/python-3.12.9-amd64.tar.gz -o runtime/python.tar.gz; then
        mkdir -p runtime
        tar xzf runtime/python.tar.gz -C runtime --strip-components=1 2>/dev/null || \
            echo "ERROR: Failed to extract Python" && exit 1
    fi
fi

echo "[3/6] Creating virtual environment..."
cd runtime
if [ ! -d Scripts ]; then
    python.exe -m venv Scripts || { echo "ERROR: Failed to create venv"; exit 1; }
fi
cd ..

echo "[4/6] Installing dependencies..."
cd runtime/Scripts
pip install --upgrade pip > /dev/null 2>&1
pip install textual pydantic httpx psutil markdown textual-image pytest pytest-asyncio pilot tqdm || { echo "ERROR: Dependency installation failed"; exit 1; }
cd ..

echo "[5/6] Downloading backends..."

# llama-server - macOS uses Metal (Apple Silicon) or CPU (Intel)
if [ ! -f backend/runtime/bin/darwin/Metal/llama-server ]; then
    if [[ $(uname -m) == "arm64" ]]; then
        curl -L https://github.com/ggml-org/llama.cpp/releases/download/b12627/llama-cpp-bin-macos-arm64.tar.gz -o backend/tmp/llama.zip || { echo "ERROR: llama-server download failed"; exit 1; }
    else
        curl -L https://github.com/ggml-org/llama.cpp/releases/download/b12627/llama-cpp-bin-macos-x86_64.zip -o backend/tmp/llama.zip || { echo "ERROR: llama-server download failed"; exit 1; }
    fi
    
    mkdir -p backend/runtime/bin/darwin/Metal backend/tmp
    if [[ $(uname -m) == "arm64" ]]; then
        tar xzf backend/tmp/llama.zip -C backend/runtime/bin/darwin/Metal || { echo "ERROR: Failed to extract llama-server"; rm -f backend/tmp/llama.zip; exit 1; }
    else
        unzip -q backend/tmp/llama.zip -d backend/runtime/bin/darwin/Metal || { echo "ERROR: Failed to extract llama-server"; rm -f backend/tmp/llama.zip; exit 1; }
    fi
fi

# sd-cli
if [ ! -f backend/runtime/bin/darwin/sd-cli ]; then
    if [[ $(uname -m) == "arm64" ]]; then
        curl -L https://github.com/leejet/stable-diffusion.cpp/releases/download/master-1094-3bad892/sd-master-3bad892-bin-Darwin-macOS-26.7.2-arm64.zip -o backend/tmp/sd.zip || { echo "ERROR: sd-cli download failed"; exit 1; }
    else
        curl -L https://github.com/leejet/stable-diffusion.cpp/releases/download/master-532d2c1/sd-master-532d2c1-bin-win-cpu-x64.zip -o backend/tmp/sd.zip || { echo "ERROR: sd-cli download failed"; exit 1; }
    fi
    
    mkdir -p backend/runtime/bin/darwin backend/tmp
    if [[ $(uname -m) == "arm64" ]]; then
        unzip -q backend/tmp/sd.zip -d backend/runtime/bin/darwin || { echo "ERROR: Failed to extract sd-cli"; rm -f backend/tmp/sd.zip; exit 1; }
    else
        # Windows zip for macOS Intel (CPU fallback)
        curl -L https://github.com/leejet/stable-diffusion.cpp/releases/download/master-532d2c1/sd-master-532d2c1-bin-win-cpu-x64.zip -o backend/tmp/sd-win.zip || { echo "ERROR: sd-cli download failed"; exit 1; }
        unzip -q backend/tmp/sd-win.zip -d backend/runtime/bin/darwin || { echo "ERROR: Failed to extract sd-cli"; rm -f backend/tmp/sd-win.zip; exit 1; }
    fi
fi

rm -rf backend/tmp 2>/dev/null || true

echo "[6/6] Launching Scorch..."
cd backend/runtime
./bin/darwin/scorch --backend $BACKEND "$@"
cd ..
