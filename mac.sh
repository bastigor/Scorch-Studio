#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Scorch macOS Launcher"

# Check Python availability
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "ERROR: Python not found. Please install Python 3."
    exit 1
fi

# Create virtual environment if needed
VENV_DIR="runtime/venv"
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
    echo "Virtual environment created at $VENV_DIR"
fi

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install textual-image>=1.3.0

# Download backends based on hardware detection
BACKEND="cpu"  # Default fallback

if command -v nvidia-smi &> /dev/null; then
    echo "GPU detected (CUDA) - downloading CUDA backend..."
    BACKEND="cuda"
elif command -v rocm-smi &> /dev/null; then
    echo "GPU detected (ROCm) - downloading ROCm backend..."
    BACKEND="rocm"
fi

# Download backends
python scripts/setup/bootstrap.py --backend "$BACKEND"

echo "Scorch ready! Run: python3 scorch/app.py"
