"""Discover and filter source files in a repository."""
from pathlib import Path
from typing import List, Set

class FileDiscovery:
    """Find relevant source files for documentation."""
    
    DEFAULT_EXTENSIONS = {
        '.py', '.js', '.ts', '.jsx', '.tsx',
        '.java', '.cpp', '.c', '.h', '.hpp',
        '.go', '.rs', '.rb', '.php'
    }
    
    DEFAULT_IGNORE = {
        '__pycache__', 'node_modules', '.git',
        'venv', '.venv', 'dist', 'build',
        '.pytest_cache', '.mypy_cache'
    }
    
    def __init__(self, extensions: Set[str] = None, ignore: Set[str] = None):
        self.extensions = extensions or self.DEFAULT_EXTENSIONS
        self.ignore = ignore or self.DEFAULT_IGNORE
    
    def discover_files(self, root_path: Path, max_files: int = 1000) -> List[Path]:
        """Find all source files in the repository."""
        files = []
        for path in root_path.rglob('*'):
            if len(files) >= max_files:
                break
            if path.is_file() and path.suffix in self.extensions:
                # Check if path contains ignored directories
                if not any(ignored in path.parts for ignored in self.ignore):
                    files.append(path)
        return files
    
    def filter_python_files(self, files: List[Path]) -> List[Path]:
        """Get only Python files from the list."""
        return [f for f in files if f.suffix == '.py']
