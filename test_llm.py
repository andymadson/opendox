from pathlib import Path
from opendox.parsers.python_parser import PythonParser
from opendox.generators.llm_generator import LLMGenerator

test_file = Path('test_sample.py')  # Changed to simpler file
parser = PythonParser()
result = parser.parse_file(test_file)

if 'error' in result:
    print(f"Parser error: {result['error']}")
    exit(1)

if result.get('functions'):
    func = result['functions'][0]
    print(f'Generating docs for: {func.name}')
    
    generator = LLMGenerator()
    doc = generator.generate_function_doc(func.__dict__)
    
    print('\nGenerated documentation:')
    print(doc)
else:
    print("No functions found")
