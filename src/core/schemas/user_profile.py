from pydantic import BaseModel
from pydantic import ConfigDict


class UserProfileBase(BaseModel):
    user_id: str  # ID пользователя из Keycloak
    full_name: str | None = None
    address: str | None = None


class UserProfileCreate(UserProfileBase):
    pass


class UserProfileRead(UserProfileBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
