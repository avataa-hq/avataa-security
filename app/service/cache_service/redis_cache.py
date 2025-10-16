import redis

from service.cache_service.cache_interface import CacheServiceInterface


class RedisCache(CacheServiceInterface):
    def __init__(
        self,
        host: str,
        port: int,
        db: int,
        username=None,
        password=None,
        max_ttl: int | None = 60,
    ):
        self.host: str = host
        self.port: int = port
        self.db: int = db
        self.username: str = username
        self.password: str = password
        self.max_ttl: int | None = max_ttl
        self._client: redis.Redis | None = None
        self._async_client: redis.asyncio.client.Redis | None = None

    @property
    def client(self) -> redis.Redis:
        if self._client is None:
            self._client = redis.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                username=self.username,
                password=self.password,
            )
        return self._client

    @property
    def async_client(self) -> redis.asyncio.client.Redis:
        if self._async_client is None:
            self._async_client = redis.asyncio.client.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                username=self.username,
                password=self.password,
            )
        return self._async_client

    async def get(self, key):
        return await self.async_client.get(key)

    async def set(self, key, value, ttl: int | None = None):
        if ttl is None:
            ttl = self.max_ttl
        else:
            ttl = min(ttl, self.max_ttl)
        await self.async_client.set(key, value, ex=ttl)
        return self

    async def delete(self, key):
        await self.async_client.delete(key)
        return self

    def __getitem__(self, key):
        return self.client.get(key)

    def __setitem__(self, key, value, ttl: int | None = None):
        if ttl is None:
            ttl = self.max_ttl
        else:
            ttl = min(ttl, self.max_ttl)
        self.client.set(key, value, ex=ttl)

    def __delitem__(self, key):
        self.client.delete(key)
        return self
