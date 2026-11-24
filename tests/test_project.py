"""Scorch Project Structure Tests.

These tests validate the overall project structure and ensure all required components exist."""

import pytest
from pathlib import Path


class TestProjectRoot:
    """Test project root files and directories."""

    def test_readme_exists(self):
        """Verify README.md exists with proper content."""
        readme_path = Path("README.md")
        assert readme_path.exists()
        
        content = readme_path.read_text(encoding="utf-8")
        assert "Scorch" in content, "Missing project name in README"
        assert "Offline" in content or "offline-first" in content.lower()

    def test_license_exists(self):
        """Verify LICENSE file exists."""
        license_path = Path("LICENSE")
        assert license_path.exists(), "LICENSE file not found"
        
        content = license_path.read_text(encoding="utf-8")
        assert "MIT" in content or "License" in content

    def test_requirements_exists(self):
        """Verify requirements.txt exists with dependencies."""
        req_path = Path("requirements.txt")
        assert req_path.exists()
        
        content = req_path.read_text(encoding="utf-8")
        assert "textual>=" in content, "Missing textual dependency"

    def test_data_directories_exist(self):
        """Verify all required data directories exist."""
        paths_to_check = [
            Path("data"),
            Path("backend"),
            Path("outputs/images"),
            Path("llm-models"),
            Path("models"),
        ]
        
        for p in paths_to_check:
            assert p.exists(), f"Directory not found: {p}"


class TestScorchPackage:
    """Test scorch package structure."""

    def test_scorch_directory_exists(self):
        """Verify scorch directory exists."""
        scorch_path = Path("scorch")
        assert scorch_path.exists() and scorch_path.is_dir()

    def test_core_files_exist(self):
        """Verify core scorch files exist."""
        required_files = [
            "app.py",
            "strings.py",
            "storage.py",
            "theme.tcss",
            "backends.py",
        ]
        
        for filename in required_files:
            file_path = Path("scorch") / filename
            assert file_path.exists(), f"{filename} not found"

    def test_widgets_directory_exists(self):
        """Verify widgets directory and files exist."""
        widget_dir = Path("scorch/widgets")
        assert widget_dir.exists()
        
        widget_files = ["panel.py", "monitor.py"]
        for filename in widget_files:
            file_path = widget_dir / filename
            assert file_path.exists(), f"widgets/{filename} not found"

    def test_engines_directory_exists(self):
        """Verify engines directory and files exist."""
        engine_dir = Path("scorch/engines")
        assert engine_dir.exists()
        
        engine_files = ["manager.py", "models.py"]
        for filename in engine_files:
            file_path = engine_dir / filename
            assert file_path.exists(), f"engines/{filename} not found"

    def test_screens_directory_exists(self):
        """Verify screens directory and files exist."""
        screen_dir = Path("scorch/screens")
        assert screen_dir.exists()
        
        # Check for at least one screen file
        screen_files = list(screen_dir.glob("*.py"))
        assert len(screen_files) >= 1, "No screen files found in screens/"


class TestConfiguration:
    """Test configuration files."""

    def test_backends_config_exists(self):
        """Verify backends.json exists with proper structure."""
        config_path = Path("scripts/config/backends.json")
        assert config_path.exists()
        
        import json
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Check for both backend types
        assert "llama-server" in config, "Missing llama-server config"
        assert "sd-cli" in config, "Missing sd-cli config"

    def test_strings_module_exists(self):
        """Verify strings.py exists with English content."""
        strings_path = Path("scorch/strings.py")
        assert strings_path.exists()
        
        content = strings_path.read_text(encoding="utf-8")
        # Check for English string constants
        assert "Scorch" in content or "APP_NAME" in content

    def test_theme_file_exists(self):
        """Verify theme.tcss exists with color definitions."""
        theme_path = Path("scorch/theme.tcss")
        assert theme_path.exists()
        
        content = theme_path.read_text(encoding="utf-8")
        # Check for red/dark theme colors
        assert "#" in content or "color" in content.lower()


class TestLauncher:
    """Test Windows launcher script."""

    def test_windows_launcher_exists(self):
        """Verify windows.bat exists and is valid batch file."""
        launcher_path = Path("windows.bat")
        assert launcher_path.exists(), "windows.bat not found"
        
        content = launcher_path.read_text(encoding="utf-8")
        # Check for batch file markers
        assert "@echo off" in content, "Not a valid batch file"


class TestDocumentation:
    """Test documentation files."""

    def test_dev_guide_exists(self):
        """Verify dev-guide.md exists."""
        guide_path = Path("dev-guide.md")
        assert guide_path.exists()

    def test_backend_docs_exists(self):
        """Verify docs/backend.md exists."""
        doc_path = Path("docs/backend.md")
        assert doc_path.exists()


class TestTestsDirectory:
    """Test tests directory structure."""

    def test_tests_directory_exists(self):
        """Verify tests directory exists."""
        tests_dir = Path("tests")
        assert tests_dir.exists(), "tests/ directory not found"

    def test_conftest_exists(self):
        """Verify conftest.py configuration file exists."""
        conftest_path = Path("tests/conftest.py")
        assert conftest_path.exists()

    def test_test_files_exist(self):
        """Verify at least one test file exists."""
        test_files = list(Path("tests").glob("test_*.py"))
        assert len(test_files) >= 1, "No test files found in tests/"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
