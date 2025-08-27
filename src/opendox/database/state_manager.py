"""DuckDB state management for documentation."""
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Optional

try:
    import duckdb
    DUCKDB_AVAILABLE = True
except ImportError:
    DUCKDB_AVAILABLE = False
    duckdb = None

class DocumentationStateManager:
    """Manage documentation state with DuckDB."""
    
    def __init__(self, project_root: Path):
        if not DUCKDB_AVAILABLE:
            raise ImportError("DuckDB is not installed. Install with: pip install duckdb")
        
        self.db_path = project_root / '.opendox' / 'state.duckdb'
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = duckdb.connect(str(self.db_path))
        self._initialize_schema()
    
    def _initialize_schema(self):
        """Create tables for tracking documentation state."""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS files (
                file_path VARCHAR PRIMARY KEY,
                content_hash VARCHAR NOT NULL,
                last_parsed TIMESTAMP,
                last_documented TIMESTAMP,
                parse_success BOOLEAN DEFAULT FALSE,
                doc_generated BOOLEAN DEFAULT FALSE
            )
        """)
        
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS documentation_metadata (
                file_path VARCHAR PRIMARY KEY,
                doc_coverage FLOAT,
                quality_score FLOAT,
                last_llm_model VARCHAR,
                generation_time_ms INTEGER
            )
        """)
    
    def get_changed_files(self, since: Optional[datetime] = None) -> List[str]:
        """Get files that need documentation updates."""
        try:
            query = """
                SELECT file_path 
                FROM files 
                WHERE last_parsed > last_documented
                   OR doc_generated = false
                   OR last_documented IS NULL
            """
            result = self.conn.execute(query).fetchall()
            return [row[0] for row in result]
        except:
            # Table might be empty
            return []
    
    def update_file_state(self, file_path: Path, content: str):
        """Update file hash and timestamps."""
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        
        self.conn.execute(
            """
            INSERT INTO files (file_path, content_hash, last_parsed, last_documented, doc_generated)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT (file_path) DO UPDATE SET
                content_hash = EXCLUDED.content_hash,
                last_documented = EXCLUDED.last_documented,
                doc_generated = true
            """,
            (str(file_path), content_hash, datetime.now(), datetime.now(), True)
        )