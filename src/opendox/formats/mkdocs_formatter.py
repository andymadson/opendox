"""Format documentation as MkDocs markdown."""
from pathlib import Path
from typing import List, Dict, Any, Optional
import yaml
import json
from datetime import datetime

class MkDocsFormatter:
    """Convert parsed code to MkDocs documentation."""
    
    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir)
        self.docs_dir = self.output_dir / "docs"
        self.docs_dir.mkdir(parents=True, exist_ok=True)
        
        # Track created pages for navigation
        self.api_pages = []
        self.guide_pages = []
        
        # Track modules for complete documentation
        self.modules = []
        self.nav_structure = {}
        
    def create_config(self, project_name: str = "Documentation"):
        """Create mkdocs.yml configuration with enhanced features."""
        config = {
            'site_name': project_name,
            'site_description': f'Automated documentation for {project_name}',
            'site_author': 'OPENDOX',
            
            # Repository info without site_url to avoid weird local serving URLs
            'repo_url': f'https://github.com/andymadson/{project_name.lower()}',
            'repo_name': f'andymadson/{project_name.lower()}',
            'edit_uri': 'edit/main/docs/',
            
            'theme': {
                'name': 'material',
                'language': 'en',
                'palette': [
                    {
                        'media': '(prefers-color-scheme: light)',
                        'scheme': 'default',
                        'primary': 'indigo',
                        'accent': 'indigo',
                        'toggle': {
                            'icon': 'material/brightness-7',
                            'name': 'Switch to dark mode'
                        }
                    },
                    {
                        'media': '(prefers-color-scheme: dark)',
                        'scheme': 'slate',
                        'primary': 'indigo',
                        'accent': 'indigo',
                        'toggle': {
                            'icon': 'material/brightness-4',
                            'name': 'Switch to light mode'
                        }
                    }
                ],
                'font': {
                    'text': 'Roboto',
                    'code': 'Roboto Mono'
                },
                'features': [
                    'navigation.tabs',
                    'navigation.sections',
                    'navigation.expand',
                    'navigation.path',
                    'navigation.top',
                    'navigation.footer',
                    'navigation.indexes',
                    'search.suggest',
                    'search.highlight',
                    'search.share',
                    'content.code.copy',
                    'content.code.select',
                    'content.code.annotate',
                    'toc.integrate',
                    'toc.follow'
                ],
                'icon': {
                    'logo': 'material/library',
                    'repo': 'fontawesome/brands/github'
                }
            },
            
            'plugins': [
                'search',
                'autorefs'
            ],
            
            'markdown_extensions': [
                'pymdownx.highlight',
                'pymdownx.superfences',
                'pymdownx.tabbed',
                'pymdownx.details',
                'pymdownx.snippets',
                'pymdownx.keys',
                'pymdownx.caret',
                'pymdownx.mark',
                'pymdownx.tilde',
                'pymdownx.smartsymbols',
                'admonition',
                'attr_list',
                'md_in_html',
                'footnotes',
                'tables',
                'def_list',
                'pymdownx.tasklist',
                'pymdownx.emoji',
                'toc'
            ],
            
            'extra': {
                'social': [
                    {
                        'icon': 'fontawesome/brands/github',
                        'link': f'https://github.com/andymadson/{project_name.lower()}'
                    },
                    {
                        'icon': 'fontawesome/brands/python',
                        'link': 'https://pypi.org/project/opendox/'
                    },
                    {
                        'icon': 'fontawesome/brands/twitter',
                        'link': 'https://twitter.com/'
                    }
                ],
                'generator': False,
                'version': {
                    'provider': 'mike'
                }
            },
            
            'copyright': f'Copyright &copy; {datetime.now().year} - Generated with <a href="https://github.com/andymadson/opendox">OPENDOX</a>'
        }
        
        # Add navigation if we have modules
        if self.modules or self.api_pages:
            config['nav'] = self._build_navigation()
            
        # Save config with UTF-8 encoding
        config_path = self.output_dir / 'mkdocs.yml'
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
            
    def create_index(self, project_name: str, description: str = ""):
        """Create an enhanced index.md homepage."""
        # Ensure we have a valid project name
        if not project_name or project_name.strip() in ['', '.', '..']:
            project_name = "OPENDOX"
            
        project_lower = project_name.lower()
        current_date = datetime.now().strftime('%B %d, %Y at %I:%M %p')
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        num_modules = len(self.api_pages) if self.api_pages else len(self.modules)
        
        # Count total functions and classes
        total_functions = sum(len(m.get('functions', [])) for m in self.modules)
        total_classes = sum(len(m.get('classes', [])) for m in self.modules)
        
        # Build content without f-string issues
        content = f"""# {project_name} Documentation

<div align="center">

**Welcome to the {project_name} Documentation**

*Automatically generated by OPENDOX - Intelligent documentation powered by LLMs*

Last updated: {current_date}

</div>

---

## 🚀 Quick Start

<div class="grid cards" markdown>

-   :material-book-open:{{ .lg .middle }} **Getting Started**

    ---

    Learn how to install and use {project_name}

    [:octicons-arrow-right-24: Installation Guide](#installation)

-   :material-api:{{ .lg .middle }} **API Reference**

    ---

    Detailed documentation for all modules and functions

    [:octicons-arrow-right-24: Browse API](api/)

-   :material-source-branch:{{ .lg .middle }} **Source Code**

    ---

    View the project repository on GitHub

    [:octicons-arrow-right-24: GitHub](https://github.com/andymadson/{project_lower})

-   :material-help-circle:{{ .lg .middle }} **Help & Support**

    ---

    Get help and report issues

    [:octicons-arrow-right-24: Get Help](#support)

</div>

---

## 📋 About {project_name}

{description if description else f'{project_name} is a Python project that provides automated documentation generation using Large Language Models. It analyzes your codebase and generates comprehensive, readable documentation.'}

### ✨ Key Features

- 🤖 **AI-Powered** - Uses state-of-the-art LLMs for intelligent documentation
- 🐍 **Python-First** - Optimized for Python projects with deep AST analysis
- 📚 **Comprehensive** - Documents functions, classes, modules, and their relationships
- 🔄 **Incremental Updates** - Only regenerates changed files for efficiency
- 🎨 **Beautiful Output** - Generates modern, searchable documentation with Material for MkDocs
- 🌍 **Multi-Language** - Support for Python, JavaScript, TypeScript, and more

---

## 📦 Installation

Install {project_name} using pip:

```bash
pip install {project_lower}
```

Or install from source:

```bash
git clone https://github.com/andymadson/{project_lower}.git
cd {project_lower}
pip install -e .
```

---

## 🎯 Quick Example

Generate documentation for your project:

```bash
# Generate documentation
{project_lower} generate . --output docs

# Serve locally
cd docs
mkdocs serve
```

Or use it in Python:

```python
from {project_lower}.core.pipeline import DocumentationPipeline
from pathlib import Path

# Create pipeline
pipeline = DocumentationPipeline()

# Generate docs
pipeline.generate(
    source_path=Path('my_project'),
    output_path=Path('docs')
)
```

---

## 📊 Documentation Coverage

!!! info "Project Statistics"
    
    This documentation includes:
    
    - **Modules Documented**: {num_modules}
    - **Functions Documented**: {total_functions}
    - **Classes Documented**: {total_classes}
    - **Last Generated**: {current_time}
    - **Generator**: OPENDOX v0.0.1
    - **Model**: DeepSeek-Coder 6.7B

### Documented Modules

"""
        
        if self.api_pages or self.modules:
            content += "| Module | Functions | Classes | Link |\n"
            content += "|--------|-----------|---------|------|\n"
            
            # Use modules list if available, otherwise api_pages
            if self.modules:
                for module in sorted(self.modules, key=lambda x: x.get('name', '')):
                    module_name = module.get('name', 'unknown')
                    func_count = len(module.get('functions', []))
                    class_count = len(module.get('classes', []))
                    content += f"| {module_name} | {func_count} | {class_count} | [View Documentation](api/{module_name}.md) |\n"
            else:
                for page in sorted(self.api_pages):
                    module_title = page.replace('_', ' ').title()
                    content += f"| {module_title} | - | - | [View Documentation](api/{page}.md) |\n"
            content += "\n"
        else:
            content += "No modules documented yet. Run the generator to create documentation.\n\n"
        
        content += """---

## 🛠️ Configuration

Create a `.opendox.yml` file in your project root:

```yaml
llm:
  model: deepseek-coder:6.7b
  max_tokens: 500
  temperature: 0.7

output:
  format: mkdocs
  theme: material

ignore:
  - tests/
  - __pycache__/
  - .venv/
```

---

## 🤝 Support

- 📧 [Email Support](mailto:support@opendox.io)
- 🐛 [Report Issues](https://github.com/andymadson/opendox/issues)
- 💬 [Discussions](https://github.com/andymadson/opendox/discussions)
- 📖 [Documentation](https://opendox.readthedocs.io)

---

<div align="center">
<small>Generated with ❤️ by OPENDOX</small>
</div>
"""
        
        # Write index file with UTF-8 encoding
        index_path = self.docs_dir / 'index.md'
        index_path.write_text(content, encoding='utf-8')
        
    def add_module(self, module_data: Dict[str, Any]):
        """Add a module to the documentation.
        
        This method is called by the pipeline to register modules.
        """
        # Extract module info
        module_name = module_data.get('name', 'unknown')
        module_path = module_data.get('path', '')
        
        # Store module data
        self.modules.append({
            'name': module_name,
            'path': module_path,
            'functions': module_data.get('functions', []),
            'classes': module_data.get('classes', []),
            'description': module_data.get('description', '')
        })
        
        # Track for navigation
        if module_name not in self.api_pages:
            self.api_pages.append(module_name)
        
        # Create the module documentation page
        self._create_module_documentation(module_data)
        
    def _create_module_documentation(self, module_data: Dict[str, Any]):
        """Create documentation page for a module."""
        module_name = module_data.get('name', 'unknown')
        module_path = module_data.get('path', '')
        functions = module_data.get('functions', [])
        classes = module_data.get('classes', [])
        docs = module_data.get('docs', [])
        
        # Ensure api directory exists
        api_dir = self.docs_dir / 'api'
        api_dir.mkdir(exist_ok=True)
        
        # Build content
        content = f"# `{module_name}` Module\n\n"
        
        # Add module path if available
        if module_path:
            content += f"**Source:** `{module_path}`\n\n"
            
        # Add module description if available
        if module_data.get('description'):
            content += f"{module_data['description']}\n\n"
            
        # Add table of contents
        if functions or classes:
            content += "## Overview\n\n"
            
            # Summary statistics
            content += f"This module contains **{len(functions)}** functions and **{len(classes)}** classes.\n\n"
            
            if classes:
                content += "### Classes\n\n"
                for cls in classes:
                    cls_name = cls.get('name', 'Unknown') if isinstance(cls, dict) else getattr(cls, 'name', 'Unknown')
                    content += f"- [`{cls_name}`](#{cls_name.lower().replace(' ', '-')})\n"
                content += "\n"
                
            if functions:
                content += "### Functions\n\n"
                for func in functions:
                    func_name = func.get('name', 'Unknown') if isinstance(func, dict) else getattr(func, 'name', 'Unknown')
                    content += f"- [`{func_name}()`](#{func_name.lower().replace(' ', '-')})\n"
                content += "\n"
        
        content += "---\n\n"
        
        # Add classes documentation
        if classes:
            content += "## Classes\n\n"
            for i, cls in enumerate(classes):
                doc = docs[i] if i < len(docs) else ""
                content += self.format_class(cls, doc)
                content += "\n---\n\n"
                
        # Add functions documentation
        if functions:
            content += "## Functions\n\n"
            func_docs_start = len(classes)
            for i, func in enumerate(functions):
                doc_index = func_docs_start + i
                doc = docs[doc_index] if doc_index < len(docs) else ""
                content += self.format_function(func, doc)
                content += "\n---\n\n"
        
        # Add footer
        content += f"\n*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} by OPENDOX*\n"
                
        # Write the module page
        page_path = api_dir / f"{module_name}.md"
        with open(page_path, 'w', encoding='utf-8', errors='ignore') as f:
            f.write(content)
    
    def format_function(self, func_data: Any, docstring: str = "") -> str:
        """Format a function as markdown."""
        # Handle both dict and object representations
        if hasattr(func_data, '__dict__'):
            func_dict = func_data.__dict__
        elif isinstance(func_data, dict):
            func_dict = func_data
        else:
            func_dict = {'name': 'unknown'}
            
        name = func_dict.get('name', 'unknown')
        metadata = func_dict.get('metadata', {})
        args = metadata.get('args', [])
        returns = metadata.get('returns', None)
        decorators = metadata.get('decorators', [])
        signature = func_dict.get('signature', '')
        
        # Build function header
        md = f"### `{name}()`\n\n"
        
        # Add signature box
        if signature:
            md += f"```python\n{signature}\n```\n\n"
        else:
            # Build signature from parts
            sig = f"{name}({', '.join(args)})"
            if returns:
                sig += f" -> {returns}"
            md += f"```python\n{sig}\n```\n\n"
        
        # Add decorators if present
        if decorators:
            md += "**Decorators:**\n"
            for dec in decorators:
                md += f"- `@{dec}`\n"
            md += "\n"
            
        # Add docstring
        if docstring:
            # Clean and format the docstring
            doc_clean = docstring.strip()
            
            # Parse docstring sections
            if "Args:" in doc_clean or "Parameters:" in doc_clean:
                md += "#### Description\n\n"
                desc_part = doc_clean.split("Args:")[0].split("Parameters:")[0].strip()
                if desc_part:
                    md += f"{desc_part}\n\n"
                    
                # Format parameters section
                if "Args:" in doc_clean or "Parameters:" in doc_clean:
                    md += "#### Parameters\n\n"
                    params_section = doc_clean.split("Args:")[-1].split("Parameters:")[-1]
                    params_section = params_section.split("Returns:")[0].split("Raises:")[0]
                    md += params_section.strip() + "\n\n"
                    
                # Format returns section
                if "Returns:" in doc_clean:
                    md += "#### Returns\n\n"
                    returns_section = doc_clean.split("Returns:")[-1].split("Raises:")[0]
                    md += returns_section.strip() + "\n\n"
                    
                # Format raises section
                if "Raises:" in doc_clean:
                    md += "#### Raises\n\n"
                    raises_section = doc_clean.split("Raises:")[-1]
                    md += raises_section.strip() + "\n\n"
            else:
                # Simple docstring without sections
                md += "#### Description\n\n"
                md += f"{doc_clean}\n\n"
        else:
            md += "#### Description\n\n*No documentation available*\n\n"
            
        # Add source location if available
        if func_dict.get('line_start'):
            md += f"**Source:** Lines {func_dict['line_start']}"
            if func_dict.get('line_end'):
                md += f"-{func_dict['line_end']}"
            md += "\n"
            
        return md
    
    def format_class(self, class_data: Any, docstring: str = "") -> str:
        """Format a class as markdown."""
        # Handle both dict and object representations
        if hasattr(class_data, '__dict__'):
            class_dict = class_data.__dict__
        elif isinstance(class_data, dict):
            class_dict = class_data
        else:
            class_dict = {'name': 'unknown'}
            
        name = class_dict.get('name', 'unknown')
        metadata = class_dict.get('metadata', {})
        methods = metadata.get('methods', [])
        bases = metadata.get('bases', [])
        decorators = metadata.get('decorators', [])
        
        # Build class header
        md = f"### `{name}`\n\n"
        
        # Add class signature
        if bases:
            md += f"```python\nclass {name}({', '.join(bases)})\n```\n\n"
        else:
            md += f"```python\nclass {name}\n```\n\n"
            
        # Add decorators if present
        if decorators:
            md += "**Decorators:**\n"
            for dec in decorators:
                md += f"- `@{dec}`\n"
            md += "\n"
            
        # Add docstring
        if docstring:
            doc_clean = docstring.strip()
            md += "#### Description\n\n"
            md += f"{doc_clean}\n\n"
        else:
            md += "#### Description\n\n*No documentation available*\n\n"
            
        # Add methods list
        if methods:
            md += "#### Methods\n\n"
            md += "| Method | Description |\n"
            md += "|--------|-------------|\n"
            for method in methods:
                # Try to extract method description from docstring if available
                desc = "Method implementation"
                if method == "__init__":
                    desc = "Initialize the class instance"
                elif method.startswith("_"):
                    desc = "Private method"
                md += f"| `{method}()` | {desc} |\n"
            md += "\n"
            
        # Add source location if available
        if class_dict.get('line_start'):
            md += f"**Source:** Lines {class_dict['line_start']}"
            if class_dict.get('line_end'):
                md += f"-{class_dict['line_end']}"
            md += "\n"
            
        return md
    
    def create_module_page(self, module_name: str, elements: List, docs: List[str]):
        """Legacy method for compatibility - redirects to add_module."""
        module_data = {
            'name': module_name,
            'functions': [e for e in elements if hasattr(e, 'type') and e.type == 'function'],
            'classes': [e for e in elements if hasattr(e, 'type') and e.type == 'class'],
            'docs': docs
        }
        self.add_module(module_data)
        
    def _build_navigation(self) -> List[Dict]:
        """Build navigation structure for mkdocs.yml."""
        nav = [
            {'Home': 'index.md'}
        ]
        
        # Add API Reference section
        if self.api_pages or self.modules:
            api_section = {'API Reference': []}
            
            # Use modules if available, otherwise api_pages
            pages_to_add = []
            if self.modules:
                pages_to_add = [m['name'] for m in self.modules]
            elif self.api_pages:
                pages_to_add = self.api_pages
                
            for page_name in sorted(pages_to_add):
                api_section['API Reference'].append({page_name: f'api/{page_name}.md'})
                
            nav.append(api_section)
            
        return nav
    
    def finalize(self):
        """Finalize documentation generation."""
        # Update config with final navigation
        if self.modules or self.api_pages:
            project_name = self.output_dir.name
            if project_name in ['docs', 'docs_output', 'documentation']:
                project_name = "OPENDOX"
            self.create_config(project_name)
            
        # Create a summary file
        summary_path = self.output_dir / 'generation_summary.json'
        summary = {
            'generated_at': datetime.now().isoformat(),
            'modules_count': len(self.modules),
            'total_functions': sum(len(m.get('functions', [])) for m in self.modules),
            'total_classes': sum(len(m.get('classes', [])) for m in self.modules),
            'modules': [
                {
                    'name': m['name'], 
                    'functions': len(m.get('functions', [])), 
                    'classes': len(m.get('classes', []))
                } 
                for m in self.modules
            ]
        }
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
            
        # Create requirements file for MkDocs if it doesn't exist
        requirements_path = self.output_dir / 'requirements.txt'
        if not requirements_path.exists():
            requirements = [
                'mkdocs>=1.5.3',
                'mkdocs-material>=9.5.0',
                'mkdocs-autorefs>=0.5.0',
                'pymdown-extensions>=10.5'
            ]
            requirements_path.write_text('\n'.join(requirements), encoding='utf-8')