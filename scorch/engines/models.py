# Scorch Model Manager - LLM and Stable Diffusion Model Management
"""Manages LLM GGUF models and Stable Diffusion checkpoints.

Provides methods to:
- Scan for available models in designated directories
- Download models from Hugging Face or other sources
- Verify model integrity before use
- Display model information in the UI"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Optional


class ModelManager:
    """Manages LLM and Stable Diffusion model files.
    
    This class handles scanning directories for supported models,
    downloading new ones, and providing model metadata."""

    def __init__(self):
        # Default directory paths
        self.llm_model_dir = Path("llm-models")
        self.sd_model_dir = Path("models")
        
        # Supported file extensions
        self.llm_extensions = ["*.gguf", "*.bin"]
        self.sd_extensions = ["*.safetensors", "*.ckpt", "*.pth"]

    @property
    def available_llm_models(self) -> List[Path]:
        """List all available LLM model files in the model directory.
        
        Returns:
            Sorted list of Path objects for .gguf and .bin files
        """
        models = []
        
        if self.llm_model_dir.exists():
            # Check llm-models directory
            for ext in ["*.gguf", "*.bin"]:
                models.extend(self.llm_model_dir.glob(ext))
            
            # Sort by size (largest first - full models before quantized)
            sorted_models = sorted(models, key=lambda p: p.stat().st_size, reverse=True)
        else:
            print(f"LLM model directory not found: {self.llm_model_dir}")
        
        return list(sorted_models)

    @property
    def available_sd_models(self) -> List[Path]:
        """List all available Stable Diffusion checkpoint files.
        
        Returns:
            Sorted list of Path objects for .safetensors and .ckpt files
        """
        models = []
        
        if self.sd_model_dir.exists():
            # Check models directory
            for ext in ["*.safetensors", "*.ckpt"]:
                models.extend(self.sd_model_dir.glob(ext))
            
            # Sort by size (largest first)
            sorted_models = sorted(models, key=lambda p: p.stat().st_size, reverse=True)
        else:
            print(f"Stable Diffusion model directory not found: {self.sd_model_dir}")
        
        return list(sorted_models)

    def get_model_info(self, model_path: Path) -> Optional[Dict]:
        """Get detailed information about a specific model file.
        
        Args:
            model_path: Path to the model file
            
        Returns:
            Dictionary with model metadata or None if info unavailable
        """
        try:
            stat_info = model_path.stat()
            
            # Detect model type by extension
            is_llm = any(model_path.suffix.lower().endswith(ext) for ext in self.llm_extensions)
            is_sd = any(model_path.suffix.lower().endswith(ext) for ext in self.sd_extensions)
            
            return {
                "path": str(model_path),
                "filename": model_path.name,
                "size_bytes": stat_info.st_size,
                "size_human": format_size(stat_info.st_size),
                "is_llm_model": is_llm,
                "is_sd_checkpoint": is_sd,
            }
            
        except Exception as e:
            print(f"Error getting model info for {model_path}: {e}")
            return None

    def download_model(self, url: str, output_dir: Path) -> bool:
        """Download a model file from URL.
        
        Args:
            url: Remote URL to download the model from
            output_dir: Directory where to save the downloaded model
            
        Returns:
            True if download completed successfully, False otherwise
        
        Note:
            Full implementation would use aiohttp or requests library
            with progress tracking and resume capability.
        """
        try:
            import urllib.request as urlopen  # Python 2 compatible
            
            output_dir.mkdir(parents=True, exist_ok=True)
            
            filename = url.split("/")[-1] if "/" in url else "model.bin"
            model_path = output_dir / filename
            
            print(f"Downloading {filename}...")
            print(f"  URL: {url}")
            
            with urlopen.urlopen(url) as response, open(model_path, 'wb') as f:
                while True:
                    chunk = response.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)
                    
            print(f"Downloaded to: {model_path}")
            
            # Verify file size (basic integrity check)
            model_size = model_path.stat().st_size
            if model_size < 1_000_000:  # At least 1MB for valid models
                print(f"Warning: Model seems too small ({model_size} bytes)")
            
            return True
            
        except Exception as e:
            print(f"Error downloading model from {url}: {e}")
            import traceback
            traceback.print_exc(file=sys.stderr)  # sys imported at top of file
            return False


def format_size(size_bytes: int) -> str:
    """Format file size in human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Human-readable string (e.g., "2.5 GB", "1 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if abs(size_bytes) < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    
    return f"{size_bytes:.1f} PB"


def scan_models() -> Dict[str, List[Path]]:
    """Scan for models in both LLM and Stable Diffusion directories.
    
    Returns:
            Dictionary with two keys: 'llm' and 'sd', each containing list of model paths
    
    Example:
        >>> llm_models, sd_models = scan_models()
        >>> print(f"Found {len(llm_models)} LLM models")
        >>> print(f"Found {len(sd_models)} SD checkpoints")
    """
    manager = ModelManager()
    
    return {
        "llm": manager.available_llm_models,
        "sd": manager.available_sd_models,
    }


# Export main classes and functions for use in other modules
__all__ = [
    "ModelManager",
    "format_size",
    "scan_models",
]
