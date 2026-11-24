# Scorch UI Strings - English (EN)
"""Centralized string definitions for all user interface text.

All UI text should be in English to ensure consistency across platforms and languages.
Translations can be added here if needed, but the primary language is English."""


# Main app strings
APP_NAME = "Scorch"
VERSION = "0.1.0"
APP_DESCRIPTION = "Local AI studio, offline and portable"

# Screen titles
SCREEN_CHAT_TITLE = "Conversations"
SCREEN_IMAGES_TITLE = "Image Generation"
SCREEN_MODELS_TITLE = "Models"
SCREEN_SETTINGS_TITLE = "Settings"

# Common buttons and actions
BUTTON_NEW_CONVERSATION = "New Conversation"
BUTTON_GENERATE = "Generate"
BUTTON_SAVE = "Save"
BUTTON_CANCEL = "Cancel"
BUTTON_DELETE = "Delete"
BUTTON_REMOVE = "Remove"
BUTTON_SELECT = "Select"
BUTTON_OPEN = "Open in File Explorer"
BUTTON_HELP = "Help (F1)"

# Status messages
STATUS_READY = "Ready to use"
STATUS_PROCESSING = "Processing..."
STATUS_ERROR = "Error"
STATUS_WARN = "Warning"
STATUS_SUCCESS = "Success"

# Error messages
ERROR_NO_MODEL = "No model installed. Go to 'Models' and download one."
ERROR_BACKEND_NOT_FOUND = f"{backend} is not available. Use CPU or another backend."
ERROR_DISK_SPACE = "Disk space error. Check available space at {path}"

# Chat section strings
CHAT_NEW = "New conversation"
CHAT_RENAME = "Rename:"
CHAT_DELETE = "Delete conversation"
CHAT_INTERRUPT = "Interrupt generation"
CHAT_REGENERATE = "Regenerate last response"
CHAT_SYSTEM_PROMPT = "System prompt:"
CHAT_TOKENS_ESTIMATE = "{tokens} tokens estimated"

# Image generation strings
IMAGE_GENERATING = "Generating..."
IMAGE_DONE = "Image generated!"
IMAGE_FAILED = "Generation failed. Check logs."
IMAGE_CANCELLED = "Generation cancelled."
IMAGE_OPEN_OUTPUT = "Open output in File Explorer"

# Model section strings
MODEL_DOWNLOADING = "Downloading..."
MODEL_DOWNLOADED = "Model downloaded successfully!"
MODEL_IMPORTING = "Importing..."
MODEL_INSTALLED = "Installed"
MODEL_ACTIVE = "Active"
MODEL_REMOVE = "Remove model"

# Settings section strings
SETTING_GPU_BACKEND = "GPU Backend:"
SETTING_WORKSPACE_POLICY = "Workspace policy:"
SETTING_CONTEXT_SIZE = "Context size (tokens):"
SETTING_THREAD_COUNT = "Thread count:"
SETTING_DATA_DIR = "Data directory:"

# Workspace policy options
WORKSPACE_EXCLUSIVE = "Exclusive (mutually exclusive)"
WORKSPACE_COEXIST = "Coexist (allow both simultaneously)"

# Terminal size warnings
TERMINAL_SMALL = "Terminal too small"
TERMINAL_MIN_WIDTH = "Minimum width: 60 columns"
TERMINAL_MIN_HEIGHT = "Minimum height: 18 lines"

# Shortcuts help text
HELP_SHORTCUTS_TITLE = "Keyboard Shortcuts"
SHORTCUTT_SCREEN_1 = "Ctrl+1 - Conversations"
SHORTCUTT_SCREEN_2 = "Ctrl+2 - Images"
SHORTCUTT_SCREEN_3 = "Ctrl+3 - Models"
SHORTCUTT_SCREEN_4 = "Ctrl+4 - Settings"
SHORTCUTT_TOGGLE_PANELS = "Ctrl+B - Toggle side panels"
SHORTCUTT_QUIT = "Ctrl+Q - Quit and exit"
HELP_SHORTCUTS_FOOTER = "Press F1 for full help"

# Download progress strings
DOWNLOAD_PROGRESS = "{percent}% ({size} of {total})"
DOWNLOAD_RESUMING = "Resuming..."
DOWNLOAD_VERIFIED = "Verified: SHA256 OK"
DOWNLOAD_FAILED_HASH = "Hash failed - corrupted file"

# Hardware monitor strings
HARDWARE_CPU = "CPU"
HARDWARE_RAM = "RAM"
HARDWARE_GPU = "GPU"
HARDWARE_VRAM = "VRAM"
HARDWARE_UNKNOWN = "Unknown"

# Model format strings
MODEL_SD_15 = "Stable Diffusion 1.5 (.safetensors/.ckpt)"
MODEL_SDXL = "Stable Diffusion XL (GGUF full model)"
MODEL_LLAMA = "LLM GGUF"