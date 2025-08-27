"""Redis cache manager for documentation."""
import hashlib
from typing import Optional

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    redis = None

class DocumentationCache:
    """Cache documentation with Redis."""
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.enabled = False
        self.memory_cache = {}
        
        if REDIS_AVAILABLE:
            try:
                self.redis_client = redis.from_url(redis_url)
                self.redis_client.ping()
                self.enabled = True
            except:
                pass
    
    def get_cached_doc(self, code_hash: str) -> Optional[str]:
        """Get cached documentation for code snippet."""
        if self.enabled:
            try:
                doc = self.redis_client.get(f"doc:{code_hash}")
                return doc.decode() if doc else None
            except:
                pass
        return self.memory_cache.get(code_hash)
    
    def cache_doc(self, code: str, documentation: str, ttl: int = 86400):
        """Cache generated documentation."""
        code_hash = hashlib.md5(code.encode()).hexdigest()
        
        if self.enabled:
            try:
                self.redis_client.setex(f"doc:{code_hash}", ttl, documentation)
            except:
                self.memory_cache[code_hash] = documentation
        else:
            self.memory_cache[code_hash] = documentation