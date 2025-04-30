from typing import Annotated

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: Annotated[str, MinLen(3), MaxLen(20)]
    password: Annotated[str, MinLen(5), MaxLen(20)]


class UserCreate(BaseModel):
    username: Annotated[str, MinLen(3), MaxLen(20)]
    hashed_password: bytes


class UserRegister(UserBase):
    pass


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class LoginRequest(UserBase):
    pass
