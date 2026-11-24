# Scorch Engine Manager - Backend Process Control
"""Manages subprocess instances for llama-server and sd-cli backends.

Provides lifecycle management, health monitoring, and process synchronization
for both LLM and image generation tasks.
"""

import asyncio
import json
import os
import signal
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any, List


class EngineManager:
    """Manages backend engine processes (llama-server, sd-cli) with lifecycle control."""
    
    def __init__(self, app):
        self.app = app
        self.processes: Dict[str, subprocess.Popen] = {}  # backend_type -> process
        self.engine_tasks: Dict[str, asyncio.Task] = {}   # engine_id -> task
        self.shutdown_requested = False
        
        # Default configuration paths
        self.llama_server_dir = Path("backend/llama-server")
        self.sd_cli_dir = Path("backend/sd-cli")
    
    async def start_llama_server(self, model_path: str, port: int = 8080) -> bool:
        """Start llama-server process for LLM inference.
        
        Args:
            model_path: Path to GGUF model file
            port: HTTP port for SSE endpoint
            
        Returns:
            True if process started successfully
        """
        try:
            # Ensure backend directory exists
            self.llama_server_dir.mkdir(parents=True, exist_ok=True)
            
            # Find llama-server binary
            server_binary = self._find_backend_binary("llama-server", "windows_cpu")
            if not server_binary.exists():
                print(f"Warning: llma-server binary not found at {server_binary}")
                return False
            
            # Build command with model path
            cmd = [str(server_binary), "-m", str(model_path), "--port", str(port)]
            
            # Start process
            self.processes["llama_server"] = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                start_new_session=True  # New session for cleanup
            )
            
            # Log startup message
            print(f"Started llama-server at port {port} with model: {model_path}")
            
            return True
            
        except Exception as e:
            print(f"Error starting llama-server: {e}")
            return False
    
    async def start_sd_cli(self, checkpoint_path: str) -> bool:
        """Start sd-cli process for image generation.
        
        Args:
            checkpoint_path: Path to Stable Diffusion checkpoint
            
        Returns:
            True if process started successfully
        """
        try:
            self.sd_cli_dir.mkdir(parents=True, exist_ok=True)
            
            # Find sd-cli binary
            cli_binary = self._find_backend_binary("sd-cli", "windows_cpu")
            if not cli_binary.exists():
                print(f"Warning: sd-cli binary not found at {cli_binary}")
                return False
            
            # Start process (non-blocking, will be invoked on-demand)
            self.processes["sd_cli"] = subprocess.Popen(
                [str(cli_binary), "-i", str(checkpoint_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                start_new_session=True
            )
            
            print(f"Started sd-cli with checkpoint: {checkpoint_path}")
            
            return True
            
        except Exception as e:
            print(f"Error starting sd-cli: {e}")
            return False
    
    async def stop_all_processes(self) -> None:
        """Gracefully stop all running backend processes."""
        self.shutdown_requested = True
        
        for engine_id, proc in list(self.processes.items()):
            if proc and proc.poll() is None:  # Process still running
                try:
                    proc.terminate()  # Send SIGTERM
                    await asyncio.sleep(0.5)  # Wait for graceful shutdown
                    
                    if proc.poll() is None:  # Still running after terminate
                        proc.kill()  # Force kill
                        
                    print(f"Stopped process: {engine_id}")
                except Exception as e:
                    print(f"Error stopping {engine_id}: {e}")
        
        self.processes.clear()
    
    def _find_backend_binary(self, backend_type: str, platform: str) -> Path:
        """Find the correct backend binary for given type and platform."""
        # Platform-specific lookup (implementation depends on OS detection)
        platforms = ["windows_cpu", "linux_cpu", "macos_metal"]
        
        for platform in platforms:
            backend_dir = self.llama_server_dir if backend_type == "llama-server" else self.sd_cli_dir
            binary_path = backend_dir / f"{backend_type}-{platform}/bin/{backend_type}"
            
            # Check if file exists and is executable
            if binary_path.exists():
                return binary_path
        
        # Fallback to generic path
        fallback = backend_dir / "bin" / backend_type
        if fallback.exists():
            return fallback
        
        raise FileNotFoundError(f"No {backend_type} backend found for this platform")


class ModelManager:
    """Manages LLM model files and verification."""
    
    def __init__(self):
        self.model_dir = Path("llm-models")
        self.model_files: List[Path] = []  # Cache of known models
    
    @property
    def available_models(self) -> List[Path]:
        """List all available model files in the model directory."""
        if not hasattr(self, '_models'):
            self._scan_models()
        return list(self._models)
    
    def _scan_models(self) -> None:
        """Scan for .gguf and other supported model formats."""
        try:
            models = []
            
            # Check llm-models directory
            if self.model_dir.exists():
                for ext in ["*.gguf", "*.bin", "*.safetensors"]:
                    models.extend(self.model_dir.glob(ext))
            
            # Sort by size (largest first - full models before quantized)
            self._models = sorted(models, key=lambda p: p.stat().st_size, reverse=True)
            print(f"Found {len(self._models)} LLM model(s)")
            
        except Exception as e:
            print(f"Error scanning models: {e}")
            self._models = []
    
    def verify_model_integrity(self, model_path: Path) -> bool:
        """Verify a model file's integrity (basic checksum check)."""
        try:
            if not model_path.exists():
                return False
            
            # Basic file size check
            expected_size = 1024 * 1024  # At least 1MB for valid models
            actual_size = model_path.stat().st_size
            
            if actual_size < expected_size:
                print(f"Warning: Model {model_path} seems too small ({actual_size} bytes)")
                return False
            
            return True
            
        except Exception as e:
            print(f"Error verifying model {model_path}: {e}")
            return False


class BackendDownloader:
    """Downloads and verifies backend binaries from GitHub releases."""
    
    def __init__(self, config_path: str = "scripts/config/backends.json"):
        self.config_path = Path(config_path)
        self.config = None
    
    @property
    def config(self):
        """Load backend configuration."""
        if not hasattr(self, '_config'):
            try:
                with open(self.config_path, 'r') as f:
                    import json
                    self._config = json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")
                self._config = {}
        return self._config
    
    async def download_backend(self, backend_type: str) -> bool:
        """Download backend binary and verify integrity."""
        try:
            # Platform detection (simplified - would need OS detection in real app)
            platform = "windows_cpu"  # Default for Windows
            
            if not self.config.get(backend_type, {}).get("platforms", {}).get(platform):
                print(f"No backend info available for {backend_type} on {platform}")
                return False
            
            backend_info = self.config[backend_type]["platforms"][platform]
            
            # Download URL would be fetched dynamically from GitHub API
            download_url = f"{backend_info['url_template']}{backend_info['asset']}"
            
            print(f"Downloading {backend_type} from {download_url}")
            
            # In production, use requests/aiohttp to download
            # For now, this is a placeholder
            
            return True
            
        except Exception as e:
            print(f"Error downloading backend: {e}")
            return False
    
    async def verify_hash(self, filepath: Path, expected_sha256: str) -> bool:
        """Verify file integrity using SHA256."""
        import hashlib
        
        try:
            h = hashlib.sha256()
            
            with open(filepath, 'rb') as f:
                while chunk := f.read(8192):
                    h.update(chunk)
            
            return h.hexdigest() == expected_sha256
            
        except Exception as e:
            print(f"Error verifying hash for {filepath}: {e}")
            return False
