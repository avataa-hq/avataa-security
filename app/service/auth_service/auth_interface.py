from abc import ABC, abstractmethod


class AuthInterface(ABC):
    @abstractmethod
    async def get_user_info(self, token):
        raise NotImplementedError

    @abstractmethod
    async def get_user_id_by_token(self, token):
        raise NotImplementedError
