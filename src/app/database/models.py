import datetime
from enum import Enum as PyEnum

from sqlalchemy import Enum, Float, DateTime, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr, relationship


class TypeFinanceRecord(PyEnum):
    expense = "expense"
    income = "income"


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id: Mapped[int] = mapped_column(primary_key=True)


class Category(Base):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(30), unique=True)

    financial_records: Mapped[list["FinancialRecord"]] = relationship(back_populates="category")


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
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))

    category: Mapped["Category"] = relationship(back_populates="financial_records")
