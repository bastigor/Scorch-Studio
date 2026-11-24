# Changelog

All notable changes to Scorch-Studio will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-11-24

### Added
- **LLM Chat Interface**: Real-time streaming chat with GGUF model support via llama-server
- **Image Generation**: Stable Diffusion integration with sd-cli for local image generation
- **Model Management**: Model browser and loading interface for managing GGUF files
- **System Monitoring**: Resource usage monitoring (CPU, RAM, GPU) with visual widgets
- **Backend Module Structure**: Organized backend binary management in `scorch/backends/` package
- **Professional Documentation**: Comprehensive README.md with installation and usage guides

### Changed
- **Language**: All code comments, documentation, and UI strings now in English
- **Code Organization**: Reorganized project structure following Python best practices
- **Module Structure**: Created proper packages for `backends/`, `engines/`, `screens/`, `widgets/`
- **Screen Integration**: All screens properly connected to main application (Chat, Images, Settings, Models)
- **CSS Loading**: Theme now loads from `theme.tcss` instead of being disabled

### Fixed
- **app.py Screen Connection**: All screen instances created and connected to application
- **Backend Migration**: Migrated backend code from file to proper module structure (`backends/manager.py`)
- **Import Issues**: Fixed missing imports in base.py, chat.py, and settings.py
- **Decorator Problems**: Removed problematic `@work` decorators causing async issues
- **Widget References**: Corrected widget initialization and access patterns

### Improved
- **Error Handling**: Enhanced error messages and logging throughout the application
- **Code Quality**: Applied consistent formatting and typing standards
- **Documentation**: Added professional README with installation, usage, and architecture guides
- **Dependencies**: Created requirements.txt documenting all Python dependencies

### Technical Details
- Backend binaries organized by platform (windows_cpu, linux_cpu, macos_metal)
- SSE (Server-Sent Events) for streaming LLM responses
- Async/Await patterns for non-blocking backend operations
- Proper package exports via `__init__.py` files

---

## [Unreleased]

### Planned
- Markdown rendering library integration
- Enhanced image gallery with thumbnails
- Model auto-detection improvements
- Resource monitor UI integration
- Configuration validation system
