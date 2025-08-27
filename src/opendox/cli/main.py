"""OPENDOX CLI - Main entry point for the documentation generator."""
import sys
from pathlib import Path
from typing import Optional
from opendox.core.pipeline import DocumentationPipeline

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

app = typer.Typer(
    name="opendox",
    help="OPENDOX - Automated Technical Documentation Generator",
    add_completion=False,
)
console = Console()

def version_callback(value: bool):
    """Show version and exit."""
    if value:
        from opendox import __version__
        console.print(f"OPENDOX version {__version__}")
        raise typer.Exit()

@app.callback()
def callback(
    version: Optional[bool] = typer.Option(
        None, "--version", "-v", callback=version_callback, is_eager=True,
        help="Show version and exit"
    ),
):
    """OPENDOX - Automated Technical Documentation Generator."""
    pass

@app.command()
def init(
    repo: str = typer.Argument(
        ..., 
        help="GitHub repository URL or local path"
    ),
    output: Path = typer.Option(
        Path("./docs"),
        "--output", "-o",
        help="Output directory for documentation"
    ),
    config: Optional[Path] = typer.Option(
        None,
        "--config", "-c",
        help="Configuration file path"
    ),
):
    """Initialize documentation for a repository."""
    console.print(Panel.fit(
        f"[bold green]Initializing OPENDOX[/bold green]\n"
        f"Repository: [cyan]{repo}[/cyan]\n"
        f"Output: [cyan]{output}[/cyan]",
        title="OPENDOX Setup"
    ))
    
    # Create output directory
    output.mkdir(parents=True, exist_ok=True)
    console.print("✅ Documentation directory created")
    
    # TODO: Implement repository cloning/validation
    console.print("📦 Repository validation... [dim](coming soon)[/dim]")

@app.command()
def generate(
    path: Path = typer.Argument(Path("."), help="Repository path"),
    output: Path = typer.Option(Path("./docs"), "--output", "-o", help="Output directory"),
    model: str = typer.Option("deepseek-coder:1.3b", "--model", "-m", help="LLM model to use"),
    max_files: int = typer.Option(10, "--max-files", help="Maximum files to process"),
    no_incremental: bool = typer.Option(False, "--no-incremental", help="Force regenerate all files"),
):
    """Generate documentation from code."""
    console.print(f"[bold blue]Generating documentation...[/bold blue]")
    console.print(f"Source: {path}")
    console.print(f"Output: {output}")
    console.print(f"Model: {model}")
    console.print(f"Incremental: {not no_incremental}")
    
    from opendox.core.pipeline import DocumentationPipeline
    
    pipeline = DocumentationPipeline(model=model)
    pipeline.generate(path, output, max_files=max_files, incremental=not no_incremental)
    
    console.print(f"[bold green]Documentation generated in {output}[/bold green]")
    console.print(f"Run 'mkdocs serve' in {output} to view")

@app.command()
def serve(
    port: int = typer.Option(8000, "--port", "-p"),
    host: str = typer.Option("localhost", "--host"),
):
    """Serve documentation locally."""
    console.print(f"[bold magenta]Starting server at http://{host}:{port}[/bold magenta]")
    console.print("[dim]Press Ctrl+C to stop[/dim]")
    # TODO: Implement MkDocs server

@app.command()
def status():
    """Show OPENDOX status and configuration."""
    console.print(Panel.fit(
        "[bold]OPENDOX Status[/bold]\n\n"
        f"Python: [green]{sys.version.split()[0]}[/green]\n"
        f"Platform: [blue]Windows[/blue]\n"
        f"Working Directory: [cyan]{Path.cwd()}[/cyan]",
        title="System Info"
    ))

def main():
    """Main entry point."""
    app()

if __name__ == "__main__":
    main()