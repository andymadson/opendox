"""Format documentation as MkDocs markdown."""
from pathlib import Path
from typing import List, Dict, Any
import yaml

class MkDocsFormatter:
    """Convert parsed code to MkDocs documentation."""
    
    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir)
        self.docs_dir = self.output_dir / "docs"
        self.docs_dir.mkdir(parents=True, exist_ok=True)
        
    def create_config(self, project_name: str = "Documentation"):
        """Create mkdocs.yml configuration."""
        config = {
            'site_name': project_name,
            'theme': {'name': 'material'}
        }
        config_path = self.output_dir / 'mkdocs.yml'
        with open(config_path, 'w') as f:
            yaml.dump(config, f)
            
    def create_index(self, project_name: str, description: str = ""):
        """Create index.md."""
        content = f"# {project_name}\n\n{description}\n"
        index_path = self.docs_dir / 'index.md'
        index_path.write_text(content)
        
    def format_function(self, func_data: Dict[str, Any], docstring: str = "") -> str:
        """Format a function as markdown."""
        name = func_data.get('name', 'unknown')
        args = func_data.get('metadata', {}).get('args', [])
        md = f"### {name}({', '.join(args)})\n\n"
        if docstring:
            md += docstring + "\n\n"
        return md
    
    def create_module_page(self, module_name: str, functions: List, docs: List[str]):
        """Create documentation page for a module."""
        api_dir = self.docs_dir / 'api'
        api_dir.mkdir(exist_ok=True)
        content = f"# {module_name}\n\n"
        for func, doc in zip(functions, docs):
            # Clean the doc string to remove problematic characters
            doc_clean = doc.encode('utf-8', errors='ignore').decode('utf-8')
            content += self.format_function(func.__dict__, doc_clean)
        page_path = api_dir / f"{module_name}.md"
        # Write with explicit UTF-8 encoding
        with open(page_path, 'w', encoding='utf-8', errors='ignore') as f:
            f.write(content)