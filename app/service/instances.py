from settings import keycloak_settings
from service.auth_service.auth_interface import AuthInterface
from service.auth_service.keycloak_auth import KeycloakAuth
from service.cache_service.cache_interface import CacheServiceInterface
from service.cache_service.redis_cache import RedisCache
from settings import redis_settings


class ServiceInstances:
    def __init__(self):
        self._cache: CacheServiceInterface | None = None
        self._auth: AuthInterface | None = None

    @staticmethod
    def __init_cache() -> CacheServiceInterface:
        return RedisCache(
            host=redis_settings.REDIS_HOST,
            port=redis_settings.REDIS_PORT,
            db=redis_settings.REDIS_DB,
            password=redis_settings.REDIS_PASSWORD,
            username=redis_settings.REDIS_USERNAME,
        )

    @property
    def cache(self) -> CacheServiceInterface:
        if not self._cache:
            self._cache = self.__init_cache()
        return self._cache

    @staticmethod
    def __init_auth() -> AuthInterface:
        return KeycloakAuth(
            server_url=keycloak_settings.KEYCLOAK_URL,
            realm_name=keycloak_settings.KEYCLOAK_REALM,
            client_id=keycloak_settings.KEYCLOAK_CLIENT_ID,
            client_secret_key=keycloak_settings.KEYCLOAK_CLIENT_SECRET,
        )

    @property
    def auth(self) -> AuthInterface:
        if not self._auth:
            self._auth = self.__init_auth()
        return self._auth


_instances: ServiceInstances | None = None


def get_service_instances():
    global _instances
    if not _instances:
        _instances = ServiceInstances()
    return _instances
