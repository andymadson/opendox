"""Mock documentation generator for testing."""
from typing import Dict, Any

class MockLLMGenerator:
    """Generate mock documentation for testing."""
    
    def __init__(self, model: str = "mock"):
        self.model = model
    
    def generate(self, prompt: str, max_tokens: int = 200) -> str:
        """Generate mock response."""
        return "This is mock documentation for testing purposes."
    
    def generate_function_doc(self, function_data: Dict[str, Any]) -> str:
        """Generate mock function documentation."""
        name = function_data.get('name', 'unknown')
        args = function_data.get('metadata', {}).get('args', [])
        language = function_data.get('language', 'python')
        
        if language == 'javascript' or language == 'typescript':
            doc = f"""
Processes data and returns a result.

@param {{{', '.join(args) if args else 'void'}}} - Input parameters
@returns {{any}} Processed result
"""
        elif language == 'python':
            doc = f"""
Performs operations on the given inputs.

Args:
    {chr(10).join([f'    {arg}: Input parameter.' for arg in args]) if args else '    None'}

Returns:
    Processed result or None.
"""
        elif language == 'go':
            doc = f"""
// {name} performs the required operation.
// Takes {len(args)} parameters and returns a result.
"""
        else:
            doc = f"""
Function {name} with {len(args)} parameters.
Performs the required operation and returns a result.
"""
        
        return doc.strip()
    
    def clean_response(self, response: str) -> str:
        """Clean up response."""
        return response.strip()