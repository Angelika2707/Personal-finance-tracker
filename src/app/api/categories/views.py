from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from src.app.api.financial_records.utils import get_current_user

from . import crud
from .schemas import (
    Category,
    CategoryCreate,
    CategoryUpdate,
)
from src.app.database.db_helper import db_helper

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=list[Category])
async def get_categories(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user_id: int = Depends(get_current_user),
):
    """Retrieves all categories belonging to the user."""
    return await crud.get_categories(session=session, user_id=current_user_id)


@router.post("/", response_model=Category)
async def create_category(
    category_in: CategoryCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user_id: int = Depends(get_current_user),
):
    """Creates a new category for the user."""
    return await crud.create_category(
        session=session, category_in=category_in, user_id=current_user_id
    )


@router.get("/{category_id}", response_model=Category)
async def get_category(
    category_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user_id: int = Depends(get_current_user),
):
    """Returns category if it belongs to the user."""
    category = await crud.get_category(
        session=session, category_id=category_id, user_id=current_user_id
    )
    if category:
        return category

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Category {category_id} not found",
    )


@router.put("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_category(
    category_id: int,
    category_update: CategoryUpdate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user_id: int = Depends(get_current_user),
):
    """Updates an existing category that belongs to the user."""
    category = await crud.get_category(
        session=session, category_id=category_id, user_id=current_user_id
    )

    if category:
        return await crud.update_category(
            session=session,
            category=category,
            category_update=category_update,
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Category {category_id} not found",
    )


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user_id: int = Depends(get_current_user),
):
    """Deletes category that belongs to the user."""
    category = await crud.get_category(
        session=session,
        category_id=category_id,
        user_id=current_user_id,
    )

    if category:
        return await crud.delete_category(session=session, category=category)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Category {category_id} not found",
    )
