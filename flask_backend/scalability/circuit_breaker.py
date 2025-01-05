# flask_backend/scalability/circuit_breaker.py
import redis
import time
from functools import wraps
from flask import jsonify, current_app
from enum import Enum

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(self, failure_threshold=5, reset_timeout=60):
        self.state = CircuitState.CLOSED
        self.failures = 0
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.last_failure_time = None
        
        # Optional Redis for distributed state
        try:
            self.redis_client = redis.Redis(
                host='localhost',
                port=6379,
                db=0,
                decode_responses=True,
                socket_connect_timeout=2
            )
            # Test connection
            self.redis_client.ping()
        except redis.ConnectionError:
            current_app.logger.warning("Redis not available - using local circuit breaker state")
            self.redis_client = None

    def get_circuit_state(self):
        if not self.redis_client:
            return self.state

        try:
            state = self.redis_client.get('circuit_state')
            return CircuitState(state) if state else CircuitState.CLOSED
        except redis.RedisError:
            return self.state

    def protect(self):
        def decorator(f):
            @wraps(f)
            def wrapped(*args, **kwargs):
                state = self.get_circuit_state()
                
                if state == CircuitState.OPEN:
                    return jsonify({
                        'error': 'Service temporarily unavailable',
                        'retry_after': self.reset_timeout
                    }), 503

                try:
                    result = f(*args, **kwargs)
                    self.reset()
                    return result
                except Exception as e:
                    self.record_failure()
                    raise

            return wrapped
        return decorator

    def record_failure(self):
        self.failures += 1
        if self.failures >= self.failure_threshold:
            self.state = CircuitState.OPEN
            self.last_failure_time = time.time()
            
            if self.redis_client:
                try:
                    self.redis_client.set('circuit_state', self.state.value)
                    self.redis_client.expire('circuit_state', self.reset_timeout)
                except redis.RedisError as e:
                    current_app.logger.error(f"Redis error: {str(e)}")

    def reset(self):
        self.failures = 0
        self.state = CircuitState.CLOSED
        self.last_failure_time = None

        if self.redis_client:
            try:
                self.redis_client.set('circuit_state', self.state.value)
            except redis.RedisError as e:
                current_app.logger.error(f"Redis error: {str(e)}")