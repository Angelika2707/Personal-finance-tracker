from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.users.schemas import UserCreate
from app.database.models import User


async def create_user(
    session: AsyncSession,
    user_in: UserCreate,
) -> User:
    user = User(**user_in.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_user_by_username(
    session: AsyncSession,
    username: str,
):
    stmt = select(User).where(User.username == username)
    result: Result = await session.execute(stmt)
    user = result.scalars().first()
    return user
