from fastapi import APIRouter, Depends

from settings import level_settings
from auth.keycloak import keycloak
from auth.security_data_models import UserData
from auth.utils import check_admin, convert_kc_roles
from kc.roles import get_available_roles
from routers.resp_models.roles import Role

PREFIX = "/roles"


router = APIRouter(prefix=PREFIX)


@router.get("/level/low")
def get_level_low(user: UserData = Depends(keycloak)):
    is_admin = check_admin(user_data=user)
    kc_roles = get_available_roles(user_data=user, is_admin=is_admin)
    filtered_roles = [
        r
        for r in kc_roles
        if r.name.startswith(level_settings.LOW_LEVEL_KC_PREFIX)
    ]
    resp_roles = convert_kc_roles(
        filtered_roles,
        kc_prefix=level_settings.LOW_LEVEL_KC_PREFIX,
        microservices_prefix=level_settings.LOW_LEVEL_MS_PREFIX,
    )
    if is_admin:
        default_role = Role(
            name_for_user="default",
            name_for_microservices="default",
            name=None,
            client_role=False,
            composite=False,
            container_id=None,
            description=None,
            id=None,
        )
        resp_roles.append(default_role)
    return resp_roles
