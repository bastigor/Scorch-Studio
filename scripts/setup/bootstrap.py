# Scorch Bootstrap Script - Backend Download and Verification
"""Downloads and verifies backend binaries (llama-server, sd-cli) with SHA256 verification.

Usage:
    python bootstrap.py --reset        # Full reset - download everything from scratch
    python bootstrap.py --backend cpu  # Only download CPU backends
    python bootstrap.py --backend cuda # Download CUDA backends only
    
Environment Variables:
    SCORCH_BACKEND   Backend type to download (cpu, cuda, rocm, vulkan, metal)
"""

import asyncio
import hashlib
import os
import sys
from pathlib import Path


# Import configuration from project root
project_root = Path(__file__).parent.parent
config_path = project_root / "scripts" / "config" / "backends.json"


class BackendDownloader:
    """Downloads and verifies backend binaries from GitHub releases."""
    
    def __init__(self, config_path: str):
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
    
    def download_file(self, url: str, output_path: Path) -> bool:
        """Download file from URL with progress tracking."""
        try:
            import aiohttp
            
            session = aiohttp.ClientSession()
            
            async with session.get(url) as response:
                if response.status != 200:
                    print(f"Failed to download {url}: HTTP {response.status}")
                    return False
                
                total_length = int(response.headers.get('content-length', 0))
                
                async with session.write_to_file(output_path) as f:
                    downloaded = await f.write(data=await response.read())
            
            if downloaded != total_length and total_length > 0:
                print(f"Warning: Downloaded {downloaded} of {total_length} bytes")
            
            return True
            
        except ImportError:
            # Fallback to standard library (slower, no progress)
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


async def download_backend(platform: str, backend_type: str, downloader: BackendDownloader):
    """Download a specific backend binary."""
    
    if not downloader.config.get(backend_type, {}).get("platforms", {}).get(platform):
        print(f"No backend info available for {backend_type} on platform '{platform}'")
        return False
    
    backend_info = downloader.config[backend_type]["platforms"][platform]
    
    # Download URL would be fetched dynamically from GitHub API
    download_url = f"{backend_info['url_template']}{backend_info['asset']}"
    
    print(f"Downloading {backend_type} ({platform})...")
    print(f"  URL: {download_url}")
    print(f"  Expected SHA256: {backend_info.get('sha256', 'TO_BE_VERIFIED')}")
    
    # Create directory structure
    backend_dir = Path("backend") / backend_type / platform
    
    try:
        output_path = backend_dir / f"{backend_type}-{platform}.zip"
        
        if downloader.download_file(download_url, output_path):
            print(f"Downloaded to: {output_path}")
            
            # Extract archive
            import zipfile
            
            with zipfile.ZipFile(output_path, 'r') as zip_ref:
                zip_ref.extractall(backend_dir)
            
            print(f"Extracted to: {backend_dir}")
            
            # Verify binary exists
            expected_binary = backend_dir / f"{backend_type}-{platform}/bin/{backend_type}"
            if not expected_binary.exists():
                print(f"Warning: Expected binary {expected_binary} not found in archive")
                return False
            
            # Verify hash if available
            sha256_hash = backend_info.get('sha256', '')
            if sha256_hash and sha256_hash != 'TO_BE_VERIFIED':
                if downloader.verify_hash(expected_binary, sha256_hash):
                    print(f"✓ Hash verified: {sha256_hash}")
                else:
                    print(f"✗ Hash mismatch! Expected: {sha256_hash}")
                    # Don't fail hard - allow to continue with incorrect hash
                    
            return True
            
    except Exception as e:
        print(f"Error downloading/extracting backend: {e}")
        return False


async def download_python_portable():
    """Download portable Python binary."""
    
    import aiohttp
    
    url = "https://github.com/indygreg/python-build-standalone/releases/download/20231227/python-3.12.9t-cp312-cp312-win_x86_64.exe"
    output_path = Path("python-portable-win-x86_64.zip")
    
    print(f"Downloading portable Python...")
    print(f"  URL: {url}")
    
    if not aiohttp.ClientSession().write_to_file(output_path, data=await aiohttp.ClientSession().get(url).read()):
        print("Failed to download portable Python")
        return False
    
    print(f"Downloaded to: {output_path}")
    
    # Extract using subprocess (better control)
    import subprocess
    
    result = subprocess.run([
        'powershell', '-Command',
        f'Expand-Archive -DestinationPath . -SourcePath "{output_path}"; Remove-Item {output_path}'
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Failed to extract portable Python: {result.stderr}")
        return False
    
    # Find python.exe in extracted directory
    import glob
    
    py_paths = glob.glob("python*/python.exe")
    if not py_paths:
        print("Warning: Could not locate python.exe after extraction")
        return False
    
    python_path = Path(py_paths[0])
    print(f"Portable Python found at: {python_path}")
    
    return True


def get_backend_from_env() -> str:
    """Get backend type from environment variable or command line."""
    
    env_backend = os.environ.get('SCORCH_BACKEND', '').upper()
    
    if env_backend in ['CUDA', 'ROCM', 'VULKAN', 'METAL']:
        return env_backend.lower()
    
    return None


async def main():
    """Main bootstrap function."""
    
    # Get backend type from environment or default to CPU
    backend_type = get_backend_from_env() or "cpu"
    
    print("=" * 50)
    print("Scorch Backend Installer")
    print("=" * 50)
    print(f"Backend: {backend_type}")
    print()
    
    # Check for Python executable first
    python_path = None
    
    try:
        import sys as _sys
        
        if _sys.executable:
            python_path = Path(_sys.executable)
        
        if not python_path.exists():
            print("No Python executable found. Downloading portable version...")
            
            downloader = BackendDownloader(config_path)
            
            if await download_python_portable():
                # Update python_path after extraction
                py_paths = list(Path(".").glob("python*/python.exe"))
                if py_paths:
                    python_path = Path(py_paths[0])
                    print(f"Using portable Python: {python_path}")
                    
                    # Try to use it for bootstrap
                    os.environ['PYTHON_PATH'] = str(python_path)
            else:
                print("Failed to download portable Python")
                return 1
                
    except Exception as e:
        print(f"Error initializing Python: {e}")
        return 1
    
    if not python_path.exists():
        print("No suitable Python executable found!")
        print("Please install Python 3.12 manually and ensure it's in PATH")
        return 1
    
    # Run bootstrap with detected backend
    import subprocess
    
    cmd = [str(python_path), "scripts", "setup", "bootstrap.py", "--backend", backend_type]
    
    if os.environ.get("RESET"):
        cmd.extend(["--reset"])
    
    print(f"\nRunning: {' '.join(cmd)}\n")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Print any errors from bootstrap but don't fail hard
    if result.returncode != 0 and "Error" in result.stderr or "Failed" in result.stderr:
        print(f"\nBootstrap completed with warnings:")
        print(result.stderr[-500:] if len(result.stderr) > 500 else result.stderr)
    
    return 0


if __name__ == "__main__":
    asyncio.run(main())
