from settings import level_settings
from auth.security_data_models import UserData
from kc.models import Role as KC_Role

from routers.resp_models.roles import Role


db_admins = {"realm_access.__admin"}


def check_admin(user_data: UserData):
    user_roles = get_user_permissions(user_data)
    is_admin = len(db_admins.intersection(user_roles)) > 0
    return is_admin


def get_user_permissions(jwt: UserData) -> list[str]:
    permissions = []
    if jwt.realm_access:
        permissions.extend(
            [
                f"{jwt.realm_access.name}.{r}"
                for r in jwt.realm_access.roles
                if r.startswith(level_settings.LOW_LEVEL_KC_PREFIX)
            ]
        )
    if jwt.resource_access:
        for resource_access in jwt.resource_access:
            permissions.extend(
                [
                    f"{resource_access.name}.{r}"
                    for r in resource_access.roles
                    if r.startswith(level_settings.LOW_LEVEL_KC_PREFIX)
                ]
            )
    return permissions


def convert_kc_roles(
    roles: list[KC_Role], kc_prefix: str, microservices_prefix: str
):
    results = []
    for role in roles:
        role = role.dict()
        role["name_for_user"] = role["name"].replace(kc_prefix, "", 1)
        role["name_for_microservices"] = microservices_prefix + role["name"]
        role = Role(**role)
        results.append(role)
    return results
