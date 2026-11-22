# Scorch UI Strings - Portuguese (pt-BR)

"""Centralized string definitions for all user interface text.
Maintain all translations in this single file to facilitate future localization."""

# Main app strings
APP_NAME = "Scorch"
VERSION = "0.1.0"
APP_DESCRIPTION = "Estúdio de IA local, offline e portátil"

# Screen titles
SCREEN_CHAT_TITLE = "Conversas"
SCREEN_IMAGES_TITLE = "Geração de Imagens"
SCREEN_MODELS_TITLE = "Modelos"
SCREEN_SETTINGS_TITLE = "Configurações"

# Common buttons and actions
BUTTON_NEW_CONVERSATION = "Nova Conversa"
BUTTON_GENERATE = "Gerar"
BUTTON_SAVE = "Salvar"
BUTTON_CANCEL = "Cancelar"
BUTTON_DELETE = "Excluir"
BUTTON_REMOVE = "Remover"
BUTTON_SELECT = "Selecionar"
BUTTON_OPEN = "Abrir no visualizador do sistema"
BUTTON_HELP = "Ajuda (F1)"

# Status messages
STATUS_READY = "Pronto para usar"
STATUS_PROCESSING = "Processando..."
STATUS_ERROR = "Erro"
STATUS_WARN = "Aviso"
STATUS_SUCCESS = "Sucesso"

# Error messages
ERROR_NO_MODEL = "Nenhum modelo instalado. Vá para 'Modelos' e baixe um."
ERROR_BACKEND_NOT_FOUND = f"{backend} não está disponível. Use CPU ou outro backend."
ERROR_DISK_SPACE = "Erro de armazenamento. Verifique espaço disponível em {path}"

# Chat section strings
CHAT_NEW = "Nova conversa"
CHAT_RENAME = "Renomear:"
CHAT_DELETE = "Excluir conversa"
CHAT_INTERRUPT = "Interruptir geração"
CHAT_REGENERATE = "Regenerar última resposta"
CHAT_SYSTEM_PROMPT = "Prompt de sistema:"
CHAT_TOKENS_ESTIMATE = "{tokens} tokens estimados"

# Image generation strings
IMAGE_GENERATING = "Gerando..."
IMAGE_DONE = "Imagem gerada!"
IMAGE_FAILED = "Geração falhou. Verifique os logs."
IMAGE_CANCELLED = "Geração cancelada."
IMAGE_OPEN_OUTPUT = "Abrir saída no visualizador do sistema"

# Model section strings
MODEL_DOWNLOADING = "Baixando..."
MODEL_DOWNLOADED = "Modelo baixado com sucesso!"
MODEL_IMPORTING = "Importando..."
MODEL_INSTALLED = "Instalado"
MODEL_ACTIVE = "Ativo"
MODEL_REMOVE = "Remover modelo"

# Settings section strings
SETTING_GPU_BACKEND = "Backend de GPU:"
SETTING_WORKSPACE_POLICY = "Política de workspaces:"
SETTING_CONTEXT_SIZE = "Tamanho do contexto (tokens):"
SETTING_THREAD_COUNT = "Núcleos de thread:"
SETTING_DATA_DIR = "Diretório de dados:"

# Workspace policy options
WORKSPACE_EXCLUSIVE = "Exclusivo (mutuamente exclusivo)"
WORKSPACE_COEXIST = "Coexistir (permitir ambos simultaneamente)"

# Terminal size warnings
TERMINAL_SMALL = "Terminal muito pequeno"
TERMINAL_MIN_WIDTH = "Mínimo de largura: 60 colunas"
TERMINAL_MIN_HEIGHT = "Mínimo de altura: 18 linhas"

# Shortcuts help text
HELP_SHORTCUTS_TITLE = "Atalhos de Teclado"
SHORTCUTT_SCREEN_1 = "Ctrl+1 - Conversas"
SHORTCUTT_SCREEN_2 = "Ctrl+2 - Imagens"
SHORTCUTT_SCREEN_3 = "Ctrl+3 - Modelos"
SHORTCUTT_SCREEN_4 = "Ctrl+4 - Configurações"
SHORTCUTT_TOGGLE_PANELS = "Ctrl+B - Mostrar/Ocultar painéis laterais"
SHORTCUTT_QUIT = "Ctrl+Q - Encerrar e sair"
HELP_SHORTCUTS_FOOTER = "Pressione F1 para ajuda completa"

# Download progress strings
DOWNLOAD_PROGRESS = "{percent}% ({size} de {total})"
DOWNLOAD_RESUMING = "Retomando..."
DOWNLOAD_VERIFIED = "Verificado: SHA256 OK"
DOWNLOAD_FAILED_HASH = "Falha no hash - arquivo corrompido"

# Hardware monitor strings
HARDWARE_CPU = "CPU"
HARDWARE_RAM = "RAM"
HARDWARE_GPU = "GPU"
HARDWARE_VRAM = "VRAM"
HARDWARE_UNKNOWN = "Desconhecido"

# Model format strings
MODEL_SD_15 = "Stable Diffusion 1.5 (.safetensors/.ckpt)"
MODEL_SDXL = "Stable Diffusion XL (GGUF completo)"
MODEL_LLAMA = "LLM GGUF"
