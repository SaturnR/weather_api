import json
from typing import Any, Optional

from redis.asyncio import Redis


class RedisCache:
    def __init__(self, redis_url: str) -> None:
        self._redis = Redis.from_url(redis_url, decode_responses=True)

    async def get(self, key: str) -> Optional[dict[str, Any]]:
        """
        Retrieve cached value by key.
        Returns None if key does not exist.
        """
        value = await self._redis.get(key)
        if value is None:
            return None

        return json.loads(value)

    async def set(
        self,
        key: str,
        value: dict[str, Any],
        ttl: int,
    ) -> None:
        """
        Store value in Redis with TTL (seconds).
        """
        serialized = json.dumps(value)
        await self._redis.set(key, serialized, ex=ttl)

    async def close(self) -> None:
        await self._redis.aclose()
