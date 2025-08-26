from pathlib import Path
from opendox.parsers.python_parser import PythonParser
from opendox.generators.llm_generator import LLMGenerator
from opendox.formats.mkdocs_formatter import MkDocsFormatter
from opendox.core.file_discovery import FileDiscovery

def build_documentation(source_path: Path, output_path: Path):
    discovery = FileDiscovery()
    parser = PythonParser()
    generator = LLMGenerator()
    formatter = MkDocsFormatter(output_path)
    
    # Setup MkDocs
    formatter.create_config("OPENDOX")
    formatter.create_index("OPENDOX", "Automated documentation")
    
    # Process files
    files = discovery.filter_python_files(
        discovery.discover_files(source_path)
    )
    
    for file in files[:5]:  # Limit for testing
        result = parser.parse_file(file)
        if 'error' not in result and result.get('functions'):
            docs = []
            for func in result['functions'][:3]:
                doc = generator.generate_function_doc(func.__dict__)
                docs.append(doc)
            
            formatter.create_module_page(file.stem, result['functions'][:3], docs)
    
    print(f"Documentation created in {output_path}")
    print("Run 'mkdocs serve' in that directory to view")

build_documentation(Path("src/opendox"), Path("docs_output"))