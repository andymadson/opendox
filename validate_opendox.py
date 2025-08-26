from pathlib import Path
from opendox.generators.llm_generator import LLMGenerator
from opendox.core.cache import DocumentationCache
from opendox.core.config_loader import OpendoxConfig

print("Testing LLM Generator...")
gen = LLMGenerator()
test_func = {
    'name': 'test_func',
    'metadata': {'args': ['x', 'y']},
    'docstring': None
}
doc = gen.generate_function_doc(test_func)
print(f"Generated: {doc[:100]}...")
assert '```' not in doc, "Found code blocks in output"
assert 'python' not in doc.lower() or 'python' in doc, "Found standalone 'python'"

print("\nTesting Cache...")
cache = DocumentationCache(Path('.'))
test_file = Path('test.py')
if test_file.exists():
    needs_update = cache.needs_update(test_file)
    print(f"File needs update: {needs_update}")

print("\nTesting Config...")
config = OpendoxConfig()
print(f"Model: {config.config['llm']['model']}")

print("\nAll tests passed!")