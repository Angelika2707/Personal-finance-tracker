import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.categories.schemas import CategoryCreate, CategoryUpdate
from app.database.models import Category
from app.api.categories.crud import (
    get_categories,
    get_category,
    create_category,
    update_category,
    delete_category,
)


@pytest.fixture
def session():
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def fake_category():
    return Category(id=7, name="Test", user_id=123)


@pytest.mark.parametrize("user_id, expected_count", [
    (123, 1),
    (456, 2),
    (789, 0),
])
@pytest.mark.asyncio
async def test_get_categories(session, fake_category, user_id, expected_count):
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [fake_category] * expected_count

    session.execute.return_value = mock_result

    result = await get_categories(session, user_id=user_id)

    assert len(result) == expected_count
    session.execute.assert_called_once()


@pytest.mark.asyncio
@pytest.mark.parametrize("user_id", [123, 456, 789])
async def test_get_categories_with_multiple_users(session, user_id):
    fake_data = {
        123: [Category(id=1, name="Food", user_id=123)],
        456: [
            Category(id=2, name="Books", user_id=456),
            Category(id=3, name="Transport", user_id=456)
        ],
        789: []
    }

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = fake_data[user_id]
    session.execute.return_value = mock_result

    result = await get_categories(session, user_id=user_id)

    assert result == fake_data[user_id]
    assert all(cat.user_id == user_id for cat in result)
    session.execute.assert_awaited_once()


@pytest.mark.parametrize("category_id, user_id, expected_result", [
    (1, 123, "found"),
    (999, 123, None),
])
@pytest.mark.asyncio
async def test_get_category(session, fake_category, category_id, user_id, expected_result):
    mock_result = MagicMock()

    if expected_result == "found":
        fake_category.id = category_id
        fake_category.user_id = user_id
        mock_result.scalars.return_value.first.return_value = fake_category
    else:
        mock_result.scalars.return_value.first.return_value = None

    session.execute.return_value = mock_result

    result = await get_category(session, category_id=category_id, user_id=user_id)

    if expected_result == "found":
        assert result == fake_category
    else:
        assert result is None
    session.execute.assert_called_once()


@pytest.mark.parametrize("update_data, expected_name", [
    ({"name": "New Name"}, "New Name"),
    ({"name": ""}, ""),
])
@pytest.mark.asyncio
async def test_update_category(session, fake_category, update_data, expected_name):
    session.commit = AsyncMock()
    category_update = CategoryUpdate(**update_data)

    updated = await update_category(session, fake_category, category_update)

    assert updated.name == expected_name
    session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_create_category(session):
    category_data = {"name": "Books"}
    session.refresh = AsyncMock()
    category_in = CategoryCreate(**category_data)

    result = await create_category(session, category_in, user_id=123)

    assert isinstance(result, Category)
    assert result.name == category_data["name"]
    assert result.user_id == 123
    session.add.assert_called_once()
    session.commit.assert_called_once()
    session.refresh.assert_called_once()


@pytest.mark.asyncio
async def test_delete_category(session, fake_category):
    await delete_category(session, fake_category)

    session.delete.assert_awaited_once_with(fake_category)
    session.commit.assert_awaited_once()
