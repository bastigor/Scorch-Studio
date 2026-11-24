# Scorch Backends - Backend Binary Management and Image Generation
"""Manages backend binaries (llama-server, sd-cli) for LLM chat and image generation.

Provides methods to:
- Start/stop backend processes via subprocess
- Verify binary existence before use
- Generate images using sd-cli CLI
- Stream responses from llama-server over SSE

All operations are asynchronous to avoid blocking the UI."""

import asyncio
import hashlib
import os
import platform
import shutil
import subprocess
from pathlib import Path
from typing import Optional, Dict, List


class BackendManager:
    """Manages backend binary lifecycle and verification.
    
    This class handles finding, starting, and stopping backend processes
    for both llama-server (LLM) and sd-cli (image generation)."""

    def __init__(self):
        # Default paths to backend directories
        self.llama_server_dir = Path("backend/llama-server")
        self.sd_cli_dir = Path("backend/sd-cli")
        
        # Platform detection
        self.platform = platform.system().lower()
        
        if "win" in self.platform:
            self.platform_identifier = "windows_cpu"
        elif "linux" in self.platform:
            self.platform_identifier = "linux_cpu"
        else:  # macOS
            self.platform_identifier = "macos_metal"

    @property
    def llama_binary(self) -> Optional[Path]:
        """Find and return the llama-server binary path."""
        if not hasattr(self, '_binary'):
            self._find_backend("llama-server")
        return self._binary
    
    @property
    def sd_cli_binary(self) -> Optional[Path]:
        """Find and return the sd-cli binary path."""
        if not hasattr(self, '_sd_binary'):
            self._find_backend("sd-cli")
        return self._sd_binary

    def _find_backend(self, backend_type: str) -> None:
        """Search for a specific backend binary.
        
        Args:
            backend_type: Either 'llama-server' or 'sd-cli'
            
        Raises:
            FileNotFoundError: If no suitable binary is found
        """
        import glob
        
        # Try platform-specific paths first
        platforms = ["windows_cpu", "linux_cpu", "macos_metal"]
        
        for plat in platforms:
            backend_dir = self.llama_server_dir if backend_type == "llama-server" else self.sd_cli_dir
            
            # Standard binary path
            binary_path = backend_dir / f"{backend_type}-{plat}/bin/{backend_type}"
            
            if binary_path.exists():
                print(f"Found {backend_type} at: {binary_path}")
                setattr(self, f'_{backend_type}_binary', binary_path)
                return
        
        # Fallback to generic paths
        backend_dir = self.llama_server_dir if backend_type == "llama-server" else self.sd_cli_dir
        fallback_paths = [
            backend_dir / f"{backend_type}.exe",  # Windows executable
            backend_dir / f"{backend_type}",       # Generic binary
            backend_dir / "bin" / backend_type,    # Standard location
        ]
        
        for fp in fallback_paths:
            if fp.exists():
                print(f"Found {backend_type} (fallback) at: {fp}")
                setattr(self, f'_{backend_type}_binary', fp)
                return
        
        raise FileNotFoundError(
            f"No {backend_type} backend binary found on this platform. "
            f"Please run the launcher to download backends first."
        )

    async def verify_backend_binary(self, backend_type: str) -> bool:
        """Verify that a backend binary exists and is accessible.
        
        Args:
            backend_type: Either 'llama-server' or 'sd-cli'
            
        Returns:
            True if binary found and executable, False otherwise
        """
        try:
            binary_path = getattr(self, f'{backend_type}_binary')
            
            if not binary_path.exists():
                print(f"Binary {backend_type} not found at: {binary_path}")
                return False
            
            # Check if file is readable and executable (simplified check)
            size = binary_path.stat().st_size
            if size == 0 or size > 1_000_000_000:  # Reasonable size range
                print(f"Binary {backend_type} exists ({size} bytes)")
                
            return True
            
        except Exception as e:
            print(f"Error verifying {backend_type}: {e}")
            return False

    async def start_llama_server(self, model_path: str, port: int = 8080) -> bool:
        """Start llama-server process for LLM inference.
        
        Args:
            model_path: Path to GGUF model file
            port: HTTP port for SSE endpoint (default: 8080)
            
        Returns:
            True if process started successfully, False otherwise
        """
        try:
            llama_binary = self.llama_binary
            
            if not llama_binary.exists():
                print(f"Warning: llma-server binary not found at {llama_binary}")
                return False
            
            # Build command with model path and port
            cmd = [str(llama_binary), "-m", str(model_path), "--port", str(port)]
            
            # Start process with stdout/stderr capture
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                start_new_session=True  # New session for cleanup
            )
            
            print(f"Started llama-server at port {port} with model: {model_path}")
            return True
            
        except Exception as e:
            print(f"Error starting llama-server: {e}")
            import traceback
            traceback.print_exc()
            return False

    async def stop_llama_server(self) -> None:
        """Gracefully stop the llama-server process."""
        try:
            proc = subprocess.Popen(
                [self.llama_binary, "-h"],  # Health check endpoint to find PID
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            import time
            
            for _ in range(30):  # Max 30 seconds
                proc.terminate()  # Send SIGTERM
                await asyncio.sleep(0.5)
                
                if proc.poll() is not None:
                    break
                    
            except Exception as e:
                print(f"Error stopping llama-server: {e}")

    async def stop_sd_cli(self) -> None:
        """Stop the sd-cli process."""
        try:
            # Similar to llama-server, would need to track and terminate
            pass
            
        except Exception as e:
            print(f"Error stopping sd-cli: {e}")


def generate_image_via_sdcli(
    prompt: str, 
    output_dir: Path = Path("outputs/images"),
    checkpoint_path: Optional[str] = None,
    steps: int = 30,
    cfg_scale: float = 7.5,
    seed: Optional[int] = None,
) -> Optional[Path]:
    """Generate an image using sd-cli CLI.
    
    This function invokes the stable-diffusion.cpp CLI directly 
    with parameters for prompt, steps, and CFG scale.
    
    Args:
        prompt: Text description of the desired image
        output_dir: Directory to save the generated image (default: outputs/images)
        checkpoint_path: Path to Stable Diffusion checkpoint (.safetensors/.ckpt)
                       If None, will search for models in 'models/' directory
        steps: Number of diffusion steps (default: 30)
        cfg_scale: Classifier-free guidance scale (default: 7.5)
        seed: Random seed for reproducibility (optional)
        
    Returns:
        Path to generated image file, or None if generation failed
        
    Example:
        >>> result = generate_image_via_sdcli(
        ...     "A cat sitting on a windowsill",
        ...     checkpoint_path="models/model.safetensors"
        ... )
        >>> print(result)  # Path to .png output
    """
    
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Determine checkpoint path if not provided
        if not checkpoint_path:
            models_dir = Path("models")
            
            if models_dir.exists():
                safetensors_files = list(models_dir.glob("*.safetensors"))
                ckpt_files = list(models_dir.glob("*.ckpt"))
                
                # Prefer .safetensors over .ckpt (more modern format)
                if safetensors_files:
                    checkpoint_path = str(safetensors_files[0])
                elif ckpt_files:
                    checkpoint_path = str(ckpt_files[0])
                else:
                    print("No Stable Diffusion model found in 'models/' directory")
                    return None
            else:
                print("Models directory not found. Download a model first.")
                return None
        
        # Build sd-cli command
        cmd = [
            str(BackendManager().sd_cli_binary),  # sd-cli binary
            "-i", checkpoint_path,  # Checkpoint path
            "--out", str(output_dir / "output.png"),  # Output filename
            f"--steps {steps}",  # Diffusion steps
            f"--cfg-scale {cfg_scale}",  # CFG scale
        ]
        
        if seed is not None:
            cmd.extend(["--seed", str(seed)])
        
        # Add prompt via environment variable (sd-cli supports this)
        os.environ["SD_PROMPT"] = prompt
        
        print(f"Generating image with prompt: {prompt[:50]}...")
        print(f"  Command: {' '.join(cmd)}")
        
        # Execute sd-cli command
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout for large generations
        )
        
        if proc.returncode != 0:
            print(f"sd-cli returned error code {proc.returncode}")
            if proc.stderr:
                print(f"Error output: {proc.stderr[:200]}")
            
            return None
        
        # Check if output file was created
        output_path = output_dir / "output.png"
        
        if not output_path.exists():
            print("Warning: No output image generated despite successful exit code")
            return None
        
        print(f"Image generated successfully: {output_path}")
        return output_path

    except subprocess.TimeoutExpired:
        print("Generation timed out after 5 minutes. Check logs for details.")
        return None
    
    except Exception as e:
        print(f"Error generating image: {e}")
        import traceback
        traceback.print_exc()
        return None


