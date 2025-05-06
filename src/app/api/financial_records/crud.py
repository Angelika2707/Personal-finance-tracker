from datetime import datetime

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.financial_records.schemas import (
    FinancialRecordCreate,
    FinancialRecordUpdate,
    FinancialRecordUpdatePartial,
)
from app.database.models import FinancialRecord


async def get_financial_records(
    session: AsyncSession,
    user_id: int,
) -> list[FinancialRecord]:
    stmt = (
        select(FinancialRecord)
        .where(FinancialRecord.user_id == user_id)
        .order_by(FinancialRecord.id)
    )
    result: Result = await session.execute(stmt)
    financial_records = result.scalars().all()
    return list(financial_records)


async def get_financial_record(
    session: AsyncSession,
    financial_record_id: int,
    user_id: int,
) -> FinancialRecord | None:
    stmt = select(FinancialRecord).where(
        FinancialRecord.id == financial_record_id,
        FinancialRecord.user_id == user_id,
    )
    result = await session.execute(stmt)
    return result.scalars().first()


async def create_financial_record(
    session: AsyncSession,
    financial_record_in: FinancialRecordCreate,
    user_id: int,
) -> FinancialRecord:
    financial_record = FinancialRecord(**financial_record_in.model_dump())
    financial_record.user_id = user_id
    session.add(financial_record)
    await session.commit()
    await session.refresh(financial_record)
    return financial_record


async def update_financial_record(
    session: AsyncSession,
    financial_record: FinancialRecord,
    financial_record_update: FinancialRecordUpdate,
) -> FinancialRecord:
    for name, value in financial_record_update.model_dump().items():
        if isinstance(value, datetime):
            value = value.replace(tzinfo=None)
        setattr(financial_record, name, value)
    await session.commit()
    return financial_record


async def update_financial_record_partial(
    session: AsyncSession,
    financial_record: FinancialRecord,
    financial_record_update: FinancialRecordUpdatePartial,
) -> FinancialRecord:
    for name, value in financial_record_update.model_dump(exclude_unset=True).items():
        setattr(financial_record, name, value)
    await session.commit()
    return financial_record


async def delete_financial_record(
    session: AsyncSession,
    financial_record: FinancialRecord,
) -> None:
    await session.delete(financial_record)
    await session.commit()
