# Create init_directories.py
"""Initialize required directories."""
from pathlib import Path

directories = [
    "src/opendox/database",
    "src/opendox/formats",
]

for dir_path in directories:
    Path(dir_path).mkdir(parents=True, exist_ok=True)
    init_file = Path(dir_path) / "__init__.py"
    if not init_file.exists():
        init_file.write_text("")
        print(f"Created {init_file}")

print("Directories initialized!")