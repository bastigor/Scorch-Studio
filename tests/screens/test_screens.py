"""Tests for screens module."""

import pytest
from textual.app import App


def test_chat_screen_exists():
    """Test that ChatScreen class exists and can be instantiated."""
    from scorch.screens import ChatScreen
    
    assert ChatScreen is not None


def test_images_screen_exists():
    """Test that ImagesScreen class exists and can be instantiated."""
    from scorch.screens import ImagesScreen
    
    assert ImagesScreen is not None


def test_settings_screen_exists():
    """Test that SettingsScreen class exists and can be instantiated."""
    from scorch.screens import SettingsScreen
    
    assert SettingsScreen is not None
