import subprocess
import os

print("=" * 60)
print("GIT COMMIT AND PUSH TO GITHUB")
print("=" * 60)

# Change to project directory
os.chdir(r'C:\Users\João Pedro\Documents\projetos\scorch-studio')

# Check git status
print("\n1. Checking git status...")
result = subprocess.run(['git', 'status'], capture_output=True, text=True)
print(result.stdout if result.returncode == 0 else f"Error: {result.stderr}")

# List files that will be committed
files_to_commit = [
    'scorch/app.py',
    'scorch/screens/base.py', 
    'scorch/screens/chat.py',
    'scorch/screens/settings.py',
    'scorch/backends/__init__.py',
    'scorch/backends/manager.py',
    '.gitignore'
]

print("\n2. Files to commit:")
for f in files_to_commit:
    if os.path.exists(f):
        size = os.path.getsize(f)
        print("  OK " + f + " (" + str(size) + " bytes)")
    else:
        print("  X " + f + " - NOT FOUND")

# Check for existing .gitignore
if not os.path.exists('.gitignore'):
    print("\n3. Creating .gitignore...")
    gitignore_content = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scorch specific
backend/
models/
outputs/
*.tcss.cache

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
"""
    with open('.gitignore', 'w', encoding='utf-8') as f:
        f.write(gitignore_content)
    print("  Created .gitignore")

# Stage the files
print("\n3. Staging files for commit...")
result = subprocess.run(['git', 'add', '-A'], capture_output=True, text=True)
print("Exit code: " + str(result.returncode))

# Commit with message
print("\n4. Committing changes...")
commit_message = """feat: Bug fixes and structural reorganization

- Fixed app.py: Connected all screens to main application
  - CSS now loads from theme.tcss
  - ChatScreen, ImagesScreen, SettingsScreen, ModelsScreen instances created
  - Screens properly connected and accessible
  
- Created backends/ module structure (NEW)
  - Migrated backend code from scorch/backends.py to scorch/backends/manager.py
  - Proper package organization with __init__.py exports
  - Better separation of concerns
  
- Fixed remaining bugs:
  - screens/base.py: Removed unused import
  - screens/chat.py: Fixed @work decorator and widget references
  - screens/settings.py: Added missing Binding import, fixed decorators

Improvements:
- Consistent module structure across project
- Proper async/await patterns
- All imports now correct
- Code follows Python best practices"""

result = subprocess.run(['git', 'commit', '-m', commit_message], capture_output=True, text=True)
print(result.stdout if result.returncode == 0 else "Error: " + result.stderr[:200])

# Try to push to GitHub
print("\n5. Attempting to push to GitHub...")
try:
    # Get remote URL
    result = subprocess.run(['git', 'remote', 'get-url', 'origin'], capture_output=True, text=True)
    remote_url = result.stdout.strip()
    print("Remote URL: " + remote_url)
    
    # Push to origin
    result = subprocess.run(['git', 'push', '-u', 'origin', 'main'], capture_output=True, text=True)
    if result.returncode == 0:
        print("SUCCESS! Changes pushed to GitHub main branch")
        print(result.stdout)
    else:
        print("Push failed (may need authentication): " + result.stderr[:200])
        
except Exception as e:
    print("Error during push setup: " + str(e))

print("\n" + "=" * 60)
print("GIT OPERATIONS COMPLETE")
print("=" * 60)
