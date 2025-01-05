class Config:
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    RATE_LIMIT_DEFAULT = 100  # requests per window
    RATE_LIMIT_WINDOW = 900   # 15 minutes in seconds
    CIRCUIT_BREAKER_THRESHOLD = 5
    CIRCUIT_BREAKER_TIMEOUT = 60