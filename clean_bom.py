import os
from pathlib import Path

def remove_bom(file_path):
    """Remove BOM from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            content = f.read()
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error cleaning {file_path}: {e}")
        return False

# Clean all Python files in src/opendox
count = 0
for root, dirs, files in os.walk('src/opendox'):
    for file in files:
        if file.endswith('.py'):
            file_path = Path(root) / file
            if remove_bom(file_path):
                count += 1
                print(f"Cleaned: {file_path}")

print(f"\nCleaned {count} files")