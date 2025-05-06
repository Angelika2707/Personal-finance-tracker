from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.app.database.db_helper import db_helper
from . import crud
from .schemas import (
    FinancialRecord,
    FinancialRecordCreate,
    FinancialRecordUpdate,
    FinancialRecordUpdatePartial,
)
from .utils import get_current_user

router = APIRouter(prefix="/financial_records", tags=["Financial Records"])


@router.get("/", response_model=list[FinancialRecord])
async def get_financial_records(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user_id: int = Depends(get_current_user),
):
    return await crud.get_financial_records(
        session=session,
        user_id=current_user_id,
    )


@router.post("/", response_model=FinancialRecord)
async def create_financial_record(
    financial_record_in: FinancialRecordCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user_id: int = Depends(get_current_user),
):
    return await crud.create_financial_record(
        session=session,
        financial_record_in=financial_record_in,
        user_id=current_user_id,
    )


@router.get("/{financial_record_id}", response_model=FinancialRecord)
async def get_financial_record(
    financial_record_id,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user_id: int = Depends(get_current_user),
):
    financial_record = await crud.get_financial_record(
        session=session,
        financial_record_id=financial_record_id,
        user_id=current_user_id,
    )
    if financial_record:
        return financial_record

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Financial record {financial_record_id} not found",
    )


@router.put("/{financial_record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_financial_record(
    financial_record_id,
    financial_record_update: FinancialRecordUpdate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user_id: int = Depends(get_current_user),
):
    financial_record = await crud.get_financial_record(
        session=session,
        financial_record_id=financial_record_id,
        user_id=current_user_id,
    )

    if financial_record:
        return await crud.update_financial_record(
            session=session,
            financial_record=financial_record,
            financial_record_update=financial_record_update,
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Financial record {financial_record_id} not found",
    )


@router.patch("/{financial_record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_financial_record_partial(
    financial_record_id,
    financial_record_update: FinancialRecordUpdatePartial,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user_id: int = Depends(get_current_user),
):
    financial_record = await crud.get_financial_record(
        session=session,
        financial_record_id=financial_record_id,
        user_id=current_user_id,
    )

    if financial_record:
        return await crud.update_financial_record_partial(
            session=session,
            financial_record=financial_record,
            financial_record_update=financial_record_update,
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Financial record {financial_record_id} not found",
    )


@router.delete("/{financial_record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_financial_record(
    financial_record_id,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    current_user_id: int = Depends(get_current_user),
):
    financial_record = await crud.get_financial_record(
        session=session,
        financial_record_id=financial_record_id,
        user_id=current_user_id,
    )

    if financial_record:
        return await crud.delete_financial_record(
            session=session, financial_record=financial_record
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Financial record {financial_record_id} not found",
    )