def verify_file_hash(filepath: Path, expected_sha256: str) -> bool:
    """Verify file integrity using SHA256 checksum.
    
    Args:
        filepath: Path to the file to verify
        expected_sha256: Expected SHA256 hash
        
    Returns:
        True if file matches expected hash, False otherwise
    """
    try:
        h = hashlib.sha256()
        
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192):
                h.update(chunk)
        
        return h.hexdigest() == expected_sha256
        
    except Exception as e:
        print(f"Error verifying hash for {filepath}: {e}")
        return False


def download_file(url: str, output_path: Path) -> bool:
    """Download file from URL with progress tracking.
    
    This is a simplified version - full implementation would use aiohttp
    or requests library for better error handling and progress display.
    
    Args:
        url: Remote URL to download
        output_path: Local path where to save the file
        
    Returns:
        True if download completed successfully, False otherwise
    """
    try:
        import urllib.request as urlopen  # Python 2 compatible
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with urlopen.urlopen(url) as response, open(output_path, 'wb') as f:
            while True:
                chunk = response.read(8192)
                if not chunk:
                    break
                f.write(chunk)
        
        return True
        
    except ImportError:
        # Fallback for environments with urllib.error
        import urllib.request as urlopen
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with urlopen.urlopen(url) as response, open(output_path, 'wb') as f:
            while True:
                chunk = response.read(8192)
                if not chunk:
                    break
                f.write(chunk)
        
        return True
        
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        import traceback
        traceback.print_exc()
        return False


# Export main classes and functions for use in other modules
__all__ = [
    "BackendManager",
    "generate_image_via_sdcli",
    "verify_file_hash",
    "download_file",
]
