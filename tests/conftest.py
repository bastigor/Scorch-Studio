"""Scorch Test Configuration.

This file provides pytest configuration and fixtures for all tests."""

import pytest


@pytest.fixture(scope="session")
def test_data_dir():
    """Return the directory containing test data files."""
    import os
    return os.path.join(os.path.dirname(__file__), "data")


@pytest.fixture
def mock_strings():
    """Provide a mock Strings class for testing screens that depend on strings.py."""
    from scorch.strings import Strings
    return Strings()


@pytest.fixture
def sample_llm_model_path(tmp_path):
    """Create a mock LLM model file in a temporary directory."""
    model_file = tmp_path / "test-model.gguf"
    # Create an empty file (in reality, models would be much larger)
    model_file.write_bytes(b"This is a placeholder GGUF model")
    
    return str(model_file)


@pytest.fixture
def sample_sd_checkpoint(tmp_path):
    """Create a mock Stable Diffusion checkpoint in a temporary directory."""
    checkpoint = tmp_path / "test-checkpoint.safetensors"
    checkpoint.write_bytes(b"This is a placeholder SD checkpoint")
    
    return str(checkpoint)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
