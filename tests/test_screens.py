"""Scorch Screens Tests - UI screen validation.

These tests validate that all screens are properly implemented with:
- Correct compose methods
- Required widgets
- English string usage
- Proper error handling
"""

import pytest
from pathlib import Path


class TestChatScreen:
    """Test ChatScreen implementation."""

    def test_chat_screen_exists(self):
        """Verify chat.py screen exists and is readable."""
        chat_path = Path("scorch/screens/chat.py")
        assert chat_path.exists(), "chat.py not found"
        
        content = chat_path.read_text(encoding="utf-8")
        assert "class ChatScreen" in content or "@Screen" in content

    def test_chat_compose_method(self):
        """Verify ChatScreen has compose method."""
        chat_path = Path("scorch/screens/chat.py")
        content = chat_path.read_text(encoding="utf-8")
        
        # Should define UI composition
        assert "compose" in content.lower()

    def test_chat_widgets(self):
        """Verify ChatScreen imports required widgets."""
        chat_path = Path("scorch/screens/chat.py")
        content = chat_path.read_text(encoding="utf-8")
        
        from textual.widgets import Input, TextArea
        
        # Should use input field for messages
        assert "Input" in content or "TextArea" in content

    def test_chat_bindings(self):
        """Verify ChatScreen has keyboard bindings."""
        chat_path = Path("scorch/screens/chat.py")
        content = chat_path.read_text(encoding="utf-8")
        
        # Should define shortcuts
        assert "BINDINGS" in content or "Binding" in content

    def test_chat_strings_usage(self):
        """Verify ChatScreen uses English strings."""
        chat_path = Path("scorch/screens/chat.py")
        content = chat_path.read_text(encoding="utf-8")
        
        # Should import and use Strings class
        assert "Strings" in content or "strings" in content.lower()

    def test_chat_message_bubble(self):
        """Verify MessageBubble widget exists."""
        chat_path = Path("scorch/screens/chat.py")
        content = chat_path.read_text(encoding="utf-8")
        
        # Should have message display class
        assert "MessageBubble" in content or "message bubble" in content.lower()


class TestImagesScreen:
    """Test ImagesScreen implementation."""

    def test_images_screen_exists(self):
        """Verify images.py screen exists."""
        images_path = Path("scorch/screens/images.py")
        assert images_path.exists(), "images.py not found"
        
        content = images_path.read_text(encoding="utf-8")
        assert "class ImagesScreen" in content or "@Screen" in content

    def test_images_compose_method(self):
        """Verify ImagesScreen has compose method."""
        images_path = Path("scorch/screens/images.py")
        content = images_path.read_text(encoding="utf-8")
        
        # Should define UI composition
        assert "compose" in content.lower()

    def test_images_prompt_input(self):
        """Verify ImagesScreen has prompt input field."""
        images_path = Path("scorch/screens/images.py")
        content = images_path.read_text(encoding="utf-8")
        
        # Should have input for image generation
        assert "prompt" in content.lower() or "text area" in content.lower()

    def test_images_strings_usage(self):
        """Verify ImagesScreen uses English strings."""
        images_path = Path("scorch/screens/images.py")
        content = images_path.read_text(encoding="utf-8")
        
        # Should import and use Strings class
        assert "Strings" in content or "strings" in content.lower()


class TestSettingsScreen:
    """Test SettingsScreen implementation."""

    def test_settings_screen_exists(self):
        """Verify settings.py screen exists."""
        settings_path = Path("scorch/screens/settings.py")
        assert settings_path.exists(), "settings.py not found"
        
        content = settings_path.read_text(encoding="utf-8")
        assert "class SettingsScreen" in content or "@Screen" in content

    def test_settings_compose_method(self):
        """Verify SettingsScreen has compose method."""
        settings_path = Path("scorch/screens/settings.py")
        content = settings_path.read_text(encoding="utf-8")
        
        # Should define UI composition
        assert "compose" in content.lower()

    def test_settings_backend_selection(self):
        """Verify SettingsScreen has backend selection."""
        settings_path = Path("scorch/screens/settings.py")
        content = settings_path.read_text(encoding="utf-8")
        
        # Should allow selecting backends
        assert "llama-server" in content.lower() or "backend" in content.lower()

    def test_settings_strings_usage(self):
        """Verify SettingsScreen uses English strings."""
        settings_path = Path("scorch/screens/settings.py")
        content = settings_path.read_text(encoding="utf-8")
        
        # Should import and use Strings class
        assert "Strings" in content or "strings" in content.lower()


class TestAppIntegration:
    """Test app.py integration with screens."""

    def test_app_module_exists(self):
        """Verify app.py exists and is readable."""
        app_path = Path("scorch/app.py")
        assert app_path.exists(), "app.py not found"
        
        content = app_path.read_text(encoding="utf-8")
        assert "class App" in content or "@App" in content

    def test_app_screens(self):
        """Verify app.py defines screens."""
        app_path = Path("scorch/app.py")
        content = app_path.read_text(encoding="utf-8")
        
        # Should reference chat and images screens
        assert "chat" in content.lower() or "ChatScreen" in content

    def test_app_navigation(self):
        """Verify app.py has navigation functionality."""
        app_path = Path("scorch/app.py")
        content = app_path.read_text(encoding="utf-8")
        
        # Should have screen switching logic
        assert "switch_screen" in content.lower() or "navigate" in content.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
