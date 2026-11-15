import time
from typing import Any, Optional

class TTLCache:
    def __init__(self, ttl_seconds: int):
        self.ttl = ttl_seconds
        self.store = {}

    def get(self, key: str) -> Optional[Any]:
        if key in self.store:
            value, timestamp = self.store[key]
            if time.time() - timestamp < self.ttl:
                return value
            else:
                del self.store[key]
        return None

    def set(self, key: str, value: Any):
        self.store[key] = (value, time.time())

cache = TTLCache(ttl_seconds=600)
