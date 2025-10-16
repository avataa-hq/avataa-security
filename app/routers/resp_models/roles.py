from pydantic import Field

from kc.models import Role as KC_Role


class Role(KC_Role):
    name_for_user: str = Field(..., alias="nameForUser", min_length=1)
    name_for_microservices: str = Field(
        ..., alias="nameForMicroservices", min_length=1
    )
    name: str | None = Field(None, alias="nameForKeycloak", min_length=1)
    container_id: str | None = Field(None, alias="containerId")
    description: str | None = Field(None, alias="description")
    id: str | None = Field(None, alias="id")

    class Config:
        allow_population_by_field_name = True
