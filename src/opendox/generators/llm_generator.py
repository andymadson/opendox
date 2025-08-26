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
        """Generate or enhance documentation."""
        existing_doc = function_data.get('docstring', '')
        
        if existing_doc and len(existing_doc) > 50:  # Has substantial docs
            return self.enhance_docstring(function_data, existing_doc)
        else:
            return self.generate_new_docstring(function_data)
    
    def enhance_docstring(self, function_data: Dict[str, Any], existing: str) -> str:
        """Add missing sections to existing docstring."""
        prompt = f"""The function '{function_data['name']}' has this docstring:
{existing}

Add any missing sections (Args, Returns, Raises, Examples) if needed.
Keep the original description. Only add what's missing."""
        
        response = self.generate(prompt, max_tokens=150)
        return self.clean_response(response)
    
    def generate_new_docstring(self, function_data: Dict[str, Any]) -> str:
        """Generate new docstring for undocumented function."""
        name = function_data.get('name', 'unknown')
        args = function_data.get('metadata', {}).get('args', [])
        
        # Concise prompt for better output
        prompt = f"""Write a concise Python docstring for function '{name}' with parameters {args}.
Maximum 3 sentences for description.

Use this exact format:
One-line description of what the function does.

Args:
    parameter_name: Brief description of parameter.

Returns:
    Brief description of return value.

Generate the docstring content only (no function definition, no triple quotes):"""
        
        response = self.generate(prompt, max_tokens=200)
        return self.clean_response(response)
    
    def clean_response(self, response: str) -> str:
        """Clean up LLM response to remove unwanted formatting."""
        # Remove code blocks
        response = response.replace('```python', '')
        response = response.replace('```', '')
        
        # Remove triple quotes
        response = response.replace('"""', '')
        response = response.replace("'''", '')
        
        # Remove function definitions if accidentally included
        if 'def ' in response:
            response = response.split('def ')[0]
        
        # Remove standalone "python" lines
        lines = response.split('\n')
        cleaned_lines = [line for line in lines if line.strip().lower() != 'python']
        
        # Remove excessive blank lines
        final_lines = []
        prev_blank = False
        for line in cleaned_lines:
            is_blank = len(line.strip()) == 0
            if not (is_blank and prev_blank):
                final_lines.append(line)
            prev_blank = is_blank
        
        return '\n'.join(final_lines).strip()