import datetime
from enum import Enum as PyEnum

from sqlalchemy import Enum, Float, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr


class TypeFinanceRecord(PyEnum):
    expense = "expense"
    income = "income"


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id: Mapped[int] = mapped_column(primary_key=True)


class FinancialRecord(Base):
    type: Mapped[TypeFinanceRecord] = mapped_column(
        Enum(
            TypeFinanceRecord,
            name="typefinancerecord",
        ),
        nullable=False,
    )
    description: Mapped[str] = mapped_column()
    amount: Mapped[float] = mapped_column(Float)
    date: Mapped[datetime.datetime] = mapped_column(DateTime)
