"""Python code parser using AST."""
import ast
from pathlib import Path
from typing import Any, Dict, List

from .base import BaseParser, CodeElement


class PythonParser(BaseParser):
    """Parser for Python source files."""
    
    @property
    def supported_extensions(self) -> List[str]:
        return [".py", ".pyw"]
    
    def parse_file(self, file_path: Path) -> Dict[str, Any]:
        """Parse Python file and extract all elements."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            return {"error": str(e), "file": str(file_path)}
        
        try:
            tree = ast.parse(content, filename=str(file_path))
        except SyntaxError as e:
            return {"error": f"Syntax error: {e}", "file": str(file_path)}
        
        functions = self.extract_functions(tree)
        classes = self.extract_classes(tree)
        
        return {
            "file": str(file_path),
            "language": "python",
            "functions": functions,
            "classes": classes,
            "imports": self._extract_imports(tree),
            "total_lines": len(content.splitlines()),
        }
    
    def extract_functions(self, tree: ast.AST) -> List[CodeElement]:
        """Extract all function definitions."""
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                element = CodeElement(
                    name=node.name,
                    type="function",
                    line_start=node.lineno,
                    line_end=node.end_lineno,
                    docstring=ast.get_docstring(node),
                    signature=self._get_function_signature(node),
                    metadata={
                        "args": [arg.arg for arg in node.args.args],
                        "decorators": [d.id if hasattr(d, "id") else str(d) 
                                     for d in node.decorator_list],
                        "is_async": isinstance(node, ast.AsyncFunctionDef),
                    }
                )
                functions.append(element)
        return functions
    
    def extract_classes(self, tree: ast.AST) -> List[CodeElement]:
        """Extract all class definitions."""
        classes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                methods = [m.name for m in node.body 
                          if isinstance(m, ast.FunctionDef)]
                
                element = CodeElement(
                    name=node.name,
                    type="class",
                    line_start=node.lineno,
                    line_end=node.end_lineno,
                    docstring=ast.get_docstring(node),
                    metadata={
                        "methods": methods,
                        "bases": [self._get_name(base) for base in node.bases],
                        "decorators": [d.id if hasattr(d, "id") else str(d) 
                                     for d in node.decorator_list],
                    }
                )
                classes.append(element)
        return classes
    
    def _extract_imports(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Extract import statements."""
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append({
                        "module": alias.name,
                        "alias": alias.asname,
                        "type": "import"
                    })
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    imports.append({
                        "module": node.module,
                        "name": alias.name,
                        "alias": alias.asname,
                        "type": "from"
                    })
        return imports
    
    def _get_function_signature(self, node: ast.FunctionDef) -> str:
        """Extract function signature as string."""
        args = []
        for arg in node.args.args:
            arg_str = arg.arg
            if arg.annotation:
                arg_str += f": {ast.unparse(arg.annotation)}"
            args.append(arg_str)
        
        signature = f"{node.name}({', '.join(args)})"
        if node.returns:
            signature += f" -> {ast.unparse(node.returns)}"
        
        return signature
    
    def _get_name(self, node: ast.AST) -> str:
        """Get name from AST node."""
        if hasattr(node, "id"):
            return node.id
        elif hasattr(node, "name"):
            return node.name
        else:
            return ast.unparse(node)
