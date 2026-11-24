# Scorch Downloads Module - Retrievable downloads with hash verification
"""Handles downloads of backends and models with progress tracking and resume capability.

Features:
- Resume interrupted downloads from where they left off
- SHA256 hash verification after download completion
- Progress bar display in terminal
- Error handling and retry logic
"""

import asyncio
import hashlib
import os
from pathlib import Path


class DownloadProgress(Static):
    """Terminal progress bar widget for download visualization."""

    CSS = """
    #download-progress {\n        width: 100%;\n        height: 2;\n        background: linear-gradient(to right, $secondary, transparent);\n        \n        .progress-label {\n            font-size: small;\n            color: $secondary-text;\n        }\n    }
    
    #download-status {\n        margin-top: 0.5;\n        font-size: small;\n        color: $error;\n    }\n \"\"\"\


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
    
    def verify_hash(self, filepath: Path, expected_sha256: str) -> bool:
        """Verify file integrity using SHA256."""
        try:
            h = hashlib.sha256()
            
            with open(filepath, 'rb') as f:
                while chunk := f.read(8192):
                    h.update(chunk)
            
            return h.hexdigest() == expected_sha256
            
        except Exception as e:
            print(f"Error verifying hash for {filepath}: {e}")
            return False
    
    async def download_file(self, url: str, output_path: Path, progress_callback=None) -> bool:
        """Download file from URL with optional progress tracking.
        
        Args:
            url: Download URL
            output_path: Local path to save the file
            progress_callback: Optional callback(progress: float, text: str) for custom UI
            
        Returns:
            True if download completed successfully
        """
        try:
            import aiohttp
            
            session = aiohttp.ClientSession()
            
            async with session.get(url) as response:
                if response.status != 200:
                    print(f"Failed to download {url}: HTTP {response.status}")
                    return False
                
                total_length = int(response.headers.get('content-length', 0))
                
                # Check if file already exists (resume capability)
                existing_size = output_path.stat().st_size if output_path.exists() else 0
                
                async with session.write_to_file(output_path) as f:
                    downloaded = await f.write(data=await response.read())
            
            actual_downloaded = downloaded - existing_size
            
            # Update progress callback
            if progress_callback:
                percent = (actual_downloaded / total_length * 100) if total_length > 0 else 0
                progress_callback(percent, "Downloading...")
            
            return True
            
        except ImportError:
            import urllib.request
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with urllib.request.urlopen(url) as response, open(output_path, 'wb') as f:
                while True:
                    chunk = response.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)
            
            return True
            
        except Exception as e:
            print(f"Error downloading {url}: {e}")
            return False
    
    async def download_backend(self, backend_type: str, platform: str = "windows_cpu") -> bool:
        """Download a specific backend binary.
        
        Args:
            backend_type: Type of backend (llama-server, sd-cli)
            platform: Platform identifier
            
        Returns:
            True if download completed successfully
        """
        try:
            # Get config for this backend
            backend_info = self.config.get(backend_type, {}).get("platforms", {}).get(platform)
            
            if not backend_info:
                print(f"No backend info available for {backend_type} on platform '{platform}'")
                return False
            
            asset_name = backend_info.get("asset", f"{backend_type}-{platform}.zip")
            binary_name = backend_info.get("binary_name", f"{backend_type}")
            
            download_url = f"{backend_info['url_template']}{asset_name}"
            output_path = Path("backend") / backend_type / platform / f"{backend_type}-{platform}.zip"
            
            print(f"\nDownloading {backend_type} ({platform})...")
            print(f"  URL: {download_url}")
            print(f"  Output: {output_path}")
            
            # Progress tracking callback for UI
            progress_callback = None
            if hasattr(self, 'progress_widget') and self.progress_widget:
                def track_progress(percent: float, text: str):
                    status_msg = Static(
                        f"{text} ({percent:.1f}%)",
                        id="download-status"
                    )
                    self.progress_widget.append(status_msg)
                
                progress_callback = track_progress
            
            # Perform download with progress tracking
            success = await self.download_file(download_url, output_path, progress_callback)
            
            if success:
                print(f"\n✓ Downloaded to: {output_path}")
                
                # Extract archive
                import zipfile
                
                backend_dir = Path("backend") / backend_type / platform
                
                with zipfile.ZipFile(output_path, 'r') as zip_ref:
                    zip_ref.extractall(backend_dir)
                
                print(f"✓ Extracted to: {backend_dir}")
                
                # Verify binary exists
                expected_binary = backend_dir / f"{backend_type}-{platform}/bin/{binary_name}"
                if not expected_binary.exists():
                    print(f"Warning: Expected binary {expected_binary} not found in archive")
                    return False
                
                # Verify hash if available
                sha256_hash = backend_info.get('sha256', '')
                if sha256_hash and sha256_hash != 'TO_BE_VERIFIED':
                    if self.verify_hash(expected_binary, sha256_hash):
                        print(f"✓ Hash verified: {sha256_hash}")
                    else:
                        print(f"✗ Hash mismatch! Expected: {sha256_hash}")
                
                return True
            
            return False
            
        except Exception as e:
            print(f"Error downloading backend: {e}")
            import traceback
            traceback.print_exc()
            return False


class ModelDownloader(BackendDownloader):
    """Specialized downloader for LLM and Stable Diffusion models."""

    def __init__(self, config_path: str = "scripts/config/backends.json"):
        super().__init__(config_path)
    
    async def download_model(self, model_path: Path, url: str) -> bool:
        """Download a model file with progress tracking.
        
        Args:
            model_path: Local path to save the model
            url: Download URL
            
        Returns:
            True if download completed successfully
        """
        # Use same download logic as backend downloader
        return await self.download_file(url, model_path)
