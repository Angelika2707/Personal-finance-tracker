import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

from app.database.models import FinancialRecord
from app.api.financial_records.schemas import (
    FinancialRecordCreate,
    FinancialRecordUpdate,
    FinancialRecordUpdatePartial,
)
from app.api.financial_records.crud import (
    get_financial_records,
    get_financial_record,
    create_financial_record,
    update_financial_record,
    update_financial_record_partial,
    delete_financial_record,
)


@pytest.fixture
def session():
    return AsyncMock()


@pytest.fixture
def fake_financial_record():
    return FinancialRecord(
        id=1,
        type="income",
        description="Test record",
        amount=100.0,
        date=datetime(2025, 1, 1),
        user_id=123,
        category_id=5,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_id, expected_count",
    [
        (123, 2),
        (456, 1),
        (999, 0),
    ],
)
async def test_get_financial_records(
    session, user_id, expected_count, fake_financial_record
):
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [
        fake_financial_record
    ] * expected_count
    session.execute.return_value = mock_result

    result = await get_financial_records(session, user_id=user_id)

    assert isinstance(result, list)
    assert len(result) == expected_count
    session.execute.assert_awaited_once()


@pytest.mark.asyncio
@pytest.mark.parametrize("user_id", [123, 456, 789])
async def test_get_financial_records_multiple_users(session, user_id):
    fake_data = {
        123: [
            FinancialRecord(
                id=1,
                type="income",
                description="Salary",
                amount=1000.0,
                date=datetime(2025, 1, 1),
                user_id=123,
                category_id=1,
            ),
            FinancialRecord(
                id=2,
                type="expense",
                description="Groceries",
                amount=150.0,
                date=datetime(2025, 1, 2),
                user_id=123,
                category_id=2,
            ),
        ],
        456: [
            FinancialRecord(
                id=3,
                type="income",
                description="Bonus",
                amount=500.0,
                date=datetime(2025, 1, 3),
                user_id=456,
                category_id=3,
            ),
        ],
        789: [],
    }
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = fake_data[user_id]
    session.execute.return_value = mock_result

    result = await get_financial_records(session, user_id=user_id)

    assert isinstance(result, list)
    assert result == fake_data[user_id]
    session.execute.assert_awaited_once()


@pytest.mark.asyncio
@pytest.mark.parametrize("record_exists", [True, False])
async def test_get_financial_record(session, fake_financial_record, record_exists):
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = (
        fake_financial_record if record_exists else None
    )
    session.execute.return_value = mock_result

    record_id = 1
    user_id = 123

    result = await get_financial_record(
        session, financial_record_id=record_id, user_id=user_id
    )

    if record_exists:
        assert result == fake_financial_record
    else:
        assert result is None
    session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_financial_record(session):
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.add = MagicMock()

    data = {
        "type": "expense",
        "description": "description",
        "amount": 200.0,
        "date": datetime(2025, 5, 5),
        "category_id": 1,
    }

    financial_record_in = FinancialRecordCreate(**data)

    result = await create_financial_record(session, financial_record_in, user_id=42)

    assert isinstance(result, FinancialRecord)
    assert result.user_id == 42
    assert result.amount == data["amount"]
    session.add.assert_called_once()
    session.commit.assert_awaited_once()
    session.refresh.assert_awaited_once()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "update_data",
    [
        {},
        {"amount": 500.0},
        {"description": "Changed", "amount": 123.45},
    ],
)
async def test_update_financial_record(session, fake_financial_record, update_data):
    session.commit = AsyncMock()

    default_data = {
        "type": fake_financial_record.type,
        "description": fake_financial_record.description,
        "amount": fake_financial_record.amount,
        "date": fake_financial_record.date,
        "user_id": fake_financial_record.user_id,
        "category_id": fake_financial_record.category_id,
    }
    default_data.update(update_data)

    update = FinancialRecordUpdate(**default_data)
    updated = await update_financial_record(session, fake_financial_record, update)

    for key, value in update_data.items():
        assert getattr(updated, key) == value
    session.commit.assert_awaited_once()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "partial_data",
    [
        {},
        {"description": "Only desc"},
        {"description": "Desc", "type": "expense"},
    ],
)
async def test_update_financial_record_partial(
    session, fake_financial_record, partial_data
):
    session.commit = AsyncMock()

    update = FinancialRecordUpdatePartial(**partial_data)
    updated = await update_financial_record_partial(
        session, fake_financial_record, update
    )

    for key, value in partial_data.items():
        assert getattr(updated, key) == value
    session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_financial_record(session, fake_financial_record):
    session.delete = AsyncMock()
    session.commit = AsyncMock()

    await delete_financial_record(session, fake_financial_record)

    session.delete.assert_awaited_once_with(fake_financial_record)
    session.commit.assert_awaited_once()
