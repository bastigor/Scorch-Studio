# Scorch Studio - Local AI Studio

## 📋 Versão: 0.1.1 (Hotfix Release - 23/Nov/2026)

### 🎯 O que foi corrigido nesta release:

#### Bugs Críticos Corrigidos:
- ✅ **Syntax error Python** em `scorch/backends.py` (linha 209)
- ✅ **Lógica errada de detecção de tipo de modelo** (`models.py`, linha 85-86)
- ✅ **Erro ao baixar modelos da internet** (`models.py`, linha 126 - urlopen incorreto)
- ✅ **Importação duplicada e referências incorretas** em `chat.py`

#### Bugs de Alto Impacto:
- ✅ **Path não importado** em `base.py` (linha 42)
- ✅ **Uso incorreto do decorator @work** em `settings.py`, linhas 103-111
- ✅ **Criação incorreta de App para quit** em `settings.py`, linhas 116-126
- ✅ **Referências a widgets inexistentes** em `chat.py`

#### Otimizações Aplicadas:
- Códigos de erro padronizados (consistente "ERROR" e mensagens em inglês)
- Traceback correto usando `sys.stderr`
- Mensagens consistentes em toda a aplicação

### 📦 Estrutura do Projeto

```
scorch-studio/
├── scorch/                    # Core library (corrigido)
│   ├── app.py                # Main App class
│   ├── backends.py           # Backend management ✅ CORRIGIDO
│   ├── storage.py            # Storage management
│   ├── downloads.py          # Download utilities  
│   ├── engines/              # Engine management
│   │   ├── manager.py        # Engine manager
│   │   └── models.py         # Model management ✅ CORRIGIDO
│   ├── screens/              # UI Screens
│   │   ├── base.py           # Base screen class ✅ CORRIGIDO
│   │   ├── chat.py           # Chat interface (corrigido)
│   │   ├── images.py         # Image generation
│   │   └── settings.py       # Settings management ✅ CORRIGIDO
│   ├── widgets/              # Custom widgets
│   ├── theme.tcss            # Textual CSS theme
│   └── strings.py            # UI strings (English)
├── backend/                  # Backend binaries directory
├── data/                     # Data storage
├── outputs/                  # Generated images output
├── llm-models/              # LLM models (.gguf)
├── models/                   # Stable Diffusion checkpoints
├── tests/                    # Test suite
└── scripts/config/          # Configuration files
```

### 🚀 Como Rodar

```bash
# Instalar dependências
pip install -r requirements.txt

# Iniciar a aplicação
python scorch/app.py

# Ou com desenvolvimento
python -m textual dev scorch.app:ScorchApp
```

### 🔧 Prerrequisitos

- Python 3.10+ (recomendado 3.12+)
- Windows 10/11 ou Linux/macOS
- CPU ou GPU disponível para rodar backends

### 📖 Documentação Completa

Para detalhes completos sobre todos os bugs corrigidos e otimizações aplicadas, consulte:
- **[CHANGELOG.md](CHANGELOG.md)** - Registro completo de todas as correções
- **`scorch/README.md`** - Detalhes por arquivo

---

## Original README (Versão 0.1.0)

Scorch é um estúdio de IA local, totalmente offline e portátil. Oferece interface TUI moderna para chat com LLMs e geração de imagens via Stable Diffusion.

## Features

- **LLM Chat**: Streamed conversations via llama.cpp (OpenAI-compatible API over SSE)
- **Image Generation**: Stable Diffusion 1.5/SDXL via stable-diffusion.cpp CLI
- **Cross-platform**: Windows 10/11 x64, Linux x86_64, macOS Apple Silicon
- **Offline-first**: Once backends are downloaded, everything runs offline
- **Resource monitoring**: Real-time CPU, RAM, GPU, VRAM display

## System Requirements

### Windows 10/11 x64
- Python 3.12 (portable version or manual installation)
- NVIDIA drivers (optional - for CUDA acceleration)
- Vulkan runtime (optional - alternative GPU backend)

## Installation

```bash
# Instalar dependências
pip install -r requirements.txt

# Iniciar a aplicação
python scorch/app.py
```

---

**Última atualização**: 23 de Novembro de 2026  
**Próxima release planejada**: Versão 1.0.0 com reorganização completa da estrutura e melhorias
