import datetime
import pytest
from httpx import Client, Response, RequestError
from src.app.frontend.api_helpers import (
    get_data,
    create_record,
    update_record,
    delete_record,
    get_categories,
    create_category,
    delete_category,
    logout_user,
)


@pytest.fixture
def mock_client(mocker):
    mock = mocker.MagicMock(spec=Client)
    mocker.patch("src.app.frontend.api_helpers.client", mock)
    return mock


@pytest.fixture(autouse=True)
def mock_streamlit(mocker):
    mocker.patch("streamlit.error")
    mocker.patch("streamlit.success")
    mocker.patch("streamlit.rerun")
    mocker.patch("streamlit.session_state", {})


@pytest.mark.parametrize(
    "status_code, response_json, expected",
    [
        (
            200,
            [
                {
                    "id": 1,
                    "type": "expense",
                    "description": "Record",
                    "amount": 100.0,
                    "date": "2025-01-01 15:00:00.000000",
                    "user_id": 1,
                    "category_id": 1,
                }
            ],
            [
                {
                    "id": 1,
                    "type": "expense",
                    "description": "Record",
                    "amount": 100.0,
                    "date": "2025-01-01 15:00:00.000000",
                    "user_id": 1,
                    "category_id": 1,
                }
            ],
        ),
        (500, None, []),
    ],
)
def test_get_data(mock_client, status_code, response_json, expected):
    mock_client.get.return_value = Response(status_code, json=response_json)
    result = get_data()
    assert result == expected


def test_get_data_request_error(mock_client):
    mock_client.get.side_effect = RequestError("Connection error")
    result = get_data()
    assert result == []


@pytest.mark.parametrize(
    "status_code, expected",
    [
        (200, True),
        (500, False),
    ],
)
def test_create_record(mock_client, status_code, expected):
    data = {
        "type": "income",
        "amount": 123.45,
        "description": "Test income",
        "date": "2025-01-01 15:00:00.000000",
        "category_id": 1,
    }
    mock_client.post.return_value = Response(status_code)
    assert create_record(data) is expected


def test_create_record_request_error(mock_client):
    mock_client.post.side_effect = RequestError("Connection error")
    data = {
        "type": "income",
        "amount": 123.45,
        "description": "Test income",
        "date": "2025-01-01 15:00:00.000000",
        "category_id": 1,
    }
    result = create_record(data)
    assert result is False


@pytest.mark.parametrize(
    "status_code, expected",
    [
        (204, True),
        (404, False),
    ],
)
def test_delete_record(mock_client, status_code, expected):
    mock_client.delete.return_value = Response(status_code)
    assert delete_record(100) == expected


def test_delete_record_request_error(mock_client):
    mock_client.delete.side_effect = RequestError("Connection error")
    result = delete_record(999)
    assert result is False


@pytest.mark.parametrize(
    "status_code, expected",
    [
        (204, True),
        (400, False),
    ],
)
def test_update_record(mock_client, status_code, expected):
    data = {
        "type": "expense",
        "amount": 50.0,
        "description": "Updated",
        "date": "2025-01-02 15:00:00.000000",
    }
    mock_client.put.return_value = Response(status_code)
    assert update_record(1, data) == expected


def test_update_record_request_error(mock_client):
    mock_client.put.side_effect = RequestError("Connection error")
    result = update_record(1, {"description": "update"})
    assert result is False


def test_logout_user_success(mock_client, mocker):
    mock_client.post.return_value = Response(200)
    mock_client.cookies = {}
    mocker.patch("streamlit.session_state", {"x": 1})
    logout_user()
    assert mock_client.post.called


def test_logout_user_failure(mock_client):
    mock_client.post.return_value = Response(401, json={"detail": "Fail"})
    logout_user()


def test_logout_user_request_error(mock_client):
    mock_client.post.side_effect = RequestError("Connection error")
    logout_user()
    assert mock_client.post.called


@pytest.mark.parametrize(
    "status_code, response_json, expected",
    [
        (200, [{"id": 1, "name": "Other"}], [{"id": 1, "name": "Other"}]),
        (500, None, []),
    ],
)
def test_get_categories(mock_client, status_code, response_json, expected):
    mock_client.get.return_value = Response(status_code, json=response_json)
    result = get_categories()
    assert result == expected


def test_get_categories_request_error(mock_client):
    mock_client.get.side_effect = RequestError("Connection error")
    result = get_categories()
    assert result == []


def test_create_category_success(mock_client, mocker):
    mocker.patch("src.app.frontend.api_helpers.get_categories", return_value=[])
    mock_client.post.return_value = Response(200, json={"name": "Travel", "user_id": 1})
    result = create_category({"name": "travel"})
    assert result == {"name": "Travel", "user_id": 1}


@pytest.mark.parametrize(
    "existing, input_data, expected",
    [
        ([{"name": "Food"}], {"name": "food"}, None),
        ([{"name": "Food"}], {"name": "Food"}, None),
        ([], {"name": "   "}, None),
    ],
)
def test_create_category_invalid_cases(mocker, existing, input_data, expected):
    mocker.patch("src.app.frontend.api_helpers.get_categories", return_value=existing)
    result = create_category(input_data)
    assert result is expected


def test_create_category_request_error(mock_client, mocker):
    mocker.patch("src.app.frontend.api_helpers.get_categories", return_value=[])
    mock_client.post.side_effect = RequestError("Connection error")
    result = create_category({"name": "Test"})
    assert result is None


@pytest.mark.parametrize(
    "status_code, expected",
    [
        (204, True),
        (404, False),
    ],
)
def test_delete_category(mock_client, status_code, expected):
    mock_client.delete.return_value = Response(status_code)
    assert delete_category(123) is expected


def test_delete_category_request_error(mock_client):
    mock_client.delete.side_effect = RequestError("Connection error")
    result = delete_category(999)
    assert result is False
