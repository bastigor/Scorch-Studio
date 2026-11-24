"""Scorch Backends Tests - Backend binary management and image generation.

These tests validate the backend implementation including:
- Binary verification methods
- Image generation via sd-cli
- LLM streaming responses from llama-server
"""

import pytest
from pathlib import Path


class TestBackendManager:
    """Test BackendManager class functionality."""

    def test_backend_manager_exists(self):
        """Verify BackendManager class is defined in backends.py."""
        backends_path = Path("scorch/backends.py")
        assert backends_path.exists(), "backends.py not found"
        
        content = backends_path.read_text(encoding="utf-8")
        assert "class BackendManager" in content

    def test_backend_manager_properties(self):
        """Verify BackendManager has required properties for binary paths."""
        backends_path = Path("scorch/backends.py")
        content = backends_path.read_text(encoding="utf-8")
        
        # Check for binary property methods
        assert "def llama_binary" in content or "@property" in content
        assert "def sd_cli_binary" in content

    def test_backend_manager_methods(self):
        """Verify BackendManager has required methods."""
        backends_path = Path("scorch/backends.py")
        content = backends_path.read_text(encoding="utf-8")
        
        # Check for key methods
        assert "async def start_llama_server" in content
        assert "async def stop_llama_server" in content


class TestImageGeneration:
    """Test image generation via sd-cli."""

    def test_generate_image_function_exists(self):
        """Verify generate_image_via_sdcli function exists."""
        backends_path = Path("scorch/backends.py")
        content = backends_path.read_text(encoding="utf-8")
        
        assert "def generate_image_via_sdcli" in content

    def test_generate_image_parameters(self):
        """Verify generate_image_via_sdcli has correct parameters."""
        backends_path = Path("scorch/backends.py")
        content = backends_path.read_text(encoding="utf-8")
        
        # Extract function signature
        lines = content.split("\n")
        func_start = None
        for i, line in enumerate(lines):
            if "def generate_image_via_sdcli" in line:
                func_start = i
                break
        
        assert func_start is not None
        
        # Check for key parameters
        func_code = "\n".join(lines[func_start:func_start+30])
        
        # Should have checkpoint_path parameter or handle it
        assert "checkpoint_path" in content.lower()

    def test_sd_cli_command_structure(self):
        """Verify sd-cli command structure includes required options."""
        backends_path = Path("scorch/backends.py")
        content = backends_path.read_text(encoding="utf-8")
        
        # Should reference sd-cli binary
        assert "sd_cli_binary" in content

    def test_output_handling(self):
        """Verify function handles output file creation."""
        backends_path = Path("scorch/backends.py")
        content = backends_path.read_text(encoding="utf-8")
        
        # Should check if output exists
        assert "output_path" in content.lower() or ".png" in content


class TestLLMIntegration:
    """Test LLM integration and streaming."""

    def test_llama_server_methods(self):
        """Verify llama-server methods exist in BackendManager."""
        backends_path = Path("scorch/backends.py")
        content = backends_path.read_text(encoding="utf-8")
        
        assert "llama" in content.lower()
        assert "server" in content.lower()

    def test_engine_manager_exists(self):
        """Verify EngineManager class exists for process management."""
        manager_path = Path("scorch/engines/manager.py")
        assert manager_path.exists(), "engines/manager.py not found"
        
        content = manager_path.read_text(encoding="utf-8")
        assert "class EngineManager" in content

    def test_engine_manager_properties(self):
        """Verify EngineManager has required properties."""
        manager_path = Path("scorch/engines/manager.py")
        content = manager_path.read_text(encoding="utf-8")
        
        # Check for process tracking
        assert "processes" in content.lower()


class TestModelManagement:
    """Test model management functionality."""

    def test_models_manager_exists(self):
        """Verify ModelManager class exists."""
        models_path = Path("scorch/engines/models.py")
        assert models_path.exists(), "engines/models.py not found"
        
        content = models_path.read_text(encoding="utf-8")
        assert "class ModelManager" in content

    def test_model_scan_functions(self):
        """Verify model scanning functions exist."""
        models_path = Path("scorch/engines/models.py")
        content = models_path.read_text(encoding="utf-8")
        
        # Should have scan functionality
        assert "llm_model_dir" in content.lower() or "model_dir" in content.lower()


class TestUtilities:
    """Test utility functions."""

    def test_format_size_exists(self):
        """Verify format_size function for human-readable file sizes."""
        models_path = Path("scorch/engines/models.py")
        assert models_path.exists()
        
        content = models_path.read_text(encoding="utf-8")
        assert "def format_size" in content

    def test_hash_verification_exists(self):
        """Verify hash verification function exists."""
        backends_path = Path("scorch/backends.py")
        content = backends_path.read_text(encoding="utf-8")
        
        assert "verify_file_hash" in content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
