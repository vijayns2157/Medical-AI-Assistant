import json

import redis

from app.config import REDIS_URL


def get_redis():
    return redis.Redis.from_url(
        REDIS_URL,
        decode_responses=True,
    )


def get_cached_answer(question: str):
    redis_client = get_redis()

    cache_key = f"medical_rag:{question.strip().lower()}"

    cached = redis_client.get(cache_key)

    if cached:
        return json.loads(cached)

    return None


def set_cached_answer(question: str, result: dict, ttl: int = 3600):
    redis_client = get_redis()

    cache_key = f"medical_rag:{question.strip().lower()}"

    redis_client.setex(
        cache_key,
        ttl,
        json.dumps(result, default=str),
    )