import time
import redis
from enum import Enum
from functools import wraps
from flask import jsonify, current_app
from threading import Lock

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(self, failure_threshold=5, reset_timeout=60, half_open_timeout=30):
        self.state = CircuitState.CLOSED
        self.failures = 0
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.half_open_timeout = half_open_timeout
        self.last_failure_time = None
        self.half_open_time = None
        self.lock = Lock()
        
        try:
            self.redis_client = redis.Redis(
                host='localhost',
                port=6379,
                db=0,
                decode_responses=True,
                socket_connect_timeout=2
            )
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
                with self.lock:
                    current_state = self.get_circuit_state()
                    current_time = time.time()

                    if current_state == CircuitState.OPEN:
                        if self.last_failure_time is not None and \
                           (current_time - self.last_failure_time) >= self.reset_timeout:
                            self._transition_to_half_open()
                        else:
                            retry_after = self.reset_timeout
                            if self.last_failure_time is not None:
                                retry_after = max(0, self.reset_timeout - 
                                               int(current_time - self.last_failure_time))
                            return jsonify({
                                'error': 'Service temporarily unavailable',
                                'retry_after': retry_after
                            }), 503

                    if current_state == CircuitState.HALF_OPEN:
                        if self.half_open_time is not None and \
                           (current_time - self.half_open_time) >= self.half_open_timeout:
                            self._transition_to_closed()
                        elif self.failures > 0:
                            self._transition_to_open()
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
            self._transition_to_open()

    def reset(self):
        self.failures = 0
        self._transition_to_closed()

    def _transition_to_open(self):
        self.state = CircuitState.OPEN
        self.last_failure_time = time.time()
        self._update_redis_state()

    def _transition_to_half_open(self):
        self.state = CircuitState.HALF_OPEN
        self.half_open_time = time.time()
        self.failures = 0
        self._update_redis_state()

    def _transition_to_closed(self):
        self.state = CircuitState.CLOSED
        self.failures = 0
        self.last_failure_time = None
        self.half_open_time = None
        self._update_redis_state()

    def _update_redis_state(self):
        if not self.redis_client:
            return
            
        try:
            pipeline = self.redis_client.pipeline()
            pipeline.set('circuit_state', self.state.value)
            
            if self.state == CircuitState.OPEN:
                pipeline.expire('circuit_state', self.reset_timeout)
            elif self.state == CircuitState.HALF_OPEN:
                pipeline.expire('circuit_state', self.half_open_timeout)
                
            pipeline.execute()
        except redis.RedisError as e:
            current_app.logger.error(f"Redis error: {str(e)}")