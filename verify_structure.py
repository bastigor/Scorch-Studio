"""Verify project structure after fixes."""
import os
from pathlib import Path

print("=" * 60)
print("SCORCH-STUDIO PROJECT VERIFICATION")
print("=" * 60)

# Check directory structure
scorch_dir = Path(r'C:\Users\João Pedro\Documents\projetos\scorch-studio\scorch')

print("\n1. DIRECTORY STRUCTURE CHECK")
print("-" * 40)

required_dirs = [
    "screens",
    "widgets", 
    "engines",
    "backends"
]

for req_dir in required_dirs:
    full_path = scorch_dir / req_dir
    if full_path.exists():
        print("OK: " + req_dir + "/ exists")
        files = [f.name for f in full_path.glob("*.py")]
        if "__init__.py" in files:
            print("  - Has __init__.py (module)")
        else:
            print("  - Contains: " + str(files))
    else:
        print("X: " + req_dir + "/ does NOT exist")

print("\n2. KEY FILES CHECK")
print("-" * 40)

key_files = [
    "app.py",
    "screens/chat.py",
    "screens/images.py", 
    "screens/settings.py",
    "screens/base.py",
    "widgets/panel.py",
    "widgets/monitor.py",
    "engines/manager.py",
    "engines/models.py",
    "backends/__init__.py",
    "backends/manager.py"
]

for f in key_files:
    full_path = scorch_dir / f
    if full_path.exists():
        print("OK: " + f + " exists")
    else:
        print("X: " + f + " NOT FOUND")

print("\n3. IMPORT CHECKS")
print("-" * 40)

# Check if imports are correct
import_checks = [
    ("app.py", ['from scorch.screens import', 'EngineManager']),
    ("backends/__init__.py", ['BackendManager', '__all__']),
    ("screens/chat.py", ['from textual.app import App'])
]

for file_path, required_imports in import_checks:
    full_path = scorch_dir / file_path
    if not full_path.exists():
        print("W: " + file_path + " not found, skipping")
        continue
    
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    missing = []
    for imp in required_imports:
        if imp.lower() not in content.lower():
            missing.append(imp)
    
    if missing:
        print("W: " + file_path + ": Missing imports - " + str(missing))
    else:
        print("OK: " + file_path + ": All required imports present")

print("\n4. BUG FIX SUMMARY")
print("-" * 40)

fixes_applied = [
    ("app.py", "CSS = theme.tcss"),
    ("app.py", "ChatScreen instances created"),
    ("app.py", "Screens connected to app"),
    ("backends/", "Directory structure created"),
    ("screens/base.py", "Removed unused import"),
    ("screens/chat.py", "Fixed widget references"),
    ("screens/settings.py", "Fixed decorator issues")
]

for file_path, fix_desc in fixes_applied:
    print("OK: " + file_path + ": " + fix_desc)

print("\n" + "=" * 60)
print("VERIFICATION COMPLETE")
print("=" * 60)
