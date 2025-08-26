from pathlib import Path
from opendox.core.file_discovery import FileDiscovery
from opendox.parsers.python_parser import PythonParser

# Check file discovery
discovery = FileDiscovery()
repo_path = Path("temp_requests")

if not repo_path.exists():
    print(f"Error: {repo_path} doesn't exist")
    exit()

files = discovery.discover_files(repo_path, max_files=20)
python_files = discovery.filter_python_files(files)

print(f"Found {len(files)} total files")
print(f"Found {len(python_files)} Python files")

if python_files:
    print("\nFirst 5 Python files:")
    for f in python_files[:5]:
        print(f"  - {f}")
    
    # Try parsing one
    parser = PythonParser()
    result = parser.parse_file(python_files[0])
    
    if 'error' in result:
        print(f"\nParser error: {result['error']}")
    else:
        print(f"\nParsed {python_files[0].name}:")
        print(f"  Functions: {len(result.get('functions', []))}")
        print(f"  Classes: {len(result.get('classes', []))}")