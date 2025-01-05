# flask_backend/scalability/rate_limiter.py
import redis
import time
from functools import wraps
from flask import request, jsonify, current_app

class RateLimiter:
    def __init__(self, redis_host='localhost', redis_port=6379, db=0):
        try:
            self.redis_client = redis.Redis(
                host=redis_host,
                port=redis_port,
                db=db,
                decode_responses=True,
                socket_connect_timeout=2
            )
            # Test connection
            self.redis_client.ping()
        except redis.ConnectionError:
            current_app.logger.warning("Redis not available - rate limiting disabled")
            self.redis_client = None

    def limit(self, max_requests=100, window=60):
        def decorator(f):
            @wraps(f)
            def wrapped(*args, **kwargs):
                if not self.redis_client:
                    return f(*args, **kwargs)

                try:
                    key = f'rate_limit:{request.remote_addr}'
                    requests = self.redis_client.get(key)

                    if requests is None:
                        self.redis_client.setex(key, window, 1)
                    else:
                        requests = int(requests)
                        if requests >= max_requests:
                            return jsonify({
                                'error': 'Rate limit exceeded',
                                'retry_after': self.redis_client.ttl(key)
                            }), 429
                        self.redis_client.incr(key)

                    return f(*args, **kwargs)
                except redis.RedisError as e:
                    current_app.logger.error(f"Rate limiting error: {str(e)}")
                    return f(*args, **kwargs)
            return wrapped
        return decorator