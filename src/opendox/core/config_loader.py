# src/opendox/core/config_loader.py
import yaml
from pathlib import Path
from typing import Dict, Any

class OpendoxConfig:
    def __init__(self, config_path: Path = None):
        self.config = self.load_config(config_path)
    
    def load_config(self, config_path: Path = None) -> Dict:
        """Load configuration from file or defaults."""
        if config_path and config_path.exists():
            with open(config_path) as f:
                return yaml.safe_load(f)
        
        # Check for .opendox.yml in current directory
        default_path = Path('.opendox.yml')
        if default_path.exists():
            with open(default_path) as f:
                return yaml.safe_load(f)
        
        # Return defaults
        return {
            'llm': {'model': 'deepseek-coder:1.3b', 'max_tokens': 200},
            'ignore': ['tests/', 'test/', '__pycache__/', '.git/'],
            'output': {'format': 'mkdocs', 'theme': 'material'},
        }