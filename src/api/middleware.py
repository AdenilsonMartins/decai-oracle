"""
API Middleware - Rate Limiting, Caching, and Circuit Breakers
"""

import time
import json
import functools
from typing import Any, Callable, Optional
from redis import Redis
from slowapi import Limiter
from slowapi.util import get_remote_address
from tenacity import retry, stop_after_attempt, wait_exponential
from src.utils.logger import setup_logger
from src.utils.config import settings

logger = setup_logger(__name__)

# Redis setup for caching and rate limiting
redis_client: Optional[Redis] = None
try:
    redis_client = Redis(host="localhost", port=6379, db=0, decode_responses=True)
    redis_client.ping()
    logger.info("✅ Connected to Redis")
except Exception as e:
    logger.warning(f"⚠️ Redis not available, caching will be disabled: {e}")
    redis_client = None

# Rate Limiter setup
limiter = Limiter(key_func=get_remote_address)

class CacheManager:
    """Manages Redis caching for API responses"""
    
    @staticmethod
    def get(key: str) -> Optional[Any]:
        if not redis_client:
            return None
        data = redis_client.get(key)
        return json.loads(data) if data else None

    @staticmethod
    def set(key: str, value: Any, ttl: int = 300):
        if not redis_client:
            return
        redis_client.setex(key, ttl, json.dumps(value))

def cache_response(ttl: int = 300):
    """Decorator to cache function results in Redis"""
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"cache:{func.__name__}:{args}:{kwargs}"
            cached_val = CacheManager.get(cache_key)
            if cached_val:
                logger.info(f"💾 Cache hit for {cache_key}")
                return cached_val
            
            result = await func(*args, **kwargs)
            CacheManager.set(cache_key, result, ttl)
            return result
        return wrapper
    return decorator

class CircuitBreaker:
    """Simple Circuit Breaker pattern implementation"""
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failures = 0
        self.last_failure_time = 0
        self.state = "CLOSED" # CLOSED, OPEN, HALF_OPEN

    def call(self, func: Callable, *args, **kwargs):
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "HALF_OPEN"
                logger.info("🟠 Circuit Breaker entering HALF_OPEN")
            else:
                logger.error("🔴 Circuit Breaker is OPEN. Request rejected.")
                raise Exception("Circuit Breaker is OPEN")

        try:
            result = func(*args, **kwargs)
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                self.failures = 0
                logger.info("🟢 Circuit Breaker restored to CLOSED")
            return result
        except Exception as e:
            self.failures += 1
            self.last_failure_time = time.time()
            if self.failures >= self.failure_threshold:
                self.state = "OPEN"
                logger.error(f"🔴 Circuit Breaker opened after {self.failures} failures")
            raise e

# Example retry policy for external APIs
remote_api_retry = retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    reraise=True
)
