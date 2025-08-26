"""Configuration management for OPENDOX."""
from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class ModelConfig(BaseModel):
    """LLM model configuration."""
    name: str = "codellama:7b"
    temperature: float = 0.3
    max_tokens: int = 2048
    api_key: Optional[str] = None
    
class ParserConfig(BaseModel):
    """Code parser configuration."""
    languages: List[str] = ["python", "javascript", "typescript"]
    ignore_patterns: List[str] = ["*test*", "*__pycache__*", "*.pyc", "node_modules"]
    max_file_size: int = 1_000_000  # 1MB
    
class OutputConfig(BaseModel):
    """Documentation output configuration."""
    format: str = "mkdocs"  # mkdocs, sphinx, markdown
    theme: str = "material"
    include_source: bool = True
    
class OpendoxSettings(BaseSettings):
    """Main OPENDOX configuration."""
    github_token: Optional[str] = Field(None, env="GITHUB_TOKEN")
    openai_api_key: Optional[str] = Field(None, env="OPENAI_API_KEY")
    cache_enabled: bool = True
    cache_ttl: int = 86400  # 24 hours
    debug: bool = False
    
    model: ModelConfig = ModelConfig()
    parser: ParserConfig = ParserConfig()
    output: OutputConfig = OutputConfig()
    
    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"
        case_sensitive = False

# Global settings instance
settings = OpendoxSettings()
