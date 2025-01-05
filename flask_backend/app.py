# flask_backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from scalability.cache import CacheService
from scalability.rate_limiter import RateLimiter
from scalability.circuit_breaker import CircuitBreaker

app = Flask(__name__)
CORS(app)

# Initialize services with error handling
cache_service = CacheService()
rate_limiter = RateLimiter()
circuit_breaker = CircuitBreaker()

@app.route('/api/translate', methods=['POST'])
@rate_limiter.limit(100, 60)  # 100 requests per minute
@circuit_breaker.protect()
def translate():
    try:
        data = request.get_json()
        text = data.get('text')
        source_lang = data.get('sourceLang', 'auto')
        target_lang = data.get('targetLang', 'en')

        # Create cache key
        cache_key = f"translation:{text}:{source_lang}:{target_lang}"

        def translate_text():
            # Your translation logic here
            return {
                "text": text,
                "translated": f"Translated: {text}",
                "source_lang": source_lang,
                "target_lang": target_lang
            }

        # Use cache with fallback
        result = cache_service.cache_with_fallback(
            cache_key,
            translate_text,
            expires=3600  # Cache for 1 hour
        )

        return jsonify(result)

    except Exception as e:
        app.logger.error(f"Translation error: {str(e)}")
        return jsonify({
            "error": "Translation failed",
            "details": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)