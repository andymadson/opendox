# Create targeted_docs.py
from pathlib import Path
from opendox.core.pipeline import DocumentationPipeline

# Target specific important files
important_files = [
    "src/opendox/cli/main.py",
    "src/opendox/core/pipeline.py",
    "src/opendox/parsers/python_parser.py",
    "src/opendox/generators/llm_generator.py",
    "src/opendox/formats/mkdocs_formatter.py",
]

pipeline = DocumentationPipeline(model="deepseek-coder:6.7b")

# Process each important file
for file_path in important_files:
    file = Path(file_path)
    if file.exists():
        print(f"Documenting {file.name}...")
        # Process it (you'll need to modify pipeline to accept single files)