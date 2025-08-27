"""LLM-based documentation generator using Ollama."""
import ollama
from typing import Dict, Any, List, Optional
import json
import re
from pathlib import Path
from datetime import datetime

class LLMGenerator:
    """Generate documentation using Ollama with improved prompting and caching."""
    
    def __init__(self, model: str = "deepseek-coder:6.7b", 
                 enable_rag: bool = False, cache_dir: Optional[Path] = None):
        """
        Initialize the LLM Generator.
        
        Args:
            model: The Ollama model to use (deepseek-coder:6.7b or codellama:7b-instruct)
            enable_rag: Whether to use RAG for enhanced documentation
            cache_dir: Directory for caching similar examples
        """
        self.model = model
        self.client = ollama.Client()
        
        # Verify model is available
        try:
            self.client.show(model)
        except:
            print(f"[Warning] Model {model} not found. Attempting to pull...")
            try:
                self.client.pull(model)
            except:
                print(f"[Error] Could not pull {model}. Using fallback.")
                self.model = "llama2:latest"
        
        self.enable_rag = enable_rag
        
        # Windows-compatible cache directory
        if cache_dir is None:
            cache_dir = Path.home() / ".opendox" / "cache"
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Track generation statistics
        self.stats = {
            "total_generated": 0,
            "cache_hits": 0,
            "errors": 0
        }
        
        # Load example library for few-shot learning
        self.example_library = self._load_example_library()
        
    def generate(self, prompt: str, max_tokens: int = 500, temperature: float = 0.7) -> str:
        """
        Generate text using Ollama with better error handling.
        
        Args:
            prompt: The prompt to send to the model
            max_tokens: Maximum number of tokens to generate
            temperature: Temperature for generation (lower = more deterministic)
        
        Returns:
            Generated text or error message
        """
        try:
            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                options={
                    'num_predict': max_tokens,
                    'temperature': temperature,
                    'top_p': 0.9,
                    'stop': ['```', '"""', "'''", 'def ', 'class ', '\n\n\n']
                }
            )
            self.stats["total_generated"] += 1
            return response['response']
        except Exception as e:
            self.stats["errors"] += 1
            print(f"[Warning] LLM generation failed: {str(e)}")
            return self._fallback_documentation()
    
    def generate_function_doc(self, function_data: Dict[str, Any]) -> str:
        """
        Generate or enhance documentation for a function.
        
        Args:
            function_data: Dictionary containing function metadata
        
        Returns:
            Generated documentation string
        """
        existing_doc = function_data.get('docstring', '')
        
        # Check if we already have good documentation
        if existing_doc and self._is_good_docstring(existing_doc):
            return self._enhance_existing_docstring(function_data, existing_doc)
        
        # Generate new documentation
        return self._generate_comprehensive_docstring(function_data)
    
    def _generate_comprehensive_docstring(self, function_data: Dict[str, Any]) -> str:
        """Generate a comprehensive docstring for an undocumented function."""
        name = function_data.get('name', 'unknown')
        args = function_data.get('metadata', {}).get('args', [])
        returns = function_data.get('metadata', {}).get('returns')
        decorators = function_data.get('metadata', {}).get('decorators', [])
        is_async = function_data.get('metadata', {}).get('is_async', False)
        
        # Build context
        context_hints = []
        if 'init' in name or name == '__init__':
            context_hints.append("This is a constructor/initialization method")
        if 'get' in name or 'fetch' in name:
            context_hints.append("This likely retrieves or fetches data")
        if 'set' in name or 'update' in name:
            context_hints.append("This likely modifies or updates data")
        if 'create' in name or 'build' in name:
            context_hints.append("This likely creates or builds something")
        if is_async:
            context_hints.append("This is an async function")
        if decorators:
            context_hints.append(f"Uses decorators: {', '.join(decorators)}")
        
        # Create a more specific, directive prompt
        prompt = f"""Write a Python docstring for this function:

Function: {name}
Parameters: {', '.join(args) if args else 'none'}
Return type hint: {returns if returns else 'not specified'}
{' | '.join(context_hints) if context_hints else ''}

Instructions:
1. Start with a clear, specific one-line description (NOT generic placeholder text)
2. Based on the function name '{name}', describe what it actually does
3. Document each parameter with its purpose
4. Describe what the function returns
5. Add an example if the function has 2+ parameters

Write ONLY the docstring content (no quotes, no markdown):
"""

        response = self.generate(prompt, max_tokens=400, temperature=0.7)
        cleaned = self.clean_response(response)
        
        # Check for placeholder text and fix it
        if any(placeholder in cleaned.lower() for placeholder in 
               ["one-line summary here", "summary here", "description here", "todo"]):
            better_summary = self._generate_summary_from_name(name)
            # Replace first line with better summary
            lines = cleaned.split('\n')
            lines[0] = better_summary
            cleaned = '\n'.join(lines)
        
        # Ensure it doesn't start with generic text
        if cleaned.startswith("One-line"):
            cleaned = self._generate_summary_from_name(name) + cleaned[cleaned.find('\n'):]
        
        # Cache this generation for future RAG use
        if self.enable_rag and len(cleaned) > 50:
            signature = f"{name}({', '.join(args)})"
            self._cache_documentation(signature, cleaned)
        
        return cleaned
    
    def _generate_summary_from_name(self, name: str) -> str:
        """Generate a meaningful summary from the function name."""
        # Handle special Python methods
        if name == '__init__':
            return "Initialize a new instance of this class."
        if name == '__str__':
            return "Return string representation of the object."
        if name == '__repr__':
            return "Return detailed representation of the object."
        if name.startswith('__') and name.endswith('__'):
            return f"Python magic method for {name.strip('_')} operation."
        
        # Convert snake_case to readable text
        words = name.replace('_', ' ').split()
        
        # Generate based on common patterns
        if not words:
            return "Perform the operation."
        
        first_word = words[0].lower()
        rest = ' '.join(words[1:]) if len(words) > 1 else "operation"
        
        if first_word in ['get', 'fetch', 'retrieve', 'find', 'load']:
            return f"Retrieve {rest}."
        elif first_word in ['set', 'update', 'modify', 'change']:
            return f"Update {rest}."
        elif first_word in ['create', 'build', 'generate', 'make', 'construct']:
            return f"Create {rest}."
        elif first_word in ['delete', 'remove', 'clear', 'destroy']:
            return f"Remove {rest}."
        elif first_word in ['check', 'validate', 'verify', 'test']:
            return f"Validate {rest}."
        elif first_word in ['calculate', 'compute']:
            return f"Calculate {rest}."
        elif first_word in ['parse', 'process', 'analyze']:
            return f"Process {rest}."
        elif first_word in ['save', 'store', 'write']:
            return f"Save {rest}."
        elif first_word in ['read', 'open']:
            return f"Read {rest}."
        elif first_word == 'is' or first_word == 'has':
            return f"Check if {name.replace('_', ' ')}."
        elif first_word == 'run' or first_word == 'execute':
            return f"Execute {rest}."
        else:
            # Default: make it readable
            return f"{name.replace('_', ' ').capitalize()}."
    
    def _enhance_existing_docstring(self, function_data: Dict[str, Any], existing: str) -> str:
        """Enhance an existing docstring by adding missing sections."""
        name = function_data.get('name', 'unknown')
        args = function_data.get('metadata', {}).get('args', [])
        
        # Check what's missing
        missing_sections = []
        existing_lower = existing.lower()
        
        if 'args:' not in existing_lower and 'parameters:' not in existing_lower and args:
            missing_sections.append('Args')
        if 'returns:' not in existing_lower and 'return:' not in existing_lower:
            missing_sections.append('Returns')
        if 'example:' not in existing_lower and len(args) > 2:
            missing_sections.append('Example')
        
        if not missing_sections:
            return existing  # Already complete
        
        prompt = f"""Enhance this Python docstring by adding the missing sections.

Function: {name}
Parameters: {args}
Current docstring:
{existing}

Add ONLY these missing sections: {', '.join(missing_sections)}
Keep the original description unchanged.
Write only the enhanced docstring content:"""

        response = self.generate(prompt, max_tokens=400, temperature=0.5)
        return self.clean_response(response)
    
    def clean_response(self, response: str) -> str:
        """
        Clean up LLM response to remove unwanted formatting.
        
        Args:
            response: Raw response from LLM
            
        Returns:
            Cleaned documentation string
        """
        if not response:
            return ""
        
        # Remove code block markers and language identifiers
        cleaned = re.sub(r'```(?:python)?\n?', '', response)
        cleaned = re.sub(r'```\n?', '', cleaned)
        
        # Remove triple quotes
        cleaned = cleaned.replace('"""', '')
        cleaned = cleaned.replace("'''", '')
        
        # Remove function definitions if accidentally included
        if 'def ' in cleaned:
            cleaned = cleaned.split('def ')[0]
        
        # Remove standalone "python" lines
        lines = cleaned.split('\n')
        cleaned_lines = []
        for line in lines:
            stripped = line.strip().lower()
            if stripped not in ['python', 'python:', '```python', '```']:
                cleaned_lines.append(line)
        
        # Remove excessive blank lines (more than 2 consecutive)
        cleaned = '\n'.join(cleaned_lines)
        cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
        
        # Ensure proper indentation for docstring sections
        cleaned = self._fix_indentation(cleaned)
        
        return cleaned.strip()
    
    def _fix_indentation(self, text: str) -> str:
        """Fix common indentation issues in generated docstrings."""
        lines = text.split('\n')
        fixed_lines = []
        in_section = False
        
        for line in lines:
            # Detect section headers
            if re.match(r'^(Args?|Parameters?|Returns?|Raises?|Yields?|Example?|Examples?|Note?|Notes?|Warning?|See Also?):', line):
                fixed_lines.append(line)
                in_section = True
            elif in_section and line.strip() and not line.startswith('    '):
                # Add proper indentation for section content
                if line.strip().startswith('-') or line.strip().startswith('*'):
                    # Bullet point - convert to proper indentation
                    content = line.strip()[1:].strip()
                    fixed_lines.append(f"    {content}")
                elif not re.match(r'^[A-Z]', line.strip()):
                    # Regular content that should be indented
                    fixed_lines.append(f"    {line.strip()}")
                else:
                    # New section or description
                    fixed_lines.append(line)
                    in_section = False
            else:
                fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def _is_good_docstring(self, docstring: str) -> bool:
        """
        Check if a docstring is already comprehensive.
        
        Args:
            docstring: The existing docstring
            
        Returns:
            True if docstring is comprehensive, False otherwise
        """
        if len(docstring) < 20:
            return False
        
        # Check for placeholder text
        if any(placeholder in docstring.lower() for placeholder in 
               ["todo", "fixme", "xxx", "placeholder", "summary here"]):
            return False
        
        # Check for key sections
        has_description = len(docstring.split('\n')[0]) > 10
        has_args = any(section in docstring.lower() 
                      for section in ['args:', 'parameters:', 'params:'])
        has_returns = any(section in docstring.lower() 
                         for section in ['returns:', 'return:'])
        
        return has_description and (has_args or has_returns)
    
    def _find_similar_functions(self, signature: str) -> List[str]:
        """
        Find similar functions from cache for RAG.
        
        Args:
            signature: The function signature
            
        Returns:
            List of similar function documentation examples
        """
        cache_file = self.cache_dir / "function_cache.json"
        
        if not cache_file.exists():
            return []
        
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache = json.load(f)
            
            # Simple similarity based on parameter count and naming
            similar = []
            target_param_count = signature.count(',') + 1 if '(' in signature else 0
            
            for cached_sig, cached_doc in cache.items():
                cached_param_count = cached_sig.count(',') + 1 if '(' in cached_sig else 0
                if abs(cached_param_count - target_param_count) <= 1:
                    # Also check for name similarity
                    if any(word in cached_sig.lower() for word in signature.lower().split('_')):
                        similar.append(cached_doc)
                        if len(similar) >= 3:
                            break
            
            return similar
        except Exception:
            return []
    
    def _cache_documentation(self, signature: str, documentation: str):
        """
        Cache generated documentation for future RAG use.
        
        Args:
            signature: The function signature
            documentation: The generated documentation
        """
        cache_file = self.cache_dir / "function_cache.json"
        
        try:
            if cache_file.exists():
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cache = json.load(f)
            else:
                cache = {}
            
            cache[signature] = documentation
            
            # Limit cache size
            if len(cache) > 1000:
                # Remove oldest entries (simple FIFO)
                items = list(cache.items())
                cache = dict(items[-1000:])
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"[Warning] Failed to cache documentation: {e}")
    
    def _load_example_library(self) -> Dict[str, str]:
        """Load a library of good documentation examples."""
        return {
            "simple_function": """Calculate the sum of two numbers.
            
Args:
    a: First number to add
    b: Second number to add
    
Returns:
    The sum of a and b""",
            
            "complex_function": """Process data with multiple transformations.

Applies a series of transformations to the input data including
normalization, filtering, and aggregation operations.

Args:
    data: Input data as numpy array or list
    normalize: Whether to normalize the data (default: True)
    filter_threshold: Minimum threshold for filtering (default: 0.5)
    
Returns:
    Processed data as numpy array
    
Raises:
    ValueError: If data is empty or threshold is invalid
    TypeError: If data type is not supported
    
Example:
    >>> result = process_data([1, 2, 3], normalize=True)
    >>> print(result)
    [0.0, 0.5, 1.0]"""
        }
    
    def _fallback_documentation(self) -> str:
        """Generate minimal fallback documentation when LLM fails."""
        return "Documentation pending - please add manual documentation for this function."
    
    def generate_class_doc(self, class_data: Dict[str, Any]) -> str:
        """
        Generate documentation for a class.
        
        Args:
            class_data: Dictionary containing class metadata
            
        Returns:
            Generated class documentation
        """
        name = class_data.get('name', 'UnknownClass')
        methods = class_data.get('metadata', {}).get('methods', [])
        bases = class_data.get('metadata', {}).get('bases', [])
        docstring = class_data.get('docstring', '')
        
        # More specific prompt for classes
        prompt = f"""Generate documentation for this Python class:

Class name: {name}
Inherits from: {', '.join(bases) if bases else 'object'}
Methods: {', '.join(methods[:5]) if methods else 'none'}  # Limit to first 5
Existing docstring: {docstring[:100] if docstring else 'none'}

Write a comprehensive class docstring that includes:
1. Brief description of what {name} does
2. Main purpose and use cases
3. Key attributes (inferred from methods)
4. Example usage

Write only the docstring content (no quotes or code blocks):"""

        response = self.generate(prompt, max_tokens=400, temperature=0.7)
        cleaned = self.clean_response(response)
        
        # Fix generic class descriptions
        if "this class" in cleaned.lower()[:50]:
            cleaned = cleaned.replace("This class", f"The {name} class", 1)
            cleaned = cleaned.replace("this class", f"the {name} class", 1)
        
        return cleaned
    
    def generate_module_doc(self, module_data: Dict[str, Any]) -> str:
        """
        Generate documentation for an entire module.
        
        Args:
            module_data: Dictionary containing module information
            
        Returns:
            Generated module documentation
        """
        module_name = module_data.get('name', 'module')
        classes = module_data.get('classes', [])
        functions = module_data.get('functions', [])
        
        prompt = f"""Generate a module-level docstring for the Python module '{module_name}'.

This module contains:
- {len(classes)} classes: {', '.join([c.name for c in classes[:3]])}{'...' if len(classes) > 3 else ''}
- {len(functions)} functions: {', '.join([f.name for f in functions[:3]])}{'...' if len(functions) > 3 else ''}

Write a clear module docstring that explains the module's purpose and main functionality.
Keep it concise but informative. Write only the content:"""

        response = self.generate(prompt, max_tokens=200, temperature=0.6)
        return self.clean_response(response)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get generation statistics."""
        return {
            **self.stats,
            "cache_size": len(list(self.cache_dir.glob("*.json"))),
            "model": self.model,
            "timestamp": datetime.now().isoformat()
        }