import time
from typing import Optional, Callable, Any, List, Tuple, Union
import redis
from functools import wraps
from flask import request, current_app

class RateLimiter:
    def __init__(self, redis_host: str = 'localhost', redis_port: int = 6379, db: int = 0):
        self.redis_client: Optional[redis.Redis] = None
        self._local_cache = {}
        
        try:
            redis_client = redis.Redis(
                host=redis_host,
                port=redis_port,
                db=db,
                decode_responses=True,
                socket_connect_timeout=2
            )
            # Test connection
            redis_client.ping()
            self.redis_client = redis_client
        except redis.ConnectionError:
            current_app.logger.warning("Redis not available - using in-memory fallback")

    def limit(self, max_requests: int = 100, window: int = 60) -> Callable:
        def decorator(f: Callable) -> Callable:
            @wraps(f)
            def wrapped(*args: Any, **kwargs: Any) -> Any:
                if not self.redis_client:
                    return self._local_rate_limit(f, max_requests, window, *args, **kwargs)
                    
                try:
                    key = f'rate_limit:{request.remote_addr}'
                    current = time.time()
                    
                    # Clean old requests and count current ones in a pipeline
                    pipeline = self.redis_client.pipeline()
                    pipeline.zremrangebyscore(key, 0, current - window)
                    pipeline.zadd(key, {str(current): current})
                    pipeline.zcount(key, '-inf', '+inf')
                    pipeline.expire(key, window)
                    
                    _, _, requests_count, _ = pipeline.execute()
                    
                    if requests_count > max_requests:
                        retry_after = window
                        
                        try:
                            # Get oldest timestamp - handle Redis response type safely
                            oldest_entries = self.redis_client.zrange(
                                key, 
                                0, 
                                0, 
                                withscores=True,
                                score_cast_func=float
                            )
                            
                            if oldest_entries and isinstance(oldest_entries, list):
                                # Each entry is a tuple of (member, score)
                                oldest_entry = oldest_entries[0]
                                if isinstance(oldest_entry, tuple) and len(oldest_entry) == 2:
                                    oldest_timestamp = oldest_entry[1]  # Use the score (timestamp)
                                    retry_after = int(window - (current - oldest_timestamp))
                        except (IndexError, ValueError, TypeError) as e:
                            current_app.logger.error(f"Error processing rate limit timestamp: {str(e)}")
                            # Fall back to default window value
                            retry_after = window
                            
                        return {
                            'error': 'Rate limit exceeded',
                            'retry_after': max(0, retry_after)
                        }, 429
                        
                    return f(*args, **kwargs)
                    
                except redis.RedisError as e:
                    current_app.logger.error(f"Rate limiting error: {str(e)}")
                    return f(*args, **kwargs)
                    
            return wrapped
        return decorator
        
    def _local_rate_limit(self, f: Callable, max_requests: int, window: int, *args: Any, **kwargs: Any) -> Any:
        key = f'rate_limit:{request.remote_addr}'
        current = time.time()
        
        if key not in self._local_cache:
            self._local_cache[key] = []
            
        # Clean expired timestamps
        self._local_cache[key] = [ts for ts in self._local_cache[key] 
                                 if current - ts <= window]
        
        if len(self._local_cache[key]) >= max_requests:
            retry_after = window
            if self._local_cache[key]:
                retry_after = int(window - (current - self._local_cache[key][0]))
                
            return {
                'error': 'Rate limit exceeded',
                'retry_after': max(0, retry_after)
            }, 429
            
        self._local_cache[key].append(current)
        return f(*args, **kwargs)