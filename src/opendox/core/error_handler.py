# src/opendox/core/error_handler.py
from typing import List, Dict
from rich.console import Console
from rich.table import Table

class ErrorCollector:
    def __init__(self):
        self.errors: List[Dict] = []
        self.console = Console()
    
    def add_error(self, file: str, error: str, line: int = None):
        self.errors.append({
            'file': file,
            'error': error,
            'line': line
        })
    
    def report(self):
        if not self.errors:
            return
        
        table = Table(title="Documentation Errors")
        table.add_column("File", style="cyan")
        table.add_column("Error", style="red")
        
        for error in self.errors:
            table.add_row(error['file'], error['error'])
        
        self.console.print(table)