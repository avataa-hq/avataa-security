from typing import Optional, Dict

from fastapi import HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi.requests import Request
import jwt
import aiohttp
from aiohttp import ClientConnectionError, ClientResponseError, InvalidURL
import asyncio

from auth.security_data_models import UserData
from settings import keycloak_settings


class Keycloak(OAuth2AuthorizationCodeBearer):
    def __init__(
        self,
        keycloak_public_url: str,
        authorization_url: str,
        token_url: str,
        refresh_url: Optional[str] = None,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        description: Optional[str] = None,
        auto_error: bool = True,
        options: Optional[dict] = None,
    ):
        super(Keycloak, self).__init__(
            authorizationUrl=authorization_url,
            tokenUrl=token_url,
            refreshUrl=refresh_url,
            scheme_name=scheme_name,
            scopes=scopes,
            description=description,
            auto_error=auto_error,
        )
        self.keycloak_public_url = keycloak_public_url
        self._public_key = None
        if not options:
            options = {
                "verify_signature": True,
                "verify_aud": False,
                "verify_exp": True,
            }
        self._options = options

    async def _get_public_key(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.keycloak_public_url,
                    timeout=aiohttp.ClientTimeout(total=5),
                ) as resp:
                    if resp.status != 200:
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

        public_key = (
            "-----BEGIN PUBLIC KEY-----\n"
            + data["public_key"]
            + "\n-----END PUBLIC KEY-----"
        )
        return public_key

    async def __call__(self, request: Request) -> UserData:
        user_info = await self._parse_jwt(request)
        return UserData.from_jwt(user_info)

    async def _parse_jwt(self, request: Request) -> dict:
        token = await super(Keycloak, self).__call__(request)

        if self._public_key is None:
            self._public_key = await self._get_public_key()

        user_info = await self._decode_token(token)
        return user_info

    async def _decode_token(self, token: str):
        try:
            decoded_token = jwt.decode(
                token,
                self._public_key,
                algorithms=["RS256"],
                options=self._options,
            )
        except jwt.PyJWTError as e:
            print(e)
            raise HTTPException(status_code=403, detail=str(e))
        return decoded_token


class KeycloakToken(OAuth2AuthorizationCodeBearer):
    def __init__(
        self,
        authorization_url: str,
        token_url: str,
        refresh_url: Optional[str] = None,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        description: Optional[str] = None,
        auto_error: bool = True,
    ):
        super(KeycloakToken, self).__init__(
            authorizationUrl=authorization_url,
            tokenUrl=token_url,
            refreshUrl=refresh_url,
            scheme_name=scheme_name,
            scopes=scopes,
            description=description,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> str:
        token = await super(KeycloakToken, self).__call__(request)
        return token


keycloak = Keycloak(
    keycloak_public_url=keycloak_settings.KEYCLOAK_PUBLIC_KEY_URL,
    token_url=keycloak_settings.KEYCLOAK_TOKEN_URL,
    authorization_url=keycloak_settings.KEYCLOAK_AUTHORIZATION_URL,
    refresh_url=keycloak_settings.KEYCLOAK_AUTHORIZATION_URL,
    scopes={
        "openid": "OpenID Connect scope",
        "profile": "Read claims that represent basic profile information",
    },
)


keycloak_token = KeycloakToken(
    token_url=keycloak_settings.KEYCLOAK_TOKEN_URL,
    authorization_url=keycloak_settings.KEYCLOAK_AUTHORIZATION_URL,
    refresh_url=keycloak_settings.KEYCLOAK_AUTHORIZATION_URL,
    scopes={
        "openid": "OpenID Connect scope",
        "profile": "Read claims that represent basic profile information",
    },
)
