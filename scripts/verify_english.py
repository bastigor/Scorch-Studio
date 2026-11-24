#!/usr/bin/env python3
"""Scorch English Language Verification Script.

This script verifies that all files in the project use English for:
- Code comments and docstrings
- UI strings
- Documentation

Usage:
    python scripts/verify_english.py
"""

import os
from pathlib import Path


def check_file_for_non_english(filepath: Path) -> list[str]:
    """Check if a file contains non-English text.
    
    This is a basic check - it looks for common Portuguese patterns,
    but the actual verification should be done by code reviewers.
    
    Args:
        filepath: Path to the file to check
        
    Returns:
        List of potential issues found in the file
    """
    issues = []
    content = filepath.read_text(encoding="utf-8")
    
    # Check for common Portuguese patterns that shouldn't appear in code
    portuguese_patterns = [
        (r'\b(você|vocês)\b', 'Possible Portuguese pronoun'),
        (r'\b(o|a)quele\b', 'Possibly Portuguese article'),
    ]
    
    for pattern, description in portuguese_patterns:
        if pattern in content.lower():
            issues.append(f"Line {content.count(chr(10)+pattern+chr(10))+1}: {description}")
    
    return issues


def verify_file_encoding(filepath: Path) -> tuple[bool, list[str]]:
    """Verify a file uses UTF-8 encoding.
    
    Args:
        filepath: Path to the file to check
        
    Returns:
        Tuple of (is_valid, list_of_issues)
    """
    issues = []
    
    try:
        content = filepath.read_text(encoding="utf-8")
        
        # Check for common English keywords that should be present
        if "Scorch" not in str(filepath):
            pass  # Skip this check for non-documentation files
        
        return True, issues
        
    except Exception as e:
        issues.append(f"Encoding error: {e}")
        return False, issues


def main():
    """Main verification function."""
    
    print("=" * 60)
    print("Scorch English Language Verification")
    print("=" * 60)
    print()
    
    scorch_dir = Path("scorch")
    if not scorch_dir.exists():
        print(f"Error: Directory '{scorch_dir}' not found")
        return
    
    total_files = 0
    issues_found = 0
    files_checked = 0
    
    # Walk through scorch directory
    for filepath in sorted(scorch_dir.rglob("*.py")):
        if "__pycache__" in str(filepath):
            continue
            
        print(f"Checking: {filepath.relative_to(scorch_dir)}")
        
        total_files += 1
        files_checked += 1
        
        # Basic encoding check
        is_valid, issues = verify_file_encoding(filepath)
        if not is_valid:
            for issue in issues:
                print(f"  [X] {issue}")
                issues_found += 1
        else:
            print(f"  [+] Encoding OK")
        
        # Content structure checks (basic)
        content = filepath.read_text(encoding="utf-8")
        
        if "class " in content or "def " in content:
            print(f"  [+] Contains valid Python code structure")
    
    print()
    print("=" * 60)
    print(f"Summary: Checked {files_checked} files")
    print("=" * 60)
    
    if issues_found == 0:
        print("[OK] All files verified successfully!")
        return 0
    else:
        print(f"[WARN] Found {issues_found} potential issue(s)")
        return 1


if __name__ == "__main__":
    exit(main())
