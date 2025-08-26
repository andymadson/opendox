"""Base parser interface."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class CodeElement:
    """Represents a code element (function, class, etc)."""
    name: str
    type: str
    line_start: int
    line_end: Optional[int] = None
    docstring: Optional[str] = None
    signature: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class BaseParser(ABC):
    """Abstract base parser for all language parsers."""
    
    def __init__(self):
        self.elements: List[CodeElement] = []
    
    @abstractmethod
    def parse_file(self, file_path: Path) -> Dict[str, Any]:
        """Parse a single file and extract elements."""
        pass
    
    @abstractmethod
    def extract_functions(self, content: str) -> List[CodeElement]:
        """Extract function definitions."""
        pass
    
    @abstractmethod
    def extract_classes(self, content: str) -> List[CodeElement]:
        """Extract class definitions."""
        pass
    
    def can_parse(self, file_path: Path) -> bool:
        """Check if this parser can handle the file."""
        return file_path.suffix in self.supported_extensions
    
    @property
    @abstractmethod
    def supported_extensions(self) -> List[str]:
        """Return list of supported file extensions."""
        pass
