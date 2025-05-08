from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.users.schemas import UserCreate
from app.database.models import User, Category


async def create_user(
    session: AsyncSession,
    user_in: UserCreate,
) -> User:
    """Creates new user."""
    user = User(**user_in.model_dump())
    session.add(user)
    await session.flush()

    default_categories = [
        {"name": "Other"},
        {"name": "Food"},
        {"name": "Transport"},
        {"name": "Housing"},
        {"name": "Entertainment"},
        {"name": "Health"},
    ]

    for category_data in default_categories:
        category = Category(name=category_data["name"], user_id=user.id)
        session.add(category)

    await session.commit()
    await session.refresh(user)
    return user


async def get_user_by_username(
    session: AsyncSession,
    username: str,
):
    """Retrieves user by username."""
    stmt = select(User).where(User.username == username)
    result: Result = await session.execute(stmt)
    user = result.scalars().first()
    return user
