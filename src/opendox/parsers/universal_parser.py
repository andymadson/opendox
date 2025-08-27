"""Universal parser using Tree-sitter for multiple languages."""
from pathlib import Path
from typing import Dict, Any, List, Optional
import ast  # Fallback for Python parsing

try:
    import tree_sitter_languages as tsl
    from tree_sitter import Node
    TREESITTER_AVAILABLE = True
except ImportError:
    TREESITTER_AVAILABLE = False
    tsl = None
    Node = None

class UniversalParser:
    """Parse multiple languages using Tree-sitter."""
    
    def __init__(self):
        self.available = False
        self.parsers = {}
        
        if not TREESITTER_AVAILABLE:
            self.supported_extensions = ['.py']
            return
        
        try:
            # Get language parsers from tree-sitter-languages
            self.parsers = {
                '.py': tsl.get_language('python'),
                '.js': tsl.get_language('javascript'),
                '.jsx': tsl.get_language('javascript'),
                '.ts': tsl.get_language('typescript'),
                '.tsx': tsl.get_language('tsx'),
                '.go': tsl.get_language('go'),
                '.rs': tsl.get_language('rust'),
                '.java': tsl.get_language('java'),
                '.cpp': tsl.get_language('cpp'),
                '.c': tsl.get_language('c'),
            }
            
            # Get parsers for queries
            self.parser_objects = {
                ext: tsl.get_parser(lang)
                for ext, lang in {
                    '.py': 'python',
                    '.js': 'javascript',
                    '.jsx': 'javascript',
                    '.ts': 'typescript',
                    '.tsx': 'tsx',
                    '.go': 'go',
                    '.rs': 'rust',
                    '.java': 'java',
                    '.cpp': 'cpp',
                    '.c': 'c',
                }.items()
            }
            
            self.supported_extensions = list(self.parsers.keys())
            self.available = True
            
        except Exception as e:
            print(f"Tree-sitter initialization failed: {e}")
            self.supported_extensions = ['.py']
            self.available = False
    
    def parse_file(self, file_path: Path) -> Dict[str, Any]:
        """Parse file using Tree-sitter or fallback to AST for Python."""
        
        # Always support Python with AST fallback
        if file_path.suffix == '.py' and not self.available:
            return self._parse_python_fallback(file_path)
        
        if not self.available:
            return {'error': 'Tree-sitter not available', 'file': str(file_path)}
        
        if file_path.suffix not in self.supported_extensions:
            return {'error': f'Unsupported file type: {file_path.suffix}', 'file': str(file_path)}
        
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            
            # Parse with tree-sitter-languages
            parser = self.parser_objects[file_path.suffix]
            tree = parser.parse(content)
            
            # Extract functions and classes based on language
            if file_path.suffix == '.py':
                return self._extract_python(tree, content, file_path)
            elif file_path.suffix in ['.js', '.jsx', '.ts', '.tsx']:
                return self._extract_javascript(tree, content, file_path)
            elif file_path.suffix == '.go':
                return self._extract_go(tree, content, file_path)
            elif file_path.suffix == '.rs':
                return self._extract_rust(tree, content, file_path)
            elif file_path.suffix == '.java':
                return self._extract_java(tree, content, file_path)
            elif file_path.suffix in ['.c', '.cpp']:
                return self._extract_c_cpp(tree, content, file_path)
            else:
                return {
                    'functions': [],
                    'classes': [],
                    'file': str(file_path),
                    'language': file_path.suffix[1:]
                }
                
        except Exception as e:
            return {'error': str(e), 'file': str(file_path)}
    
    def _parse_python_fallback(self, file_path: Path) -> Dict[str, Any]:
        """Fallback Python parsing using AST."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            functions = []
            classes = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append({
                        'name': node.name,
                        'line_start': node.lineno,
                        'metadata': {
                            'args': [arg.arg for arg in node.args.args]
                        },
                        'docstring': ast.get_docstring(node)
                    })
                elif isinstance(node, ast.ClassDef):
                    classes.append({
                        'name': node.name,
                        'line_start': node.lineno,
                        'docstring': ast.get_docstring(node)
                    })
            
            return {
                'functions': functions,
                'classes': classes,
                'file': str(file_path),
                'language': 'python'
            }
        except Exception as e:
            return {'error': str(e), 'file': str(file_path)}
    
    def _extract_python(self, tree, content: bytes, file_path: Path) -> Dict[str, Any]:
        """Extract Python elements from tree."""
        functions = []
        classes = []
        
        def traverse(node):
            if node.type == 'function_definition':
                name_node = node.child_by_field_name('name')
                if name_node:
                    name = content[name_node.start_byte:name_node.end_byte].decode('utf-8')
                    
                    # Get parameters
                    params_node = node.child_by_field_name('parameters')
                    params = []
                    if params_node:
                        for child in params_node.children:
                            if child.type == 'identifier':
                                params.append(content[child.start_byte:child.end_byte].decode('utf-8'))
                    
                    functions.append({
                        'name': name,
                        'line_start': name_node.start_point[0] + 1,
                        'metadata': {'args': params},
                        'docstring': self._extract_docstring(node, content)
                    })
            
            elif node.type == 'class_definition':
                name_node = node.child_by_field_name('name')
                if name_node:
                    name = content[name_node.start_byte:name_node.end_byte].decode('utf-8')
                    classes.append({
                        'name': name,
                        'line_start': name_node.start_point[0] + 1,
                        'docstring': self._extract_docstring(node, content)
                    })
            
            for child in node.children:
                traverse(child)
        
        traverse(tree.root_node)
        
        return {
            'functions': functions,
            'classes': classes,
            'file': str(file_path),
            'language': 'python'
        }
    
    def _extract_javascript(self, tree, content: bytes, file_path: Path) -> Dict[str, Any]:
        """Extract JavaScript/TypeScript elements."""
        functions = []
        classes = []
        
        def traverse(node):
            if node.type in ['function_declaration', 'function', 'arrow_function', 'method_definition']:
                name_node = node.child_by_field_name('name')
                if name_node:
                    name = content[name_node.start_byte:name_node.end_byte].decode('utf-8')
                elif node.parent and node.parent.type == 'variable_declarator':
                    # Arrow function assigned to variable
                    name_node = node.parent.child_by_field_name('name')
                    if name_node:
                        name = content[name_node.start_byte:name_node.end_byte].decode('utf-8')
                    else:
                        name = 'anonymous'
                else:
                    name = 'anonymous'
                
                functions.append({
                    'name': name,
                    'line_start': node.start_point[0] + 1,
                    'metadata': {'args': []},
                    'type': node.type
                })
            
            elif node.type in ['class_declaration', 'class']:
                name_node = node.child_by_field_name('name')
                if name_node:
                    name = content[name_node.start_byte:name_node.end_byte].decode('utf-8')
                    classes.append({
                        'name': name,
                        'line_start': name_node.start_point[0] + 1
                    })
            
            for child in node.children:
                traverse(child)
        
        traverse(tree.root_node)
        
        return {
            'functions': functions,
            'classes': classes,
            'file': str(file_path),
            'language': 'javascript' if file_path.suffix in ['.js', '.jsx'] else 'typescript'
        }
    
    def _extract_go(self, tree, content: bytes, file_path: Path) -> Dict[str, Any]:
        """Extract Go elements."""
        functions = []
        
        def traverse(node):
            if node.type == 'function_declaration':
                name_node = node.child_by_field_name('name')
                if name_node:
                    name = content[name_node.start_byte:name_node.end_byte].decode('utf-8')
                    functions.append({
                        'name': name,
                        'line_start': name_node.start_point[0] + 1,
                        'metadata': {'args': []}
                    })
            
            for child in node.children:
                traverse(child)
        
        traverse(tree.root_node)
        
        return {
            'functions': functions,
            'classes': [],  # Go doesn't have classes
            'file': str(file_path),
            'language': 'go'
        }
    
    def _extract_rust(self, tree, content: bytes, file_path: Path) -> Dict[str, Any]:
        """Extract Rust elements."""
        functions = []
        structs = []
        
        def traverse(node):
            if node.type == 'function_item':
                name_node = node.child_by_field_name('name')
                if name_node:
                    name = content[name_node.start_byte:name_node.end_byte].decode('utf-8')
                    functions.append({
                        'name': name,
                        'line_start': name_node.start_point[0] + 1,
                        'metadata': {'args': []}
                    })
            elif node.type == 'struct_item':
                name_node = node.child_by_field_name('name')
                if name_node:
                    name = content[name_node.start_byte:name_node.end_byte].decode('utf-8')
                    structs.append({
                        'name': name,
                        'line_start': name_node.start_point[0] + 1
                    })
            
            for child in node.children:
                traverse(child)
        
        traverse(tree.root_node)
        
        return {
            'functions': functions,
            'classes': structs,  # Treating structs as classes
            'file': str(file_path),
            'language': 'rust'
        }
    
    def _extract_java(self, tree, content: bytes, file_path: Path) -> Dict[str, Any]:
        """Extract Java elements."""
        functions = []
        classes = []
        
        def traverse(node):
            if node.type == 'method_declaration':
                name_node = node.child_by_field_name('name')
                if name_node:
                    name = content[name_node.start_byte:name_node.end_byte].decode('utf-8')
                    functions.append({
                        'name': name,
                        'line_start': name_node.start_point[0] + 1,
                        'metadata': {'args': []}
                    })
            elif node.type == 'class_declaration':
                name_node = node.child_by_field_name('name')
                if name_node:
                    name = content[name_node.start_byte:name_node.end_byte].decode('utf-8')
                    classes.append({
                        'name': name,
                        'line_start': name_node.start_point[0] + 1
                    })
            
            for child in node.children:
                traverse(child)
        
        traverse(tree.root_node)
        
        return {
            'functions': functions,
            'classes': classes,
            'file': str(file_path),
            'language': 'java'
        }
    
    def _extract_c_cpp(self, tree, content: bytes, file_path: Path) -> Dict[str, Any]:
        """Extract C/C++ elements."""
        functions = []
        classes = []
        
        def traverse(node):
            if node.type == 'function_definition':
                # Find function name in declarator
                declarator = node.child_by_field_name('declarator')
                if declarator:
                    name_node = declarator.child_by_field_name('declarator')
                    if name_node and name_node.type == 'identifier':
                        name = content[name_node.start_byte:name_node.end_byte].decode('utf-8')
                        functions.append({
                            'name': name,
                            'line_start': name_node.start_point[0] + 1,
                            'metadata': {'args': []}
                        })
            elif node.type == 'class_specifier' and file_path.suffix == '.cpp':
                name_node = node.child_by_field_name('name')
                if name_node:
                    name = content[name_node.start_byte:name_node.end_byte].decode('utf-8')
                    classes.append({
                        'name': name,
                        'line_start': name_node.start_point[0] + 1
                    })
            
            for child in node.children:
                traverse(child)
        
        traverse(tree.root_node)
        
        return {
            'functions': functions,
            'classes': classes,
            'file': str(file_path),
            'language': 'c' if file_path.suffix == '.c' else 'cpp'
        }
    
    def _extract_docstring(self, node, content: bytes) -> Optional[str]:
        """Extract docstring from a Python function or class."""
        body = node.child_by_field_name('body')
        if body and body.children:
            first_stmt = body.children[0]
            if first_stmt.type == 'expression_statement':
                expr = first_stmt.children[0] if first_stmt.children else None
                if expr and expr.type == 'string':
                    docstring = content[expr.start_byte:expr.end_byte].decode('utf-8')
                    # Clean up the docstring
                    return docstring.strip('"""').strip("'''").strip()
        return None