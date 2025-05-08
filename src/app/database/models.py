import datetime
from enum import Enum as PyEnum

from sqlalchemy import Enum, Float, DateTime, ForeignKey, String
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    declared_attr,
    relationship,
)


class TypeFinanceRecord(PyEnum):
    """Enumeration of financial record types."""

    expense = "expense"
    income = "income"


class Base(DeclarativeBase):
    """Abstract base class for all ORM models."""

    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id: Mapped[int] = mapped_column(primary_key=True)


class Category(Base):
    """A financial category for grouping records."""

    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(30))

    financial_records: Mapped[list["FinancialRecord"]] = relationship(
        back_populates="category"
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )
    user: Mapped["User"] = relationship(back_populates="categories")


class User(Base):
    """A user of the finance tracking system."""

    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[bytes] = mapped_column()

    records: Mapped[list["FinancialRecord"]] = relationship(
        back_populates="user"
    )
    categories: Mapped[list["Category"]] = relationship(back_populates="user")


class FinancialRecord(Base):
    """A single financial transaction record."""

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
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )
    user: Mapped["User"] = relationship(back_populates="records")
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category: Mapped["Category"] = relationship(
        back_populates="financial_records"
    )
