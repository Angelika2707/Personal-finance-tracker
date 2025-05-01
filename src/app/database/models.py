import datetime
from enum import Enum as PyEnum

from sqlalchemy import Enum, Float, DateTime, ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    declared_attr,
    relationship,
)


class TypeFinanceRecord(PyEnum):
    expense = "expense"
    income = "income"


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id: Mapped[int] = mapped_column(primary_key=True)


class User(Base):
    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[bytes] = mapped_column()

    records: Mapped[list["FinancialRecord"]] = relationship(back_populates="user")


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
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="records")
