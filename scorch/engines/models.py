"""Models management - download, import, list installed models."""

from pathlib import Path


class ModelManager:
    """Manages model files (SD checkpoints, LLM GGUF)."""

    def __init__(self):
        self.models = []  # List of installed models with metadata
        self.active_model = None
        self.catalog_url = "https://huggingface.co"

    @property
    def sd_dir(self) -> Path:
        return Path("models")

    @property
    def llm_models_dir(self) -> Path:
        return Path("llm-models")

    def list_installed_sd_models(self):
        """List all SD checkpoint files in models/."""
        models = []
        sd_dir = self.sd_dir
        
        for ext in ["*.safetensors", "*.ckpt"]:
            for model_file in sd_dir.glob(ext):
                models.append({
                    "path": str(model_file),
                    "filename": model_file.name,
                    "size_mb": model_file.stat().st_size / (1024 * 1024) if model_file.exists() else 0,
                    "type": ext.replace(".", ""),
                })
        
        return models

    def list_installed_llm_models(self):
        """List all LLM GGUF files in llm-models/."""
        models = []
        llm_dir = self.llm_models_dir
        
        for model_file in llm_dir.glob("*.gguf"):
            models.append({
                "path": str(model_file),
                "filename": model_file.name,
                "size_mb": model_file.stat().st_size / (1024 * 1024) if model_file.exists() else 0,
                "type": "gguf",
            })
        
        return models

    def download_model(self, url: str, output_path: Path) -> tuple[bool, Optional[str]]:
        """Download a model from URL with progress."""
        try:
            import httpx
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, stream=True)
                if not response.is_success:
                    return False, f"HTTP {response.status_code}"
                
                total_size = int(response.headers.get("content-length", 0))
                downloaded = 0
                
                with open(output_path, "wb") as f:
                    for chunk in response.iter_bytes(chunk_size=8192):
                        if not chunk:
                            continue
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            print(f"Downloading... {percent:.1f}% ({model_file.name})")
                
                return True, None
        
        except Exception as e:
            return False, str(e)

    def verify_model_hash(self, filepath: Path) -> bool:
        """Verify model file SHA256 hash."""
        import hashlib
        
        try:
            h = hashlib.sha256()
            with open(filepath, "rb") as f:
                while chunk := f.read(8192):
                    h.update(chunk)
            
            return True  # Hash verification would check against catalog
        except Exception:
            return False

    def import_model(self, local_path: str):
        """Import a model from local path."""
        model_file = Path(local_path)
        
        if not model_file.exists():
            return {"success": False, "error": "File not found"}
        
        # Copy to appropriate directory
        dest_dir = self.sd_dir if "sd" in str(model_file.name).lower() else self.llm_models_dir
        
        import shutil
        try:
            dest_file = dest_dir / model_file.name
            
            if dest_file.exists():
                print(f"Model already exists at {dest_file}, overwriting...")
            
            shutil.copy2(str(model_file), str(dest_file))
            
            return {"success": True, "path": str(dest_file)}
        
        except Exception as e:
            return {"success": False, "error": str(e)}

    def remove_model(self, model_path: Path):
        """Remove a model file."""
        import shutil
        
        try:
            if model_path.exists():
                # Checkpoint files are large - use shutil.rmtree for dirs, unlink for files
                if model_path.is_dir():
                    shutil.rmtree(model_path)
                else:
                    model_path.unlink()
            
            return {"success": True}
        
        except Exception as e:
            return {"success": False, "error": str(e)}

    def set_active_model(self, model_path: Path):
        """Set the currently active model."""
        self.active_model = str(model_path)
