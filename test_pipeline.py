#!/usr/bin/env python
"""Test script for the enhanced pipeline on Windows."""
import sys
import os
from pathlib import Path
import shutil
import tempfile
import hashlib

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from opendox.core.pipeline import DocumentationPipeline
from rich.console import Console

console = Console()

def test_basic_pipeline():
    """Test basic pipeline functionality."""
    console.print("\n[bold blue]Testing Basic Pipeline[/bold blue]")
    
    # Use the opendox source itself as test data
    source_path = Path("src/opendox")
    
    # Create temp output directory
    temp_dir = Path("test_output")
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    
    output_path = temp_dir / "test_docs"
    
    try:
        # Initialize pipeline with fallbacks
        pipeline = DocumentationPipeline(
            model="deepseek-coder:1.3b",
            use_enhanced=False,  # Start with basic parser
            use_material=False   # Start with basic formatter
        )
        
        # Generate documentation
        pipeline.generate(
            source_path=source_path,
            output_path=output_path,
            max_files=3,
            incremental=False
        )
        
        # Check outputs
        assert output_path.exists(), "Output directory not created"
        assert (output_path / "mkdocs.yml").exists(), "MkDocs config not created"
        assert (output_path / "docs").exists(), "Docs directory not created"
        
        console.print("[green]✓ Basic pipeline test passed[/green]")
        
        # List generated files
        docs_dir = output_path / "docs"
        if docs_dir.exists():
            console.print("\n[cyan]Generated files:[/cyan]")
            for file in docs_dir.rglob("*.md"):
                console.print(f"  - {file.relative_to(output_path)}")
                
    except Exception as e:
        console.print(f"[red]Error in basic pipeline: {e}[/red]")
        raise
    finally:
        # Clean up
        if temp_dir.exists() and temp_dir != Path("."):
            try:
                shutil.rmtree(temp_dir)
            except PermissionError:
                console.print("[yellow]Could not remove temp directory (file in use)[/yellow]")

def test_parser_imports():
    """Test if parsers can be imported."""
    console.print("\n[bold blue]Testing Parser Imports[/bold blue]")
    
    # Test basic parser
    try:
        from opendox.parsers.python_parser import PythonParser
        console.print("[green]✓ Basic Python parser available[/green]")
    except ImportError as e:
        console.print(f"[red]✗ Basic parser import failed: {e}[/red]")
        return False
    
    # Test enhanced parser
    try:
        from opendox.parsers.enhanced_parser import EnhancedPythonParser
        console.print("[green]✓ Enhanced parser available (LibCST installed)[/green]")
    except ImportError:
        console.print("[yellow]! Enhanced parser not available (LibCST not installed)[/yellow]")
    
    # Test universal parser
    try:
        from opendox.parsers.universal_parser import UniversalParser
        console.print("[green]✓ Universal parser available (Tree-sitter installed)[/green]")
    except ImportError:
        console.print("[yellow]! Universal parser not available (Tree-sitter not installed)[/yellow]")
    
    # Test state manager
    try:
        from opendox.database.state_manager import DocumentationStateManager
        console.print("[green]✓ State manager available (DuckDB installed)[/green]")
    except ImportError:
        console.print("[yellow]! State manager not available (DuckDB not installed)[/yellow]")
    
    return True

def test_single_file_parsing():
    """Test parsing a single file."""
    console.print("\n[bold blue]Testing Single File Parsing[/bold blue]")
    
    from opendox.parsers.python_parser import PythonParser
    
    # Test with a known file
    test_file = Path("src/opendox/cli/main.py")
    if not test_file.exists():
        console.print(f"[red]Test file not found: {test_file}[/red]")
        return
    
    parser = PythonParser()
    result = parser.parse_file(test_file)
    
    if 'error' in result:
        console.print(f"[red]Parse error: {result['error']}[/red]")
    else:
        console.print(f"[green]✓ Parsed {test_file.name}[/green]")
        console.print(f"  - Functions: {len(result.get('functions', []))}")
        console.print(f"  - Classes: {len(result.get('classes', []))}")
        console.print(f"  - Lines: {result.get('total_lines', 0)}")

def test_cache_functionality():
    """Test caching functionality."""
    console.print("\n[bold blue]Testing Cache Functionality[/bold blue]")
    
    from opendox.core.cache import DocumentationCache
    
    # Use a temp directory for cache
    cache_dir = Path("test_cache")
    cache_dir.mkdir(exist_ok=True)
    
    try:
        cache = DocumentationCache(cache_dir)
        test_file = Path("src/opendox/cli/main.py")
        
        if test_file.exists():
            # Test cache operations
            needs_update = cache.needs_update(test_file)
            console.print(f"  File needs update: {needs_update}")
            
            # Update cache
            cache.update(test_file)
            
            # Check again
            needs_update2 = cache.needs_update(test_file)
            console.print(f"  After caching, needs update: {needs_update2}")
            
            if not needs_update2:
                console.print("[green]✓ File cache working correctly[/green]")
            else:
                console.print("[yellow]! Cache may not be working correctly[/yellow]")
        else:
            console.print(f"[yellow]Test file not found: {test_file}[/yellow]")
            
    finally:
        # Clean up cache directory
        if cache_dir.exists():
            try:
                shutil.rmtree(cache_dir)
            except:
                pass

def main():
    """Run all tests."""
    console.print("[bold magenta]OPENDOX Pipeline Tests (Windows)[/bold magenta]")
    console.print(f"Python: {sys.version}")
    console.print(f"Working directory: {os.getcwd()}\n")
    
    try:
        # Run tests in order
        if test_parser_imports():
            test_single_file_parsing()
            test_cache_functionality()
            test_basic_pipeline()
            
            console.print("\n[bold green]✅ All tests completed![/bold green]")
        else:
            console.print("\n[bold yellow]⚠ Some components not available[/bold yellow]")
        
    except AssertionError as e:
        console.print(f"\n[bold red]❌ Test failed: {e}[/bold red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[bold red]❌ Unexpected error: {e}[/bold red]")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()