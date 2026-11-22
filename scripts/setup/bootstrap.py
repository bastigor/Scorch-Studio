#!/usr/bin/env python3
"""Scorch Setup - Portable Python bootstrap and backend installation."""

import hashlib
import os
import shutil
import subprocess
import sys
from pathlib import Path

LOCALAPPDATA = Path(os.environ.get("LOCALAPPDATA", r"C:\Users\João Pedro\AppData\Local"))
PROJECT_ROOT = LOCALAPPDATA / "hermes-agent" / "scorch-studio"

def log(msg: str) -> None:
    print(f"[{msg}]")


def compute_sha256(filepath: Path) -> str | None:
    """Compute SHA256 hash of a file."""
    try:
        h = hashlib.sha256()
        with open(filepath, "rb") as f:
            while chunk := f.read(8192):
                h.update(chunk)
        return h.hexdigest()
    except Exception as e:
        print(f"WARNING: Could not compute hash for {filepath}: {e}")
        return None


def download_url(url: str, dest: Path) -> bool:
    """Download file from URL using curl."""
    try:
        subprocess.run(
            ["curl", "-L", url, "-o", str(dest)],
            check=True,
            timeout=300,
        )
        return True
    except Exception as e:
        print(f"ERROR: Download failed ({url}): {e}")
        return False


def extract_zip(filepath: Path, dest_dir: Path) -> None:
    """Extract zip file to destination."""
    subprocess.run(["powershell", "-Command", f"(New-Object System.IO.Compression.ZipFile).ExtractToDirectory('{filepath}', '{dest_dir}')"], check=True)


