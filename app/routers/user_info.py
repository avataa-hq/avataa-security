from typing import Annotated

from fastapi import APIRouter, Depends

from auth.keycloak import keycloak_token
from service.instances import get_service_instances, ServiceInstances
from tasks.userinfo.task import UserInfo

PREFIX = "/cached"


router = APIRouter(prefix=PREFIX)


@router.get("/realms/{realm}/protocol/openid-connect/userinfo")
async def get_userinfo(
    realm: str,
    token: Annotated[str, Depends(keycloak_token)],
    instances: Annotated[ServiceInstances, Depends(get_service_instances)],
):
    task = UserInfo(cache=instances.cache, auth=instances.auth)
    result = await task.execute(token=token)
    return result


@router.post("/realms/{realm}/protocol/openid-connect/userinfo")
async def post_userinfo(
    realm: str,
    token: Annotated[str, Depends(keycloak_token)],
    instances: Annotated[ServiceInstances, Depends(get_service_instances)],
):
    task = UserInfo(cache=instances.cache, auth=instances.auth)
    result = await task.execute(token=token)
    return result
