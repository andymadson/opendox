# tests/test_parser.py
import pytest
from pathlib import Path
from opendox.parsers.python_parser import PythonParser

def test_parse_function():
    code = '''
def example(a: int, b: str) -> bool:
    """Test function."""
    return True
'''
    parser = PythonParser()
    # Create temp file and test...
    assert len(result['functions']) == 1
    assert result['functions'][0].name == 'example'