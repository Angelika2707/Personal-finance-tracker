from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict


class TypeFinanceRecord(str, Enum):
    """Possible types of financial records."""

    income = "income"
    expense = "expense"


class FinancialRecordBase(BaseModel):
    """Base schema for financial record."""

    type: TypeFinanceRecord
    description: str
    amount: float
    date: datetime
    category_id: int


class FinancialRecordCreate(FinancialRecordBase):
    """Schema for creating new financial records."""

    pass


class FinancialRecord(FinancialRecordBase):
    """Complete financial record representation returned in API responses."""

    model_config = ConfigDict(from_attributes=True)

    id: int


class FinancialRecordUpdate(FinancialRecordCreate):
    """Schema for full update of a financial record."""

    pass


class FinancialRecordUpdatePartial(FinancialRecordCreate):
    """Schema for partial updates of financial record fields."""

    type: TypeFinanceRecord | None = None
    description: str | None = None
    amount: float | None = None
    date: datetime | None = None
    category_id: int | None = None
