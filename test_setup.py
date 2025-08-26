#!/usr/bin/env python3
"""Test script to verify OPENDOX setup."""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    try:
        import opendox
        print(f"✓ OPENDOX version: {opendox.__version__}")
        
        from opendox.cli import app
        print("✓ CLI module imported")
        
        from opendox.core.config import settings
        print("✓ Config module imported")
        
        from opendox.parsers.python_parser import PythonParser
        print("✓ Python parser imported")
        
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_parser():
    """Test the Python parser with a sample file."""
    print("\nTesting Python parser...")
    from opendox.parsers.python_parser import PythonParser
    
    # Create a test file
    test_code = '''
def hello_world(name: str) -> str:
    """Say hello to someone."""
    return f"Hello, {name}!"

class Greeter:
    """A class that greets people."""
    
    def __init__(self, greeting: str = "Hello"):
        self.greeting = greeting
    
    def greet(self, name: str) -> str:
        return f"{self.greeting}, {name}!"
'''
    
    # Save test file
    test_file = Path("test_sample.py")
    test_file.write_text(test_code)
    
    try:
        parser = PythonParser()
        result = parser.parse_file(test_file)
        
        print(f"✓ Found {len(result['functions'])} functions")
        print(f"✓ Found {len(result['classes'])} classes")
        
        for func in result['functions']:
            print(f"  - Function: {func.name} (line {func.line_start})")
        
        for cls in result['classes']:
            print(f"  - Class: {cls.name} with {len(cls.metadata['methods'])} methods")
        
        return True
    except Exception as e:
        print(f"✗ Parser error: {e}")
        return False
    finally:
        # Clean up test file
        if test_file.exists():
            test_file.unlink()

def test_cli():
    """Test CLI functionality."""
    print("\nTesting CLI...")
    import subprocess
    
    result = subprocess.run(
        [sys.executable, "-m", "opendox.cli", "--help"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✓ CLI help command works")
        return True
    else:
        print(f"✗ CLI error: {result.stderr}")
        return False

def main():
    """Run all tests."""
    print("=" * 50)
    print("OPENDOX Setup Test")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_parser,
        test_cli,
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"✗ Test failed with error: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    if all(results):
        print("✅ All tests passed! OPENDOX is ready to use.")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
