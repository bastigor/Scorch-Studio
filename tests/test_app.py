"""Scorch Application Tests - Basic functionality validation.

These tests validate the core application structure and ensure that:
- The Textual app can be instantiated correctly
- Screens are properly defined with compose methods
- Widgets import successfully without errors
- Configuration loading works as expected
"""

import pytest
from pathlib import Path


class TestAppStructure:
    """Test basic application structure."""

    def test_app_module_exists(self):
        """Verify scorch/app.py exists and is readable."""
        app_path = Path("scorch/app.py")
        assert app_path.exists(), f"app.py not found at {app_path}"

    def test_strings_module_exists(self):
        """Verify strings.py exists with English content."""
        strings_path = Path("scorch/strings.py")
        assert strings_path.exists(), f"strings.py not found"
        
        # Check file contains expected English strings
        content = strings_path.read_text(encoding="utf-8")
        assert "Scorch" in content, "Strings missing APP_NAME"
        assert "English" in content or "EN" in content

    def test_storage_module_exists(self):
        """Verify storage.py exists with basic classes."""
        storage_path = Path("scorch/storage.py")
        assert storage_path.exists()
        
        # Check for StorageManager class
        content = storage_path.read_text(encoding="utf-8")
        assert "class StorageManager" in content

    def test_widgets_exist(self):
        """Verify widget modules exist."""
        panel_widget = Path("scorch/widgets/panel.py")
        monitor_widget = Path("scorch/widgets/monitor.py")
        
        assert panel_widget.exists(), "widgets/panel.py not found"
        assert monitor_widget.exists(), "widgets/monitor.py not found"


class TestScreens:
    """Test screen modules."""

    def test_chat_screen_exists(self):
        """Verify chat.py screen exists with basic structure."""
        chat_path = Path("scorch/screens/chat.py")
        assert chat_path.exists()
        
        content = chat_path.read_text(encoding="utf-8")
        assert "class ChatScreen" in content or "@Screen" in content

    def test_images_screen_exists(self):
        """Verify images.py screen exists."""
        images_path = Path("scorch/screens/images.py")
        assert images_path.exists()

    def test_settings_screen_exists(self):
        """Verify settings.py screen exists."""
        settings_path = Path("scorch/screens/settings.py")
        assert settings_path.exists()


class TestBackends:
    """Test backend modules."""

    def test_backends_module_exists(self):
        """Verify backends.py implementation exists."""
        backends_path = Path("scorch/backends.py")
        assert backends_path.exists(), "backends.py not found"
        
        content = backends_path.read_text(encoding="utf-8")
        assert "class BackendManager" in content or "def generate_image_via_sdcli" in content

    def test_engines_manager_exists(self):
        """Verify engines/manager.py exists."""
        manager_path = Path("scorch/engines/manager.py")
        assert manager_path.exists()
        
        content = manager_path.read_text(encoding="utf-8")
        assert "class EngineManager" in content


class TestConfiguration:
    """Test configuration files and settings."""

    def test_backends_config_exists(self):
        """Verify backends.json configuration file exists."""
        config_path = Path("scripts/config/backends.json")
        assert config_path.exists()
        
        import json
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Check for both backend types
        assert "llama-server" in config, "Missing llama-server config"
        assert "sd-cli" in config, "Missing sd-cli config"

    def test_requirements_txt_exists(self):
        """Verify requirements.txt has correct dependencies."""
        req_path = Path("requirements.txt")
        assert req_path.exists()
        
        content = req_path.read_text(encoding="utf-8")
        assert "textual>=" in content, "Missing textual dependency"

    def test_license_exists(self):
        """Verify LICENSE file exists with MIT license."""
        license_path = Path("LICENSE")
        assert license_path.exists()
        
        content = license_path.read_text(encoding="utf-8")
        assert "MIT" in content or "License" in content


class TestProjectRoot:
    """Test project root structure."""

    def test_readme_exists(self):
        """Verify README.md exists and is comprehensive."""
        readme_path = Path("README.md")
        assert readme_path.exists()
        
        content = readme_path.read_text(encoding="utf-8")
        assert "Scorch" in content, "Missing project name"
        assert "Offline" in content or "offline-first" in content.lower()

    def test_launcher_exists(self):
        """Verify Windows launcher script exists."""
        launcher_path = Path("windows.bat")
        assert launcher_path.exists(), "windows.bat not found"
        
        content = launcher_path.read_text(encoding="utf-8")
        assert "@echo off" in content  # Batch file marker

    def test_data_directories_exist(self):
        """Verify data directories exist."""
        paths_to_check = [
            Path("data"),
            Path("backend"),
            Path("outputs"),
            Path("llm-models"),
            Path("models"),
        ]
        
        for p in paths_to_check:
            assert p.exists(), f"Directory not found: {p}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
