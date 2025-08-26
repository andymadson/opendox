from pathlib import Path
from opendox.core.file_discovery import FileDiscovery
from opendox.parsers.python_parser import PythonParser
from opendox.generators.llm_generator import LLMGenerator
from rich.console import Console

console = Console()

def generate_project_docs(repo_path: Path):
    """Generate documentation for a project."""
    discovery = FileDiscovery()
    parser = PythonParser()
    generator = LLMGenerator()
    
    # Find Python files
    files = discovery.filter_python_files(
        discovery.discover_files(repo_path, max_files=10)
    )
    
    console.print(f"[green]Found {len(files)} Python files[/green]")
    
    for file_path in files[:3]:  # Just first 3 for testing
        console.print(f"\n[blue]Processing: {file_path.name}[/blue]")
        
        result = parser.parse_file(file_path)
        
        if 'error' in result:
            console.print(f"  [red]Error: {result['error']}[/red]")
            continue
            
        # Generate docs for first function
        if result.get('functions'):
            func = result['functions'][0]
            console.print(f"  Documenting: {func.name}")
            doc = generator.generate_function_doc(func.__dict__)
            console.print(f"  Generated: {doc[:100]}...")

# Run it
generate_project_docs(Path("src/opendox"))