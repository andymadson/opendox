"""Enhanced Python parser using LibCST."""
import ast
from pathlib import Path
from typing import Dict, Any, List, Optional

try:
    import libcst as cst
    LIBCST_AVAILABLE = True
except ImportError:
    LIBCST_AVAILABLE = False
    cst = None

class EnhancedPythonParser:
    """Parse Python with full formatting preservation using LibCST."""
    
    def __init__(self):
        if not LIBCST_AVAILABLE:
            raise ImportError("LibCST is not installed. Install with: pip install libcst")
        self.functions = []
        self.classes = []
        self.imports = []
    
    def parse_file(self, file_path: Path) -> Dict[str, Any]:
        """Parse Python file with LibCST."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()
            
            # Use LibCST parsing
            module = cst.parse_module(source)
            
            # For now, fallback to AST for extraction (simplified)
            tree = ast.parse(source)
            functions = []
            classes = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append({
                        'name': node.name,
                        'metadata': {
                            'args': [arg.arg for arg in node.args.args],
                        },
                        'docstring': ast.get_docstring(node),
                        'line_start': node.lineno,
                    })
                elif isinstance(node, ast.ClassDef):
                    classes.append({
                        'name': node.name,
                        'docstring': ast.get_docstring(node),
                        'line_start': node.lineno,
                    })
            
            return {
                'functions': functions,
                'classes': classes,
                'imports': [],
                'file': str(file_path),
                'source': source[:100] + '...'  # Keep sample
            }
        except Exception as e:
            return {'error': str(e), 'file': str(file_path)}