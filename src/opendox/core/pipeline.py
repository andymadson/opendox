"""Main documentation generation pipeline."""
from pathlib import Path
from rich.console import Console
from rich.progress import track, Progress, SpinnerColumn, BarColumn, TextColumn

from opendox.parsers.python_parser import PythonParser
from opendox.generators.llm_generator import LLMGenerator
from opendox.formats.mkdocs_formatter import MkDocsFormatter
from opendox.core.file_discovery import FileDiscovery
from opendox.core.cache import DocumentationCache

console = Console()

class DocumentationPipeline:
    def __init__(self, model: str = "deepseek-coder:1.3b"):
        self.discovery = FileDiscovery()
        self.parser = PythonParser()
        self.generator = LLMGenerator(model=model)
        self.cache = None  # Will be initialized per project
    
    def generate(self, source_path: Path, output_path: Path, max_files: int = 10):
        # Initialize cache for this project
        self.cache = DocumentationCache(source_path)
        
        # ... rest of the method
        
    def _process_file(self, file_path: Path, formatter: MkDocsFormatter):
        """Process a single file."""
        # Check cache first
        if self.cache:
            self.cache.update(file_path)
            console.print(f"[dim]Skipping {file_path.name} (cached)[/dim]")
            return
class DocumentationPipeline:
    """Orchestrate the documentation generation process."""
    
    def __init__(self, model: str = "deepseek-coder:1.3b"):
        self.discovery = FileDiscovery()
        self.parser = PythonParser()
        self.generator = LLMGenerator(model=model)
        
    def generate(self, source_path: Path, output_path: Path, max_files: int = 10):
        """Generate documentation for a project."""
        formatter = MkDocsFormatter(output_path)
        
        # Discover files
        files = self.discovery.discover_files(source_path, max_files=max_files)
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        ) as progress:
            task = progress.add_task("Processing files", total=len(files))
            
            for file in files:
                self._process_file(file, formatter)
                progress.update(task, advance=1)
        
        # Setup MkDocs
        project_name = source_path.name
        formatter.create_config(project_name)
        formatter.create_index(project_name, f"Documentation for {project_name}")
        
        # Discover files
        files = self.discovery.filter_python_files(
            self.discovery.discover_files(source_path, max_files=max_files)
        )
        
        console.print(f"Found {len(files)} Python files")
        
        # Process files with progress bar
        for file_path in track(files, description="Processing files..."):
            self._process_file(file_path, formatter)
            
    def _process_file(self, file_path: Path, formatter: MkDocsFormatter):
        """Process a single file."""
        result = self.parser.parse_file(file_path)
        
        if 'error' in result:
            console.print(f"[yellow]Skipping {file_path.name}: {result['error']}[/yellow]")
            return
            
        if not result.get('functions'):
            return
            
        # Generate docs for functions
        docs = []
        for func in result['functions'][:5]:  # Limit per file
            doc = self.generator.generate_function_doc(func.__dict__)
            docs.append(doc)
            
        # Create module page
        formatter.create_module_page(
            file_path.stem,
            result['functions'][:5],
            docs
        )