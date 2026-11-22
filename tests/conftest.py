"""Pytest configuration and fixtures."""

import pytest


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Setup test environment for each test."""
    pass  # Placeholder - can add actual setup logic here
