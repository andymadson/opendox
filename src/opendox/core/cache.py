# src/opendox/core/cache.py
import json
import hashlib
from pathlib import Path
from typing import Dict, Optional

class DocumentationCache:
    def __init__(self, project_root: Path):
        self.cache_dir = project_root / '.opendox'
        self.cache_file = self.cache_dir / 'cache.json'
        self.cache_dir.mkdir(exist_ok=True)
        self.cache = self._load_cache()
    
    def _load_cache(self) -> Dict:
        if self.cache_file.exists():
            return json.loads(self.cache_file.read_text())
        return {}
    
    def get_file_hash(self, file_path: Path) -> str:
        """Generate hash of file content."""
        content = file_path.read_bytes()
        return hashlib.md5(content).hexdigest()
    
    def needs_update(self, file_path: Path) -> bool:
        """Check if file has changed since last generation."""
        current_hash = self.get_file_hash(file_path)
        cached_hash = self.cache.get(str(file_path))
        return current_hash != cached_hash
    
    def update(self, file_path: Path):
        """Mark file as processed."""
        self.cache[str(file_path)] = self.get_file_hash(file_path)
        self.save()
    
    def save(self):
        self.cache_file.write_text(json.dumps(self.cache, indent=2))