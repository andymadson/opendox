"""Material for MkDocs formatter."""
from pathlib import Path
import yaml
from typing import List

from .mkdocs_formatter import MkDocsFormatter

class MaterialFormatter(MkDocsFormatter):
    """Enhanced MkDocs formatter with Material theme."""
    
    def create_advanced_config(self, project_name: str):
        """Create Material for MkDocs config with all features."""
        config = {
            'site_name': project_name,
            'site_description': f'Documentation for {project_name}',
            'theme': {
                'name': 'material',
                'features': [
                    'navigation.tabs',
                    'navigation.sections',
                    'navigation.expand',
                    'navigation.top',
                    'search.suggest',
                    'search.highlight',
                ],
                'palette': [
                    {
                        'scheme': 'default',
                        'primary': 'indigo',
                        'accent': 'blue',
                        'toggle': {
                            'icon': 'material/brightness-7',
                            'name': 'Switch to dark mode'
                        }
                    },
                    {
                        'scheme': 'slate',
                        'primary': 'indigo',
                        'accent': 'blue',
                        'toggle': {
                            'icon': 'material/brightness-4',
                            'name': 'Switch to light mode'
                        }
                    }
                ]
            },
            'plugins': ['search'],
            'markdown_extensions': [
                'pymdownx.highlight',
                'pymdownx.superfences',
                'admonition',
                'codehilite'
            ]
        }
        
        config_path = self.output_dir / 'mkdocs.yml'
        with open(config_path, 'w') as f:
            yaml.dump(config, f)
    
    def create_api_page_with_diagrams(self, module_name: str, functions: List, docs: List[str]):
        """Create enhanced API documentation with diagrams and examples."""
        api_dir = self.docs_dir / 'api'
        api_dir.mkdir(exist_ok=True)
        
        content = f"# {module_name}\n\n"
        
        # Add badges for language
        if functions:
            first_func = functions[0]
            language = first_func.get('language', 'python') if isinstance(first_func, dict) else 'python'
            
            # Language badge
            lang_badges = {
                'python': '![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)',
                'javascript': '![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black)',
                'typescript': '![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white)',
                'go': '![Go](https://img.shields.io/badge/Go-00ADD8?logo=go&logoColor=white)',
            }
            
            if language in lang_badges:
                content += f"{lang_badges[language]}\n\n"
        
        # Module overview
        content += "## Module Overview\n\n"
        if functions:
            content += f"This module contains {len(functions)} functions:\n\n"
            
            # Create summary table
            content += "| Function | Description | Line |\n"
            content += "|----------|-------------|------|\n"
            for func in functions[:10]:  # Limit to first 10
                func_name = func.get('name') if isinstance(func, dict) else func.name
                line = func.get('line_start', 'N/A') if isinstance(func, dict) else 'N/A'
                # Get first line of doc as description
                func_doc = docs[functions.index(func)] if functions.index(func) < len(docs) else ''
                first_line = func_doc.split('\n')[0] if func_doc else 'No description'
                content += f"| `{func_name}` | {first_line[:50]}... | {line} |\n"
        
        content += "\n## Functions\n\n"
        
        # Add detailed function documentation
        for func, doc in zip(functions, docs):
            if isinstance(func, dict):
                func_name = func.get('name', 'unknown')
                args = func.get('metadata', {}).get('args', [])
                line_start = func.get('line_start', 'N/A')
                language = func.get('language', 'python')
            else:
                func_name = getattr(func, 'name', 'unknown')
                args = getattr(func.metadata, 'args', []) if hasattr(func, 'metadata') else []
                line_start = getattr(func, 'line_start', 'N/A')
                language = 'python'
            
            # Function header with anchor
            content += f"### `{func_name}()`\n\n"
            
            # Add line number reference
            content += f"*Defined at line {line_start}*\n\n"
            
            # Add signature in code block
            if args:
                signature = f"{func_name}({', '.join(args)})"
            else:
                signature = f"{func_name}()"
            
            content += f"```{language}\n{signature}\n```\n\n"
            
            # Add documentation
            content += f"{doc}\n\n"
            
            # Add usage example (if available or generated)
            if language == 'python':
                content += "**Example Usage:**\n\n"
                content += f"```python\n# Example usage of {func_name}\nresult = {signature}\n```\n\n"
            elif language in ['javascript', 'typescript']:
                content += "**Example Usage:**\n\n"
                content += f"```javascript\n// Example usage of {func_name}\nconst result = {signature};\n```\n\n"
            
            content += "---\n\n"
        
        # Write the page
        page_path = api_dir / f"{module_name}.md"
        with open(page_path, 'w', encoding='utf-8', errors='ignore') as f:
            f.write(content)