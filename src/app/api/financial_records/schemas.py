from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict


class TypeFinanceRecord(str, Enum):
    income = "income"
    expense = "expense"


class FinancialRecordBase(BaseModel):
    type: TypeFinanceRecord
    description: str
    amount: float
    date: datetime
    category_id: int


class FinancialRecordCreate(FinancialRecordBase):
    pass


class FinancialRecord(FinancialRecordBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class FinancialRecordUpdate(FinancialRecordCreate):
    pass


class FinancialRecordUpdatePartial(FinancialRecordCreate):
    type: TypeFinanceRecord | None = None
    description: str | None = None
    amount: float | None = None
    date: datetime | None = None
    category_id: int | None = None
