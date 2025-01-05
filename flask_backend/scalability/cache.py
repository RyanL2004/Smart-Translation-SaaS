import redis
import json
from typing import Optional, Callable, Any, Dict, Union
from functools import wraps
from flask import current_app

class CacheService:
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0):
        self.redis_client: Optional[redis.Redis] = None
        
        try:
            redis_client = redis.Redis(
                host=host,
                port=port,
                db=db,
                decode_responses=True,
                socket_connect_timeout=2
            )
            # Test connection
            redis_client.ping()
            self.redis_client = redis_client
        except redis.ConnectionError:
            current_app.logger.warning("Redis not available - caching disabled")

    def cache_with_fallback(self, 
                          key: str, 
                          callback: Callable[[], Any], 
                          expires: int = 3600) -> Any:
        """
        Cache function results with proper error handling
        
        Args:
            key: Cache key
            callback: Function to call if cache miss
            expires: Cache expiration in seconds
            
        Returns:
            Cached or fresh data from callback
        """
        if not self.redis_client:
            return callback()

        try:
            # Try to get cached data
            cached_data = self.redis_client.get(key)
            
            if cached_data is not None:
                try:
                    # Since we use decode_responses=True, cached_data will be str
                    return json.loads(str(cached_data))
                except json.JSONDecodeError:
                    current_app.logger.error(f"Failed to decode cached data for key: {key}")
                    # If cached data is corrupted, get fresh data
                    return self._get_fresh_data(key, callback, expires)
            
            # Cache miss - get fresh data
            return self._get_fresh_data(key, callback, expires)
            
        except redis.RedisError as e:
            current_app.logger.error(f"Cache error: {str(e)}")
            return callback()
            
    def _get_fresh_data(self, 
                       key: str, 
                       callback: Callable[[], Any], 
                       expires: int) -> Any:
        """Get fresh data and cache it"""
        fresh_data = callback()
        
        if self.redis_client is None:
            return fresh_data
        
        try:
            # Only cache if data is JSON serializable
            cached_str = json.dumps(fresh_data)
            self.redis_client.setex(key, expires, cached_str)
        except (TypeError, json.JSONDecodeError) as e:
            current_app.logger.error(f"Failed to cache data: {str(e)}")
            
        return fresh_data