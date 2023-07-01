import redis  # type: ignore[import]

from core.config import settings

jwt_redis_blocklist = redis.Redis(host=settings.redis.host, port=settings.redis.port, db=0, decode_responses=True)
