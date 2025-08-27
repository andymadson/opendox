"""Generate documentation for the sample app."""
from pathlib import Path
import shutil
from opendox.core.pipeline import DocumentationPipeline

# Clear any existing state for sample_app
state_dir = Path("sample_app/.opendox")
if state_dir.exists():
    shutil.rmtree(state_dir)

# Clear output directory
output_dir = Path("sample_docs")
if output_dir.exists():
    shutil.rmtree(output_dir)

# Generate documentation
print("Generating documentation for sample_app...")
pipeline = DocumentationPipeline(model="deepseek-coder:1.3b")
pipeline.generate(
    source_path=Path("sample_app"),
    output_path=output_dir,
    max_files=20,
    incremental=False  # Force processing all files
)

print(f"\n✅ Documentation generated!")
print(f"Run: cd {output_dir} && mkdocs serve")