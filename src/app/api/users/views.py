from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.users import crud
from app.api.users.crud import get_user_by_username
from app.api.users.redis_utils import (
    is_account_locked,
    increment_failed_attempts,
    lock_account,
)
from app.api.users.schemas import UserRegister, UserCreate, LoginRequest
from app.api.users.utils import hash_password, validate_password, encode_jwt
from src.app.database.db_helper import db_helper

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register/")
async def register_user(
    user_in: UserRegister,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> dict:
    """Registers new user."""

    existing_users = await get_user_by_username(session, user_in.username)
    if existing_users:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = hash_password(user_in.password)

    new_user = UserCreate(
        username=user_in.username, hashed_password=hashed_password
    )
    await crud.create_user(session, new_user)

    return {"message": "You successfully registered!"}


@router.post("/login/")
async def login_user(
    login_data: LoginRequest,
    response: Response,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    """Authenticates user credentials."""
    user = await crud.get_user_by_username(session, login_data.username)

    if await is_account_locked(login_data.username):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account temporarily locked due to "
                   "too many failed login attempts. Try again later.",
        )

    if not user or not validate_password(
        login_data.password, user.hashed_password
    ):
        attempts = await increment_failed_attempts(login_data.username)

        if attempts >= 5:
            await lock_account(login_data.username)

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    token = encode_jwt({"sub": user.username, "user_id": user.id})

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=86400,
        expires=86400,
        samesite="lax",
        secure=True,
    )

    return {"message": "Login successful"}


@router.post("/logout/")
async def logout(response: Response):
    """Terminates user session."""
    response.delete_cookie("access_token")
    return {"message": "Logged out"}
