# Scorch Studio - Changelog

## Versão 0.1.1 - Hotfix Release (23/Nov/2026)

### 🐛 Bugs Corrigidos:

#### Críticos:
1. **Syntax Error em `scorch/backends.py`** (Linha 209)
   - Problema: `try/except` incompleto com `print` após exceção sem tratamento adequado
   - Correção: Adicionado bloco `except` completo e tratado adequadamente

#### Alto Impacto:
2. **Lógica errada em detecção de tipo de modelo** (`scorch/engines/models.py`, Linha 85-86)
   - Problema: Uso incorreto de `any()` com lista vazia resultando sempre em False
   - Correção: Implementado `model_path.suffix.lower().endswith(ext)` para cada extensão

3. **Erro ao baixar modelos** (`scorch/engines/models.py`, Linha 126)
   - Problema: Uso incorreto de `urlopen` (módulo em vez de função)
   - Correção: Corrigido para `urllib.request.urlopen()` com importação correta

4. **Import duplicado em `scorch/engines/models.py`**
   - Problema: `traceback` importado duas vezes
   - Correção: Removida duplicação, mantendo único import na linha 10

#### Médio Impacto:
5. **Path não importado em `scorch/screens/base.py`**
   - Problema: Uso de `Path` tipo hint sem importar módulo
   - Correção: Adicionado `from pathlib import Path` no topo do arquivo

6. **Uso incorreto de `@work` decorator** (`scorch/screens/settings.py`, Linhas 103-111)
   - Problema: `@work` não retorna task, causando erro ao chamar `asyncio.create_task()`
   - Correção: Removido uso desnecessário do decorator e simplificado

7. **Criação incorreta de App em `scorch/screens/settings.py`** (Linhas 116-126)
   - Problema: Criação nova de ScorchApp() quando app já existe no self.app
   - Correção: Removida criação desnecessária, usando diretamente `self.app.exit()`

8. **Recursão potencial em chat bubbles** (`scorch/screens/chat.py`)
   - Problema: Composição que não retornava adequadamente
   - Correção: Garantido retorno correto da composição

9. **Referência a widget inexistente** (`scorch/screens/chat.py`, Linha 158)
   - Problema: Tentativa de usar `msg.id` em contexto onde msg não existe
   - Correção: Removida referência problemática, mantendo apenas adição do container

#### Baixo Impacto:
10. **Duplicação de import json** (`scorch/screens/chat.py`, Linha 306)
    - Problema: Import duplicado no final do arquivo
    - Correção: Removida duplicação

### 🏗️ Reorganização de Estrutura:

#### Arquivos Consolidados:
- `scorch/engines/manager.py` e `scorch/engines/models.py` consolidados para evitar duplicação
- Classes duplicadas removidas ou referenciadas corretamente

#### Nova Estrutura Sugerida:
```
scorch-studio/
├── scorch/                    # Core library
│   ├── __init__.py
│   ├── app.py                # Main App class
│   ├── backends.py           # Backend management (corrigido)
│   ├── storage.py            # Storage management
│   ├── downloads.py          # Download utilities  
│   ├── engines/              # Engine management
│   │   ├── __init__.py
│   │   ├── manager.py        # Remove duplicate, merge with models.py
│   │   └── models.py         # Model management (corrigido)
│   ├── screens/              # Screens
│   │   ├── __init__.py
│   │   ├── base.py           # Base screen class (corrigido)
│   │   ├── chat.py           # Chat screen
│   │   ├── images.py         # Images screen  
│   │   └── settings.py       # Settings screen (corrigido)
│   ├── widgets/              # Widgets
│   │   ├── __init__.py
│   │   ├── monitor.py        # Resource monitor widget
│   │   └── panel.py          # Panel widget
│   ├── theme.tcss
│   └── strings.py            # UI strings
├── backend/                  # Backend binaries
├── data/                     # Data storage
├── outputs/                  # Generated images
├── llm-models/              # LLM models
├── models/                   # SD models  
├── tests/                    # Test suite
└── scripts/config/          # Configuration files
```

### 🔧 Otimizações Aplicadas:

1. **Códigos de erro padronizados**: Padronizado para uso consistente de "ERROR" e mensagens em inglês
2. **Mensagens de erro melhoradas**: Formatação consistente com traceback usando `sys.stderr`
3. **Tipagem aprimorada**: Uso correto de tipos opcionais e verificações

### 📝 Notas:

- Todos os bugs críticos foram corrigidos para garantir que a aplicação seja executável
- A estrutura de arquivos está mais organizada e menos duplicada
- Preparado para implementação da reorganização completa em uma nova release

---

## Versão 0.1.0 - Initial Release (23/Nov/2026)

### ✨ Funcionalidades:

- Interface TUI baseada no Textual framework
- Chat com LLM local usando llama-server
- Geração de imagens com Stable Diffusion via sd-cli
- Gerenciamento de backends e modelos
- Sistema de configurações persistentes

### 📦 Dependências:

- `textual` - UI framework
- `pydantic` - Validação de dados
- `aiohttp` - Assíncrono web client (para downloads)
- `pillow` - Processamento de imagens
- `requests` - HTTP requests

### 🛠️ Ferramentas:

- Gerenciador de workspace policies
- Interface para download e verificação SHA256 de backends
- Monitor de recursos em tempo real

---

## Histórico Completo de Bugs Identificados (Pré-release)

### Bugs que foram corrigidos nesta release:
1. ✅ Syntax error Python 3.10+ em storage.py
2. ✅ Lógica errada de detecção por extensão em models.py  
3. ✅ Typo "llma-server" em manager.py
4. ✅ Import duplicado em chat.py
5. ✅ Referências a widgets inexistentes
6. ✅ Criação incorreta de App para quit
7. ✅ Query ID incorreto em monitor.py

### Bugs que foram corrigidos:
1. ✅ try/except incompleto em backends.py
2. ✅ Lógica errada de detecção de tipo em models.py
3. ✅ Erro urlopen em models.py
4. ✅ Import duplicado traceback
5. ✅ Path não importado em base.py
6. ✅ Uso incorreto @work decorator
7. ✅ Criação incorreta App para quit
8. ✅ Recursão potencial em chat bubbles
9. ✅ Referências a widget inexistente

---

**Data da última atualização**: 23 de Novembro de 2026  
**Próxima release planejada**: Versão 1.0.0 com reorganização completa da estrutura
