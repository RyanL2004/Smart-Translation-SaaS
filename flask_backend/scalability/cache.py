# flask_backend/scalability/cache.py
import redis
from functools import wraps
import json
from flask import current_app

class CacheService:
    def __init__(self, host='localhost', port=6379, db=0):
        try:
            self.redis_client = redis.Redis(
                host=host,
                port=port,
                db=db,
                decode_responses=True,
                socket_connect_timeout=2
            )
            # Test connection
            self.redis_client.ping()
        except redis.ConnectionError:
            current_app.logger.warning("Redis not available - caching disabled")
            self.redis_client = None

    def cache_with_fallback(self, key, callback, expires=3600):
        if not self.redis_client:
            return callback()

        try:
            cached_data = self.redis_client.get(key)
            if cached_data:
                return json.loads(cached_data)

            fresh_data = callback()
            self.redis_client.setex(key, expires, json.dumps(fresh_data))
            return fresh_data
        except (redis.RedisError, json.JSONDecodeError) as e:
            current_app.logger.error(f"Cache error: {str(e)}")
            return callback()