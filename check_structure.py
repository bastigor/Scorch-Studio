import subprocess
import os

print("Checking current directory structure...")
scorch_dir = r'C:\Users\João Pedro\Documents\projetos\scorch-studio\scorch'

if not os.path.exists(scorch_dir):
    print(f"ERROR: {scorch_dir} does not exist!")
    exit(1)

# Get current structure
result = subprocess.run(['git', 'status'], shell=True, cwd=scorch_dir, capture_output=True, text=True)
print(result.stdout)

# List all Python files
print("\nCurrent Python files in scorch/:")
for root, dirs, files in os.walk(scorch_dir):
    level = root.replace(scorch_dir, '').count(os.sep)
    indent = ' ' * 2 * level
    print(f"{indent}{os.path.basename(root)}/")
    subindent = ' ' * 2 * (level + 1)
    for file in files:
        if file.endswith('.py'):
            print(f"{subindent}{file}")
