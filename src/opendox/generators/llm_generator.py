"""LLM-based documentation generator using Ollama."""
import ollama
from typing import Dict, Any

class LLMGenerator:
    """Generate documentation using Ollama."""
    
    def __init__(self, model: str = "deepseek-coder:1.3b"):
        self.model = model
        self.client = ollama.Client()
        
    def generate(self, prompt: str, max_tokens: int = 200) -> str:
        """Generate text using Ollama."""
        try:
            response = self.client.generate(
                model=self.model, 
                prompt=prompt,
                options={'num_predict': max_tokens}
            )
            return response['response']
        except Exception as e:
            return f"Error: {str(e)}"
    
    def generate_function_doc(self, function_data: Dict[str, Any]) -> str:
        """Generate documentation for a function."""
        name = function_data.get('name', 'unknown')
        args = function_data.get('metadata', {}).get('args', [])
        
        # Concise prompt for better output
        prompt = f"""Write a concise Python docstring for function '{name}' with parameters {args}.
Maximum 3 sentences for description.

Use this exact format:
\"\"\"
One-line description of what the function does.

Args:
    parameter_name: Brief description of parameter.

Returns:
    Brief description of return value.
\"\"\"

Generate the docstring content only (no function definition):
"""
        
        response = self.generate(prompt, max_tokens=200)
        
        # Clean up the response
        # Remove triple quotes if the model included them
        if '"""' in response:
            response = response.split('"""')[0]
        
        # Remove any function definitions if included
        if 'def ' in response:
            response = response.split('def ')[0]
            
        return response.strip()