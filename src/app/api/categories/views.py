from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

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
):
    return await crud.get_categories(session=session)


@router.post("/", response_model=Category)
async def create_category(
        category_in: CategoryCreate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_category(
        session=session, category_in=category_in
    )


@router.get("/{category_id}", response_model=Category)
async def get_category(
        category_id,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    category = await crud.get_category(
        session=session, category_id=category_id
    )
    if category:
        return category

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Category {category_id} not found",
    )


@router.put("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_category(
        category_id,
        category_update: CategoryUpdate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    category = await crud.get_category(
        session=session, category_id=category_id
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
        category_id,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    category = await crud.get_category(
        session=session, category_id=category_id
    )

    if category:
        return await crud.delete_category(
            session=session, category=category
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Category {category_id} not found",
    )
