# Scorch - Portable AI Studio TUI

"""
Scorch is an offline-first, portable terminal UI for local LLM chat and image generation.

No telemetry. No global installation. All runtime, backends, and dependencies
download into the project folder on first launch.

Features:
- Chat with streamed LLM responses (llama.cpp via llama-server)
- Image generation with Stable Diffusion (stable-diffusion.cpp via sd-cli)
- Cross-platform: Windows 10/11 x64, Linux x86_64, macOS Apple Silicon
- Exclusive workspace policy by default to prevent resource exhaustion

Usage:
    # On Windows: Run windows.bat from project root
    # On Linux: ./linux.sh --backend cuda --reset
    # On macOS:  ./mac.sh --backend metal --reset
    
    All backends are downloaded and verified on first launch.
"""

__version__ = "0.1.0"
