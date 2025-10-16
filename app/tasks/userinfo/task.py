import json
import time

from tasks.userinfo.protocols import CacheProtocol, AuthProtocol


class UserInfo:
    def __init__(self, cache: CacheProtocol, auth: AuthProtocol):
        self.cache = cache
        self.auth = auth

    async def execute(self, token: str) -> dict | None:
        user_id = await self.auth.get_user_id_by_token(token=token)
        cached_user_info = await self.cache.get(user_id)
        if not cached_user_info:
            user_info = await self.auth.get_user_info(token=token)
            if user_info:
                exp_time = await self.auth.get_token_expiration_time(
                    token=token
                )
                left_time = round(exp_time - time.time())
                if left_time > 0:
                    await self.cache.set(
                        user_id, json.dumps(user_info), ttl=left_time
                    )
                cached_user_info = user_info
        else:
            cached_user_info = json.loads(cached_user_info)
        return cached_user_info
