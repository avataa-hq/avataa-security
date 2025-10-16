from keycloak import KeycloakAdmin, KeycloakOpenIDConnection
from settings import keycloak_settings

keycloak_connection = KeycloakOpenIDConnection(
    server_url=keycloak_settings.KEYCLOAK_URL,
    realm_name=keycloak_settings.KEYCLOAK_REALM,
    client_id=keycloak_settings.KEYCLOAK_CLIENT_ID,
    client_secret_key=keycloak_settings.KEYCLOAK_CLIENT_SECRET,
    verify=True,
)

keycloak_admin = KeycloakAdmin(connection=keycloak_connection)
