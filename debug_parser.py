from pathlib import Path
from opendox.parsers.python_parser import PythonParser

test_file = Path('src/opendox/parsers/python_parser.py')
print(f"File exists: {test_file.exists()}")

parser = PythonParser()
result = parser.parse_file(test_file)

print(f"Result keys: {result.keys()}")
if 'error' in result:
    print(f"Error: {result['error']}")
else:
    print(f"Functions found: {len(result.get('functions', []))}")