import asyncio

import aiohttp
from aiohttp import ClientConnectionError, ClientResponseError, InvalidURL
from fastapi import HTTPException
import jwt

from service.auth_service.auth_interface import AuthInterface


class KeycloakAuth(AuthInterface):
    def __init__(
        self,
        server_url: str,
        realm_name: str,
        client_id: str,
        client_secret_key: str,
    ):
        self.server_url = server_url
        self.realm_name = realm_name
        self.client_id = client_id
        self.client_secret_key = client_secret_key

        self._kc_url = f"{server_url}/realms/{realm_name}"
        self._user_info_url = f"{self._kc_url}/protocol/openid-connect/userinfo"
        self._options = {"verify_signature": False}

    async def _decode_token(self, token: str):
        try:
            decoded_token = jwt.decode(token, options=self._options)
        except jwt.PyJWTError as e:
            print(e)
            raise HTTPException(status_code=403, detail=str(e))
        return decoded_token

    async def get_user_info(self, token):
        if not token:
            raise HTTPException(status_code=401, detail="Token is empty")
        header = {"Authorization": f"Bearer {token}"}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self._user_info_url,
                    headers=header,
                    timeout=aiohttp.ClientTimeout(total=5),
                ) as resp:
                    if resp.status != 200:
                        print(resp.status, resp.headers)
                        print("Connection url:", self._user_info_url)
                        raise HTTPException(
                            status_code=503,
                            detail="Token verification service unavailable",
                        )
                    data = await resp.json()
        except ClientConnectionError:
            raise HTTPException(
                status_code=503, detail="Token verification service unavailable"
            )
        except asyncio.TimeoutError:
            raise HTTPException(
                status_code=503, detail="Token verification service unavailable"
            )
        except ClientResponseError:
            raise HTTPException(
                status_code=503, detail="Token verification service unavailable"
            )
        except InvalidURL:
            raise HTTPException(
                status_code=503, detail="Token verification service unavailable"
            )
        else:
            return data

    async def get_user_id_by_token(self, token):
        try:
            decoded_token = jwt.decode(token, options=self._options)
        except jwt.PyJWTError as e:
            print(e)
            raise HTTPException(status_code=403, detail=str(e))
        else:
            return decoded_token["sub"]

    async def get_token_expiration_time(self, token):
        try:
            decoded_token = jwt.decode(token, options=self._options)
        except jwt.PyJWTError as e:
            print(e)
            raise HTTPException(status_code=403, detail=str(e))
        else:
            return decoded_token["exp"]
