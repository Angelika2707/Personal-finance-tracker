from typing import Annotated

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    """Base schema for a user."""

    username: Annotated[str, MinLen(3), MaxLen(20)]
    password: Annotated[str, MinLen(5), MaxLen(20)]


class UserCreate(BaseModel):
    """Schema for creating new users."""

    username: Annotated[str, MinLen(3), MaxLen(20)]
    hashed_password: bytes


class UserRegister(UserBase):
    """Schema for user registration requests."""

    pass


class User(UserBase):
    """Complete user representation."""

    model_config = ConfigDict(from_attributes=True)

    id: int


class LoginRequest(UserBase):
    """Schema for login credentials."""

    pass
