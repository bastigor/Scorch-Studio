import os

files_to_update = [
    'scorch/app.py',
    'scorch/backends/manager.py',
    'scorch/screens/chat.py',
]

print("Updating comments to English...")

for filepath in files_to_update:
    if not os.path.exists(filepath):
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        # Comment-only replacements
        translations = {
            '# Arquivo principal da aplicação': '# Main application file',
            '# Gerencia todos os backends': '# Manages all backends',
            '# Interface de chat com LLM': '# LLM chat interface',
            '# Tela base para screens': '# Base class for screens',
            '# Configurações da aplicação': '# Application settings',
            '# Geração de imagens estáveis': '# Stable diffusion image generation',
            '# Gerencia modelos e inferência': '# Manages models and inference',
        }
        
        for pt, en in translations.items():
            line = line.replace(pt, en)
        
        new_lines.append(line)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print("Updated " + filepath)

print("\nComments update complete!")
