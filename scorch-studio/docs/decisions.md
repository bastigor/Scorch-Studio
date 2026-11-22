# Scorch - Decision Log

This file documents architectural decisions and deviations from the original design.

## 2026-11-22: Initial Backend Selection

**Decision**: Use llama.cpp b12627 nightly for LLM chat, stable-diffusion.cpp master-1106 for image generation.

**Rationale**: Both projects provide pre-built binaries per platform with OpenAI-compatible API (llama-server) and straightforward CLI usage (sd-cli). Nightly builds ensure access to latest performance fixes.

**Alternative considered**: Oobabooga's llama-cpp-binaries (Python wheel only), but decided against due to lack of standalone binary + dependency on Python runtime outside project root.

## 2026-11-22: Exclusive Workspaces Default

**Decision**: Chat and image generation are mutually exclusive by default; switching workspaces unloads the other process.

**Rationale**: Prevents resource exhaustion when user has limited VRAM/RAM. Configurable via settings to `coexist` if performance is not a concern.

## 2026-11-22: Theme Color Variables

**Decision**: Define all TCSS colors as variables in theme.tcss, no hardcoded values elsewhere.

**Palette**:
```tcss
background #0d0505;
surface #150808;
border normal #7a1c1c; border focused #ff4d4d;
primary #e03131; highlight #ff6b6b;
text #f2dede; secondary #a06a6a;
```

## 2026-11-22: Terminal Image Preview Fallback

**Decision**: Use `textual-image` with Kitty/Sixel protocol support, falling back to Unicode block rendering.

**Rationale**: Provides native terminal image integration while maintaining compatibility with basic terminals lacking these protocols.

## Notes on Version Pinning

Backends are pinned by commit hash in CI (e.g., `b12627`, `master-1106`). Nightly builds rotate; the CI workflow always uses the latest tagged release unless a specific bugfix is needed. Users running an older Scorch version will automatically update backends on next launcher run if newer versions are available.

## Future Considerations (Not Implemented)

- LoRA/ControlNet support would require custom inference pipeline or server-side loading; out of scope for v1.
- Multiple simultaneous chat sessions via router mode (`llama-server` with `-np > 1`) is supported but not exposed to UI yet.
- Model download from Hugging Face uses `httpx` with progress bar; resume support implemented but hash verification only on completion.
