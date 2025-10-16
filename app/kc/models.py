from pydantic import BaseModel, Field


class Role(BaseModel):
    client_role: bool = Field(..., alias="clientRole")
    composite: bool = Field(..., alias="composite")
    container_id: str = Field(..., alias="containerId")
    description: str | None = Field(None, alias="description")
    id: str = Field(..., alias="id")
    name: str = Field(..., alias="name")
