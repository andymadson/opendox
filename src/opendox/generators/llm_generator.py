"""LLM-based documentation generator using Ollama."""
import ollama
from typing import Dict, Any
import time
from rich.console import Console

console = Console()

class LLMGenerator:
    """Generate documentation using Ollama."""
    
    def __init__(self, model: str = "deepseek-coder:1.3b"):
        self.model = model
        self.client = ollama.Client()
        # Test connection on init
        try:
            self.client.list()
            console.print(f"[green]✓ Connected to Ollama with model: {model}[/green]")
        except Exception as e:
            console.print(f"[yellow]⚠ Ollama connection issue: {e}[/yellow]")
            console.print("[yellow]  Make sure Ollama is running: 'ollama serve'[/yellow]")
            console.print(f"[yellow]  Make sure model is installed: 'ollama pull {model}'[/yellow]")
    
    def generate(self, prompt: str, max_tokens: int = 500) -> str:
        """Generate text using Ollama with retry logic."""
        for attempt in range(3):
            try:
                response = self.client.generate(
                    model=self.model, 
                    prompt=prompt,
                    options={
                        'num_predict': max_tokens,
                        'temperature': 0.7,
                        'top_p': 0.9
                    }
                )
                return response['response']
            except Exception as e:
                if attempt == 2:
                    console.print(f"[red]✗ LLM generation failed after 3 attempts: {e}[/red]")
                    return self._fallback_documentation()
                time.sleep(1)
        return self._fallback_documentation()
    
    def generate_function_doc(self, function_data: Dict[str, Any]) -> str:
        """Generate comprehensive documentation for a function."""
        name = function_data.get('name', 'unknown')
        args = function_data.get('metadata', {}).get('args', [])
        returns = function_data.get('metadata', {}).get('returns', 'None')
        existing_doc = function_data.get('docstring', '')
        
        # If there's already a good docstring, enhance it
        if existing_doc and len(existing_doc) > 50:
            return self.enhance_docstring(function_data, existing_doc)
        
        # Otherwise generate new documentation
        # Build a detailed prompt with the actual function signature
        prompt = f"""You are a technical documentation expert. Generate comprehensive documentation for this Python function.

Function Name: {name}
Parameters: {', '.join(args) if args else 'None'}
Return Type: {returns if returns else 'None'}

Generate documentation that includes:
1. A clear one-line description of what the function does
2. Detailed explanation of the purpose and behavior
3. Description of each parameter (name, expected type, purpose)
4. Description of the return value
5. Any important notes about usage or side effects

Format the response as follows:
DESCRIPTION: [One clear sentence about what this function does]

DETAILS: [2-3 sentences explaining how it works and when to use it]

PARAMETERS:
- parameter_name: [type] Description of what this parameter does

RETURNS:
[type] Description of what is returned

USAGE NOTES:
Any important information about using this function

Based on the function name '{name}', generate helpful documentation:"""
        
        response = self.generate(prompt, max_tokens=500)
        
        if not response or response == self._fallback_documentation():
            # If LLM fails, create basic documentation from available info
            return self._create_basic_documentation(function_data)
        
        return self.format_llm_response(response, function_data)
    
    def enhance_docstring(self, function_data: Dict[str, Any], existing: str) -> str:
        """Enhance an existing docstring with additional details."""
        name = function_data.get('name', 'unknown')
        args = function_data.get('metadata', {}).get('args', [])
        
        prompt = f"""Enhance this existing Python docstring with more detail and proper formatting.

Function: {name}
Parameters: {', '.join(args)}
Current Documentation:
{existing}

Improve this documentation by:
1. Adding parameter type hints and descriptions if missing
2. Adding return value description if missing  
3. Adding usage examples if helpful
4. Ensuring clear, professional language
5. Keeping the original intent but making it more comprehensive

Return ONLY the enhanced documentation text, no code or quotes:"""
        
        response = self.generate(prompt, max_tokens=400)
        
        if not response or len(response) < len(existing):
            return existing
        
        return self.clean_response(response)
    
    def format_llm_response(self, response: str, function_data: Dict[str, Any]) -> str:
        """Format the LLM response into proper documentation."""
        # Parse the structured response
        lines = response.strip().split('\n')
        formatted = []
        
        # Try to extract sections from the response
        description = ""
        details = ""
        parameters = []
        returns = ""
        notes = ""
        
        current_section = None
        for line in lines:
            line = line.strip()
            if line.startswith('DESCRIPTION:'):
                description = line.replace('DESCRIPTION:', '').strip()
            elif line.startswith('DETAILS:'):
                current_section = 'details'
                details = line.replace('DETAILS:', '').strip()
            elif line.startswith('PARAMETERS:'):
                current_section = 'parameters'
            elif line.startswith('RETURNS:'):
                current_section = 'returns'
                returns = line.replace('RETURNS:', '').strip()
            elif line.startswith('USAGE NOTES:') or line.startswith('NOTES:'):
                current_section = 'notes'
                notes = line.replace('USAGE NOTES:', '').replace('NOTES:', '').strip()
            elif current_section == 'parameters' and line.startswith('-'):
                parameters.append(line)
            elif current_section == 'details' and line:
                details += " " + line
            elif current_section == 'returns' and line:
                returns += " " + line
            elif current_section == 'notes' and line:
                notes += " " + line
        
        # Build the formatted documentation
        if description:
            formatted.append(description)
        elif function_data.get('name'):
            # Generate a basic description from the function name
            formatted.append(self._generate_description_from_name(function_data['name']))
        
        if details:
            formatted.append("\n" + details)
        
        if parameters:
            formatted.append("\nArgs:")
            for param in parameters:
                formatted.append("    " + param.strip('- '))
        elif function_data.get('metadata', {}).get('args'):
            formatted.append("\nArgs:")
            for arg in function_data['metadata']['args']:
                formatted.append(f"    {arg}: Parameter for {function_data.get('name', 'function')}")
        
        if returns:
            formatted.append("\nReturns:")
            formatted.append("    " + returns)
        elif function_data.get('metadata', {}).get('returns'):
            formatted.append("\nReturns:")
            formatted.append(f"    {function_data['metadata']['returns']}: The result of the operation")
        
        if notes:
            formatted.append("\nNotes:")
            formatted.append("    " + notes)
        
        result = '\n'.join(formatted)
        
        # If we still have no meaningful content, create basic documentation
        if len(result) < 20:
            return self._create_basic_documentation(function_data)
        
        return result
    
    def _create_basic_documentation(self, function_data: Dict[str, Any]) -> str:
        """Create basic documentation when LLM fails."""
        name = function_data.get('name', 'unknown')
        args = function_data.get('metadata', {}).get('args', [])
        returns = function_data.get('metadata', {}).get('returns', None)
        existing_doc = function_data.get('docstring', '')
        
        # If there's an existing docstring, use it
        if existing_doc:
            return existing_doc
        
        # Generate description from function name
        description = self._generate_description_from_name(name)
        
        doc_parts = [description]
        
        if args:
            doc_parts.append("\nArgs:")
            for arg in args:
                # Try to infer parameter purpose from name
                param_desc = self._infer_parameter_description(arg)
                doc_parts.append(f"    {arg}: {param_desc}")
        
        if returns and returns != 'None':
            doc_parts.append("\nReturns:")
            doc_parts.append(f"    {returns}: The result of the {name} operation")
        
        return '\n'.join(doc_parts)
    
    def _generate_description_from_name(self, name: str) -> str:
        """Generate a description based on function name patterns."""
        name_lower = name.lower()
        
        # Common patterns
        if name_lower.startswith('get_'):
            return f"Retrieves and returns {name[4:].replace('_', ' ')}"
        elif name_lower.startswith('set_'):
            return f"Sets or updates {name[4:].replace('_', ' ')}"
        elif name_lower.startswith('create_'):
            return f"Creates a new {name[7:].replace('_', ' ')}"
        elif name_lower.startswith('delete_') or name_lower.startswith('remove_'):
            return f"Removes {name[7:].replace('_', ' ') if name_lower.startswith('delete_') else name[7:].replace('_', ' ')}"
        elif name_lower.startswith('update_'):
            return f"Updates existing {name[7:].replace('_', ' ')}"
        elif name_lower.startswith('is_'):
            return f"Checks if {name[3:].replace('_', ' ')}"
        elif name_lower.startswith('has_'):
            return f"Determines if {name[4:].replace('_', ' ')} exists"
        elif name_lower.startswith('add_'):
            return f"Adds {name[4:].replace('_', ' ')} to the collection"
        elif name_lower.startswith('find_'):
            return f"Searches for and returns {name[5:].replace('_', ' ')}"
        elif name_lower.startswith('parse_'):
            return f"Parses {name[6:].replace('_', ' ')} and returns structured data"
        elif name_lower.startswith('validate_'):
            return f"Validates {name[9:].replace('_', ' ')} according to rules"
        elif name_lower.startswith('process_'):
            return f"Processes {name[8:].replace('_', ' ')} and returns results"
        elif name_lower.startswith('generate_'):
            return f"Generates {name[9:].replace('_', ' ')} based on input"
        elif name_lower == '__init__':
            return "Initializes a new instance of the class"
        elif name_lower == '__str__':
            return "Returns a string representation of the object"
        elif name_lower == '__repr__':
            return "Returns a detailed string representation for debugging"
        else:
            # Generic description
            return f"Performs {name.replace('_', ' ')} operation"
    
    def _infer_parameter_description(self, param_name: str) -> str:
        """Infer parameter description from its name."""
        param_lower = param_name.lower()
        
        # Common parameter patterns
        if param_lower in ['self', 'cls']:
            return "Reference to the instance or class"
        elif param_lower in ['name', 'title', 'label']:
            return "The name or identifier"
        elif param_lower in ['path', 'file_path', 'filepath']:
            return "Path to the file or directory"
        elif param_lower in ['data', 'content', 'body']:
            return "The data to process"
        elif param_lower in ['config', 'settings', 'options']:
            return "Configuration options"
        elif param_lower in ['id', 'uid', 'identifier']:
            return "Unique identifier"
        elif param_lower in ['value', 'val']:
            return "The value to set or process"
        elif param_lower in ['index', 'idx', 'i']:
            return "Index position"
        elif param_lower in ['count', 'num', 'number']:
            return "Number of items"
        elif param_lower in ['message', 'msg']:
            return "Message content"
        elif param_lower in ['error', 'err', 'exception']:
            return "Error or exception information"
        elif param_lower in ['callback', 'handler', 'func']:
            return "Function to call"
        elif param_lower in ['timeout', 'duration', 'interval']:
            return "Time duration in seconds"
        elif param_lower.endswith('_id'):
            return f"Identifier for {param_name[:-3].replace('_', ' ')}"
        elif param_lower.endswith('_name'):
            return f"Name of {param_name[:-5].replace('_', ' ')}"
        elif param_lower.endswith('_path'):
            return f"Path to {param_name[:-5].replace('_', ' ')}"
        elif param_lower.endswith('_url'):
            return f"URL for {param_name[:-4].replace('_', ' ')}"
        elif param_lower.startswith('is_'):
            return f"Boolean flag indicating if {param_name[3:].replace('_', ' ')}"
        elif param_lower.startswith('has_'):
            return f"Boolean flag indicating presence of {param_name[4:].replace('_', ' ')}"
        else:
            return f"Parameter for {param_name.replace('_', ' ')}"
    
    def _fallback_documentation(self) -> str:
        """Return a fallback when generation completely fails."""
        return "Function implementation. See source code for details."
    
    def clean_response(self, response: str) -> str:
        """Clean up LLM response to remove unwanted formatting."""
        # Remove code blocks
        response = response.replace('```python', '')
        response = response.replace('```', '')
        
        # Remove triple quotes
        response = response.replace('"""', '')
        response = response.replace("'''", '')
        
        # Remove function definitions if accidentally included
        lines = response.split('\n')
        cleaned_lines = []
        skip_next = False
        
        for line in lines:
            if 'def ' in line and '(' in line:
                skip_next = True
                continue
            if skip_next and line.strip().startswith('return'):
                skip_next = False
                continue
            if not skip_next:
                cleaned_lines.append(line)
        
        # Remove excessive blank lines
        final_lines = []
        prev_blank = False
        for line in cleaned_lines:
            is_blank = len(line.strip()) == 0
            if not (is_blank and prev_blank):
                final_lines.append(line)
            prev_blank = is_blank
        
        return '\n'.join(final_lines).strip()