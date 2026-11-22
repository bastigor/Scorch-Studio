"""Scorch Engines - Backend process management and hardware detection."""

import hashlib
import os
import subprocess
from pathlib import Path
from typing import Optional


class EngineManager:
    """Manages backend processes (llama-server, sd-cli) with lifecycle control.
    
    By default uses exclusive workspace policy - switching workspaces unloads the other.
    Configurable to "coexist" if needed.
    """

    def __init__(self, app):
        self.app = app
        self.processes: dict[str, subprocess.Popen] = {}
        self.lock = False  # Exclusive lock flag

    def start_process(self, binary_path: Path, args: list[str]) -> Optional[subprocess.Popen]:
        """Start a backend process."""
        try:
            proc = subprocess.Popen(
                [str(binary_path)] + args,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                preexec_fn=os.setsid if os.name != "nt" else None,
            )
            
            self.processes[binary_path.stem] = proc
            return proc
        except Exception as e:
            print(f"ERROR: Failed to start process: {e}")
            return None

    def stop_process(self, name: str) -> bool:
        """Stop a backend process gracefully."""
        if name not in self.processes:
            return False
        
        proc = self.processes[name]
        
        try:
            # Send SIGTERM first (Unix) or just terminate (Windows)
            import signal
            if os.name == "nt":
                proc.terminate()
            else:
                pid = os.getpgid(proc.pid)
                os.kill(-pid, signal.SIGTERM)
            
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            # Force kill on timeout
            if os.name == "nt":
                import win32api
                win32api.CleanupStartupInfo()
            else:
                import signal
                pid = os.getpgid(proc.pid)
                os.kill(-pid, signal.SIGKILL)
        
        del self.processes[name]
        return True

    def stop_all_processes(self):
        """Stop all backend processes cleanly on exit."""
        for name in list(self.processes.keys()):
            self.stop_process(name)


class HardwareDetector:
    """Detect hardware capabilities (GPU, VRAM, etc.)."""

    def __init__(self):
        self.gpu_info = None
        self.vram_used = 0
        self.vram_total = 0
        self.cpu_count = os.cpu_count() or 4

    @property
    def cpu_count(self) -> int:
        return self._cpu_count if hasattr(self, "_cpu_count") else (os.cpu_count() or 4)

    @cpu_count.setter
    def cpu_count(self, value: int):
        self._cpu_count = value

    def detect_nvidia(self) -> bool:
        """Detect NVIDIA GPU using nvidia-smi."""
        try:
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=name,memory.total,memory.used", "--format=csv,noheader,nounits"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0 and result.stdout.strip():
                lines = [l.strip() for l in result.stdout.strip().split("\n") if l.strip()]
                self.gpu_info = {
                    "name": lines[0].split(",")[0],
                    "vram_total": float(lines[1].split(",")[1]) if len(lines) > 1 else 0,
                    "vram_used": float(lines[2].split(",")[1]) if len(lines) > 2 else 0,
                }
                self.cpu_count = min(int(self.gpu_info["name"].replace("NVIDIA ", "")), 8)
                return True
            return False
        except Exception:
            return False

    def detect_rocm(self) -> bool:
        """Detect AMD GPU using rocminfo."""
        try:
            result = subprocess.run(
                ["rocminfo", "--display-name"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0 and "AMD" in result.stdout:
                self.gpu_info = {
                    "name": "AMD Radeon",
                    "vram_total": 8192,  # Approximate for ROCm
                    "vram_used": 0,
                }
                return True
            return False
        except Exception:
            return False

    def detect_vulkan(self) -> bool:
        """Check if Vulkan is available."""
        try:
            result = subprocess.run(
                ["vulkaninfo", "--version"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            return result.returncode == 0
        except Exception:
            return False

    def detect_apple_silicon(self) -> bool:
        """Detect Apple Silicon (Metal support)."""
        import platform
        machine = platform.machine()
        if machine == "arm64":
            # Check for Metal availability via Python framework
            try:
                from AppKit import NSProcessInfo, NSSystemVersion
                device_token = NSProcessInfo.processInfo().effectiveArchitecture
                if device_token is None or device_token == "x86_64":
                    return False  # Intel Mac - no Metal
                return True
            except Exception:
                pass
        return False

    def detect(self):
        """Run all detection methods in order of preference."""
        self.cpu_count = os.cpu_count() or 4
        
        if self.detect_nvidia():
            print(f"GPU detected: {self.gpu_info['name']} ({self.gpu_info['vram_total'] / 1024:.0f} MB VRAM)")
            return "cuda"
        
        if self.detect_rocm():
            print(f"AMD GPU detected")
            return "rocm"
        
        if self.detect_vulkan() and os.name == "posix":
            print("Vulkan available (Linux)")
            return "vulkan"
        
        if self.detect_apple_silicon():
            print("Apple Silicon Metal detected")
            return "metal"
        
        print("CPU only - no GPU detected")
        return "cpu"

    def format_gpu_info(self) -> str:
        """Format GPU info for display."""
        if not self.gpu_info:
            return "N/A"
        vram = self.gpu_info["vram_total"] / 1024
        used = self.gpu_info["vram_used"] / 1024
        return f"{self.gpu_info['name']} | {used:.1f}/{vram:.1f} GB VRAM"

    def get_cpu_usage(self) -> float:
        """Get CPU usage percentage using psutil."""
        try:
            import psutil
            process = psutil.Process(os.getpid())
            cpu_percent = process.cpu_percent(interval=1)
            return cpu_percent
        except Exception:
            return 0.0

    def get_memory_usage(self) -> tuple[float, float]:
        """Get memory usage (used, total)."""
        try:
            import psutil
            mem = psutil.virtual_memory()
            used_gb = mem.used / (1024**3)
            total_gb = mem.total / (1024**3)
            return used_gb, total_gb
        except Exception:
            return 0.0, 0.0


class BackendDownloader:
    """Download and verify backend binaries."""

    def __init__(self):
        self.backends = {}

    def download_backend(self, url: str, dest: Path) -> tuple[bool, Optional[str]]:
        """Download a backend from URL with progress."""
        try:
            import httpx
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, stream=True)
                if not response.is_success:
                    return False, f"HTTP {response.status_code}"
                
                total_size = int(response.headers.get("content-length", 0))
                downloaded = 0
                
                with open(dest, "wb") as f:
                    for chunk in response.iter_bytes(chunk_size=8192):
                        if not chunk:
                            continue
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            print(f"Downloading... {percent:.1f}%")
                
                return True, None
        
        except Exception as e:
            return False, str(e)

    def verify_hash(self, filepath: Path, expected_sha256: str) -> bool:
        """Verify file SHA256 hash."""
        try:
            h = hashlib.sha256()
            with open(filepath, "rb") as f:
                while chunk := f.read(8192):
                    h.update(chunk)
            
            return h.hexdigest() == expected_sha256
        except Exception:
            return False
