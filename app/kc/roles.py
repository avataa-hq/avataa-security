from auth.security_data_models import UserData
from kc.kc_connection import keycloak_admin
from pydantic import parse_obj_as

from kc.models import Role


def get_available_roles(user_data: UserData, is_admin: bool = False):
    if is_admin:
        roles = keycloak_admin.get_realm_roles()
    else:
        roles = keycloak_admin.get_realm_roles_of_user(user_data.id)
    return parse_obj_as(list[Role], roles)