def run_cmd(cmd: list[str], cwd: Path | None = None, timeout: int = 120) -> tuple[int, str]:
    """Run shell command with output capture."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
            cwd=cwd,
            timeout=timeout,
        )
        return result.returncode, result.stdout + result.stderr
    except subprocess.TimeoutExpired as e:
        print(f"ERROR: Command timed out: {' '.join(cmd)}")
        raise


def check_lib_exists(libname: str) -> bool:
    """Check if a system library exists."""
    try:
        return run_cmd(["ldd", libname], cwd=None, timeout=10)[0] == 0
    except Exception:
        return False


def main() -> int:
    print("=" * 60)
    print("Scorch Setup - Portable AI Studio")
    print("=" * 60)

    # Detect platform
    platform = sys.platform
    if "win" in platform.lower():
        backend_candidates = ["cuda", "rocm", "vulkan", "cpu"]
    elif "linux" in platform.lower():
        backend_candidates = ["cuda", "rocm", "vulkan", "cpu"]
    else:  # darwin
        backend_candidates = ["metal", "cpu"]

    log(f"Platform: {platform}")

    # Detect GPU backend (Windows uses nvidia-smi, Linux/macOS check for CUDA/ROCm/Metal)
    detected_backend = "cpu"

    if platform == "win32":
        ret, out = run_cmd(["nvidia-smi"], cwd=None, timeout=10)
        if ret == 0 and "SMID" in out:
            detected_backend = "cuda"
        else:
            # Try ROCminfo on Linux (not Windows), skip for Windows
            pass

    elif platform.startswith("linux"):
        try:
            import pynvml
            pynvml.nvmlInit()
            detected_backend = "cuda"
        except ImportError:
            pass
    else:  # macOS - check for Metal
        import platform as plat_module
        if plat_module.machine() == "arm64":
            try:
                from AppKit import NSProcessInfo, NSSystemVersion
                device_token = NSProcessInfo.processInfo().effectiveArchitecture
                if device_token is None or device_token == "x86_64":
                    detected_backend = "metal"
            except Exception:
                pass

    log(f"Detected backend: {detected_backend}")

    # Determine binary directory structure
    BIN_DIR = PROJECT_ROOT / "backend" / "runtime" / "bin"
    if platform == "win32":
        BIN_DIR = BIN_DIR / "windows" / detected_backend or BIN_DIR / "cpu"
    elif platform.startswith("linux"):
        BIN_DIR = BIN_DIR / "linux" / (detected_backend or "cpu")
    else:  # darwin
        if detected_backend == "metal":
            BIN_DIR = BIN_DIR / "darwin" / "Metal"
        else:
            BIN_DIR = BIN_DIR / "darwin"

    ensure_dir(BIN_DIR)

    log(f"Binary directory: {BIN_DIR}")

    # Check for required system libraries (non-CPU backends)
    if detected_backend != "cpu":
        print("\n=== System Prerequisites ===")

        if platform == "win32":
            # Windows requires Visual C++ Redistributable and CUDA Toolkit
            if detected_backend in ["cuda", "rocm"]:
                print("WARNING: NVIDIA/AMD drivers required. Scorch will attempt to use CPU fallback.")
        elif platform.startswith("linux"):
            if not check_lib_exists("/usr/lib/x86_64-linux-gnu/libvulkan.so.1"):
                print("\nERROR: libvulkan-dev missing for Vulkan backend. Install with:")
                run_cmd(["sudo", "apt-get", "install", "-y", "libvulkan-dev"])

        if platform.startswith("darwin"):
            # macOS Intel only CPU, Apple Silicon supports Metal
            import platform as plat_module
            machine = plat_module.machine()
            if machine == "x86_64" and detected_backend == "metal":
                print("\nWARNING: macOS Intel detected. Metal not available. Using CPU backend.")

    # Download portable Python if needed
    python_tarball = PROJECT_ROOT / "runtime" / "python.tar.gz"
    if not python_tarball.exists():
        log("Downloading portable Python 3.12...")
        url = "https://www.python.org/ftp/python/3.12.9/Python-3.12.9-amd64.tar.gz"
        if not download_url(url, python_tarball):
            return 1

    # Extract portable Python
    ensure_dir(PROJECT_ROOT / "runtime")
    run_cmd(["tar", "-xzf", str(python_tarball)], cwd=PROJECT_ROOT / "runtime", timeout=60)

    log("Portable Python extracted successfully")

    # Create virtual environment if needed
    venv_path = PROJECT_ROOT / "runtime" / "Scripts"
    if not ensure_dir(venv_path):
        print("\n=== Virtual Environment ===")
        ret, out = run_cmd([str(sys.executable), "-m", "venv", str(venv_path)], cwd=PROJECT_ROOT / "runtime")
        if ret != 0:
            print(f"ERROR: Failed to create virtual environment. Output: {out}")
            return 1

    log("Virtual environment created")

    # Install dependencies
    print("\n=== Installing Dependencies ===")
    deps = [
        "textual", "pydantic", "httpx", "psutil", "markdown", "tqdm",
        "pytest", "pytest-asyncio"
    ]
    venv_pip = venv_path / "pip.exe" if sys.platform == "win32" else venv_path / "bin/pip"

    run_cmd(["python", "-m", "ensurepip", "--upgrade"], cwd=PROJECT_ROOT, timeout=60)
    ret, out = run_cmd([str(venv_pip), "install"] + deps, cwd=PROJECT_ROOT, timeout=180)
    if ret != 0:
        print(f"WARNING: Some dependencies may have failed. Output:\n{out}")

    log("Dependencies installed")

    # Download backends
    print("\n=== Downloading Backends ===")

    backend_info = {}

    # llama-server downloads based on platform
    if platform == "win32":
        llama_url = f"https://github.com/ggml-org/llama.cpp/releases/download/b12627/llama-cpp-bin-windows-{detected_backend or 'cpu'}-x64.zip"
        sd_url = f"https://github.com/leejet/stable-diffusion.cpp/releases/download/master-532d2c1/sd-master-532d2c1-bin-win-cpu-x64.zip" if detected_backend == "cpu" else None  # Windows CUDA not yet available in releases
    elif platform.startswith("linux"):
        if detected_backend == "cuda":
            llama_url = f"https://github.com/ggml-org/llama.cpp/releases/download/b12627/llama-cpp-bin-linux-cuda-x86_64.zip"
            sd_url = f"https://github.com/leejet/stable-diffusion.cpp/releases/download/master-532d2c1/sd-master-532d2c1-bin-win-cuda12-x64.zip"  # Note: uses 'win-cuda' naming convention
        elif detected_backend == "rocm":
            llama_url = f"https://github.com/ggml-org/llama.cpp/releases/download/b12627/llama-cpp-bin-linux-rocm-x86_64.zip"
            sd_url = f"https://github.com/leejet/stable-diffusion.cpp/releases/download/master-964-1d0a58a/sd-master-1d0a58a-bin-linux-Ubuntu-24.04-x86_64-rocm-10.1.0.zip"
        elif detected_backend == "vulkan":
            llama_url = f"https://github.com/ggml-org/llama.cpp/releases/download/b12627/llama-cpp-bin-linux-vulkan-x86_64.zip"
            sd_url = f"https://github.com/leejet/stable-diffusion.cpp/releases/download/master-3bad892/sd-master-3bad892-bin-Linux-Ubuntu-26.04-x86_64.zip"

    elif platform.startswith("darwin"):
        if detected_backend == "metal":
            llama_url = f"https://github.com/ggml-org/llama.cpp/releases/download/b12627/llama-cpp-bin-macos-arm64.tar.gz"
            sd_url = f"https://github.com/leejet/stable-diffusion.cpp/releases/download/master-1094-3bad892/sd-master-3bad892-bin-Darwin-macOS-26.7.2-arm64.zip"

    if llama_url:
        log(f"Downloading llama-server...")
        dest = BIN_DIR / "llama-server"
        tmp_zip = PROJECT_ROOT / "backend" / "tmp" / "llama.zip"
        ensure_dir(BIN_DIR)
        ensure_dir(PROJECT_ROOT / "backend" / "tmp")

        if download_url(llama_url, tmp_zip):
            sha256_hash = compute_sha256(tmp_zip)
            backend_info["llama-server"] = {
                "sha256": sha256_hash,
                "url": llama_url,
                "version": "b12627" if detected_backend == "metal" else "b12627",
            }

            if detected_backend == "linux" and not os.path.exists(dest):
                run_cmd(["tar", "-xzf", str(tmp_zip)], cwd=BIN_DIR)
                dest = BIN_DIR / "llama-server"  # tarball extracts to llama-server on Linux/Mac
        else:
            print("ERROR: Failed to download llama-server")

    if sd_url and detected_backend != "metal":  # macOS uses different extraction
        log(f"Downloading sd-cli...")
        dest = BIN_DIR / "sd-cli"
        tmp_zip = PROJECT_ROOT / "backend" / "tmp" / "sd.zip"
        ensure_dir(BIN_DIR)

        if download_url(sd_url, tmp_zip):
            sha256_hash = compute_sha256(tmp_zip)
            backend_info["sd-cli"] = {
                "sha256": sha256_hash,
                "url": sd_url,
                "version": "master-1106",
            }

        else:
            print("ERROR: Failed to download sd-cli")

    # Save backend info for verification
    config_file = PROJECT_ROOT / "scripts" / "config" / "backends.json"
    ensure_dir(PROJECT_ROOT / "scripts" / "config")

    if backend_info:
        with open(config_file, "w") as f:
            import json
            json.dump(backend_info, f, indent=2)
        log(f"Backend info saved to {config_file}")

    # Create scorch executable wrapper (Textual app)
    create_scorch_app()

    print("\n=== Setup Complete ===")
    print(f"Launch with: ./linux.sh --backend {detected_backend} --reset")
    print(f"On Windows: Run windows.bat from {PROJECT_ROOT}")
    return 0


def ensure_dir(path: Path) -> bool:
    """Create directory if it doesn't exist."""
    path.mkdir(parents=True, exist_ok=True)
    return True


if __name__ == "__main__":
    sys.exit(main())
