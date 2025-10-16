from abc import ABC, abstractmethod


class CacheServiceInterface(ABC):
    @abstractmethod
    async def get(self, key):
        raise NotImplementedError

    @abstractmethod
    async def set(self, key, value, ttl: int | None = None):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, key):
        raise NotImplementedError

    @abstractmethod
    def __getitem__(self, key):
        raise NotImplementedError

    @abstractmethod
    def __setitem__(self, key, value, ttl: int | None = None):
        raise NotImplementedError

    @abstractmethod
    def __delitem__(self, key):
        raise NotImplementedError
