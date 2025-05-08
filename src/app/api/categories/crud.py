from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.categories.schemas import CategoryCreate, CategoryUpdate
from app.database.models import Category


async def get_categories(
    session: AsyncSession,
    user_id: int,
) -> list[Category]:
    """Retrieves all categories belonging to a user, sorted by their ID."""
    stmt = (
        select(Category)
        .where(Category.user_id == user_id)
        .order_by(Category.id)
    )
    result: Result = await session.execute(stmt)
    categories = result.scalars().all()
    return list(categories)


async def get_category(
    session: AsyncSession,
    category_id: int,
    user_id: int,
) -> Category | None:
    """Fetches a specific category by ID if it belongs to the user."""
    stmt = select(Category).where(
        Category.id == category_id,
        Category.user_id == user_id,
    )
    result = await session.execute(stmt)
    return result.scalars().first()


async def create_category(
    session: AsyncSession,
    category_in: CategoryCreate,
    user_id: int,
) -> Category:
    """Creates a new category associated with the user."""
    category = Category(**category_in.model_dump())
    category.user_id = user_id
    session.add(category)
    await session.commit()
    await session.refresh(category)
    return category


async def update_category(
    session: AsyncSession,
    category: Category,
    category_update: CategoryUpdate,
) -> Category:
    """Updates the fields of an existing category."""
    for name, value in category_update.model_dump().items():
        setattr(category, name, value)
    await session.commit()
    return category


async def delete_category(
    session: AsyncSession,
    category: Category,
) -> None:
    """Deletes the specified category."""
    await session.delete(category)
    await session.commit()
