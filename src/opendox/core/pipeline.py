"""Main documentation generation pipeline."""
from pathlib import Path
from typing import Dict, List, Any
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.table import Table

from opendox.parsers.python_parser import PythonParser
from opendox.generators.llm_generator import LLMGenerator
from opendox.formats.mkdocs_formatter import MkDocsFormatter
from opendox.core.file_discovery import FileDiscovery
from opendox.core.cache import DocumentationCache

console = Console()

class DocumentationPipeline:
    """Orchestrate the documentation generation process."""
    
    def __init__(self, model: str = "deepseek-coder:1.3b"):
        self.discovery = FileDiscovery()
        self.parser = PythonParser()
        self.generator = LLMGenerator(model=model)
        self.cache = None  # Will be initialized per project
        self.stats = {
            'modules_processed': 0,
            'functions_documented': 0,
            'classes_documented': 0,
            'errors': [],
            'file_details': {}  # Track details for each file
        }
    
    def generate(self, source_path: Path, output_path: Path, max_files: int = 10, incremental: bool = True):
        """Generate documentation for a project.
        
        Args:
            source_path: Path to the source code
            output_path: Path for output documentation
            max_files: Maximum number of files to process
            incremental: Use cache for incremental updates
        """
        # Initialize cache for this project if incremental mode
        if incremental:
            self.cache = DocumentationCache(source_path, output_path)
        
        # Setup formatter
        formatter = MkDocsFormatter(output_path)
        
        # Setup MkDocs configuration
        if source_path.name == '.' or source_path.name == '':
            # Try to get the actual directory name when using '.'
            project_name = Path.cwd().name if source_path == Path('.') else "OPENDOX"
        else:
            project_name = source_path.name
        
        # Ensure we have a valid project name
        if not project_name or project_name in ['.', '..', '']:
            project_name = "OPENDOX"
            
        console.print(f"[bold blue]Setting up documentation for:[/bold blue] {project_name}")
        
        # Discover Python files
        all_files = self.discovery.discover_files(source_path, max_files=max_files * 2)  # Get more files initially
        files = self.discovery.filter_python_files(all_files)[:max_files]  # Then limit Python files
        
        console.print(f"[green]Found {len(files)} Python files to process[/green]")
        
        # Process files with progress bar
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=console
        ) as progress:
            task = progress.add_task("Processing files...", total=len(files))
            
            for file_path in files:
                success = self._process_file(file_path, formatter, progress, task)
                if success:
                    self.stats['modules_processed'] += 1
                progress.update(task, advance=1)
        
        # Finalize documentation
        formatter.create_index(project_name, f"Automated documentation for {project_name}")
        formatter.finalize()
        
        # Display summary
        self._display_summary(files)
        
        return self.stats
    
    def _process_file(self, file_path: Path, formatter: MkDocsFormatter, progress: Progress = None, task_id = None) -> bool:
        """Process a single file and generate documentation.
        
        Args:
            file_path: Path to the Python file
            formatter: MkDocs formatter instance
            progress: Rich progress instance for status updates
            task_id: Task ID for progress updates
            
        Returns:
            True if file was successfully processed
        """
        try:
            # Initialize file stats
            self.stats['file_details'][str(file_path)] = {
                'functions': 0,
                'classes': 0,
                'status': 'Processing'
            }
            
            # Check cache if enabled
            if self.cache and not self.cache.needs_update(file_path):
                self.stats['file_details'][str(file_path)]['status'] = 'Cached'
                console.print(f"  [dim]→ Skipping {file_path.name} (cached)[/dim]")
                return False
            
            # Parse the file
            result = self.parser.parse_file(file_path)
            
            if 'error' in result:
                self.stats['errors'].append({
                    'file': str(file_path),
                    'error': result['error']
                })
                self.stats['file_details'][str(file_path)]['status'] = f"Error: {result['error'][:40]}"
                return False
            
            # Extract functions and classes
            functions = result.get('functions', [])
            classes = result.get('classes', [])
            
            # Update file stats
            self.stats['file_details'][str(file_path)]['functions'] = len(functions)
            self.stats['file_details'][str(file_path)]['classes'] = len(classes)
            
            # Skip empty files
            if not functions and not classes:
                self.stats['file_details'][str(file_path)]['status'] = 'Empty'
                return False
            
            # Generate documentation for functions
            function_docs = []
            for func in functions[:5]:  # Limit to 5 functions per file
                if progress and task_id is not None:
                    progress.update(task_id, description=f"Processing files... [cyan]→ Documenting {func.name}[/cyan]")
                
                # Convert to dict if needed
                func_data = func.__dict__ if hasattr(func, '__dict__') else func
                doc = self.generator.generate_function_doc(func_data)
                function_docs.append(doc)
                self.stats['functions_documented'] += 1
            
            # Generate documentation for classes  
            class_docs = []
            for cls in classes[:3]:  # Limit to 3 classes per file
                if progress and task_id is not None:
                    progress.update(task_id, description=f"Processing files... [cyan]→ Documenting {cls.name}[/cyan]")
                
                # Convert to dict if needed
                cls_data = cls.__dict__ if hasattr(cls, '__dict__') else cls
                # For now, just use the existing docstring or generate a simple one
                if cls_data.get('docstring'):
                    doc = cls_data['docstring']
                else:
                    doc = f"Class {cls_data.get('name', 'Unknown')} with {len(cls_data.get('metadata', {}).get('methods', []))} methods."
                class_docs.append(doc)
                self.stats['classes_documented'] += 1
            
            # Create module data
            module_data = {
                'name': file_path.stem,
                'path': str(file_path),
                'functions': functions[:5],
                'classes': classes[:3],
                'docs': class_docs + function_docs,
                'description': f"Module containing {len(functions)} functions and {len(classes)} classes"
            }
            
            # Add module to formatter
            formatter.add_module(module_data)
            
            # Update cache if enabled
            if self.cache:
                self.cache.update(file_path)
            
            # Update status
            self.stats['file_details'][str(file_path)]['status'] = 'Documented'
            
            return True
            
        except Exception as e:
            self.stats['errors'].append({
                'file': str(file_path),
                'error': str(e)
            })
            self.stats['file_details'][str(file_path)] = {
                'functions': 0,
                'classes': 0,
                'status': f"Error: {str(e)[:40]}"
            }
            console.print(f"  [red]→ Error processing {file_path.name}: {e}[/red]")
            return False
    
    def _display_summary(self, files: List[Path]):
        """Display processing summary table."""
        console.print("\n")
        
        # Create summary table
        table = Table(title="Processing Summary")
        table.add_column("File", style="cyan", no_wrap=True)
        table.add_column("Functions", justify="center")
        table.add_column("Classes", justify="center")
        table.add_column("Status")
        
        # Add rows for each file
        for file_path in files[:20]:  # Show first 20 files
            file_str = str(file_path)
            
            # Get details from stats if available
            if file_str in self.stats['file_details']:
                details = self.stats['file_details'][file_str]
                func_count = str(details['functions'])
                class_count = str(details['classes'])
                status = details['status']
                
                # Color code the status
                if status == 'Documented':
                    status_display = f"[green]{status}[/green]"
                elif status == 'Cached':
                    status_display = f"[dim]{status}[/dim]"
                elif status == 'Empty':
                    status_display = f"[dim]{status}[/dim]"
                elif status.startswith('Error'):
                    status_display = f"[red]{status}[/red]"
                else:
                    status_display = status
            else:
                # File wasn't processed at all (likely not Python or filtered out)
                func_count = "0"
                class_count = "0"
                status_display = "[dim]Empty[/dim]"
            
            table.add_row(
                file_path.name,
                func_count,
                class_count,
                status_display
            )
        
        console.print(table)
        
        # Print final statistics
        console.print("\n[bold green]✅ Documentation Complete![/bold green]")
        console.print(f"  • Modules documented: {self.stats['modules_processed']}")
        console.print(f"  • Functions documented: {self.stats['functions_documented']}")  
        console.print(f"  • Classes documented: {self.stats['classes_documented']}")
        
        if self.stats['errors']:
            console.print(f"  • [yellow]Errors encountered: {len(self.stats['errors'])}[/yellow]")