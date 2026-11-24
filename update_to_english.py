import subprocess
import os

# List of files to update
files_to_update = [
    'scorch/app.py',
    'scorch/backends/manager.py',
    'scorch/screens/chat.py',
    'scorch/screens/images.py',
    'scorch/screens/settings.py',
    'scorch/screens/base.py',
    'scorch/widgets/panel.py',
    'scorch/widgets/monitor.py',
]

print("Updating code to English...")
for filepath in files_to_update:
    if not os.path.exists(filepath):
        print("Skipping " + filepath + " - not found")
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple replacement for common Portuguese terms
    translations = {
        'Aqui': 'Here',
        'Acima': 'Above',
        'Abaixo': 'Below',
        'Clique': 'Click',
        'Insira': 'Enter',
        'Salve': 'Save',
        'Carregando': 'Loading',
        'Erro': 'Error',
        'Sucesso': 'Success',
        'Confirmar': 'Confirm',
        'Cancelar': 'Cancel',
        'Opções': 'Options',
        'Configurações': 'Settings',
        'Modelos': 'Models',
        'Imagens': 'Images',
        'Chats': 'Chats',
        'Iniciar': 'Start',
        'Parar': 'Stop',
        'Gerar': 'Generate',
        'Excluir': 'Delete',
        'Adicionar': 'Add',
        'Salvar': 'Save',
    }
    
    for pt, en in translations.items():
        content = content.replace(pt, en)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Updated " + filepath)

print("\nCode translation complete!")
