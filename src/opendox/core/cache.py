# src/opendox/core/cache.py
import json
import hashlib
from pathlib import Path
from typing import Dict, Optional

class DocumentationCache:
    def __init__(self, project_root: Path, output_dir: Path = None):
        self.cache_dir = project_root / '.opendox'
        self.cache_file = self.cache_dir / 'cache.json'
        self.cache_dir.mkdir(exist_ok=True)
        self.cache = self._load_cache()
        self.output_dir = output_dir
    
    def _load_cache(self) -> Dict:
        if self.cache_file.exists():
            try:
                return json.loads(self.cache_file.read_text())
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def get_file_hash(self, file_path: Path) -> str:
        """Generate hash of file content."""
        try:
            content = file_path.read_bytes()
            return hashlib.md5(content).hexdigest()
        except (IOError, OSError):
            return ""
    
    def needs_update(self, file_path: Path) -> bool:
        """Check if file has changed since last generation or if output doesn't exist."""
        # Always regenerate if output directory doesn't exist
        if self.output_dir and not self.output_dir.exists():
            return True
            
        # Check if the documentation file exists
        if self.output_dir:
            doc_file = self.output_dir / "docs" / "api" / f"{file_path.stem}.md"
            if not doc_file.exists():
                return True
        
        # Check if source file has changed
        current_hash = self.get_file_hash(file_path)
        cached_hash = self.cache.get(str(file_path))
        return current_hash != cached_hash
    
    def update(self, file_path: Path):
        """Mark file as processed."""
        self.cache[str(file_path)] = self.get_file_hash(file_path)
        self.save()
    
    def save(self):
        """Save cache to disk."""
        try:
            self.cache_file.write_text(json.dumps(self.cache, indent=2))
        except (IOError, OSError):
            pass  # Fail silently if cache can't be saved
    
    def clear(self):
        """Clear all cache entries."""
        self.cache = {}
        self.save()
    
    def remove_entry(self, file_path: Path):
        """Remove a specific file from cache."""
        self.cache.pop(str(file_path), None)
        self.save()