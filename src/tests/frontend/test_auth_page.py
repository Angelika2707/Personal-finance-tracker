import pytest
import streamlit as st
from httpx import Client, Response, RequestError

from src.app.frontend.auth_page import register_user, login_user, render_auth_page


@pytest.fixture
def mock_client(mocker):
    mock = mocker.MagicMock(spec=Client)
    mocker.patch("src.app.frontend.auth_page.client", mock)
    return mock


@pytest.fixture(autouse=True)
def mock_streamlit(mocker):
    mocker.patch("streamlit.error")
    mocker.patch("streamlit.success")
    mocker.patch("streamlit.rerun")
    mocker.patch("streamlit.title")
    mocker.patch("streamlit.tabs", return_value=([], []))
    mocker.patch("streamlit.text_input", side_effect=["", "", "", ""])
    st.session_state.clear()


@pytest.mark.parametrize(
    "reg_status, login_return, expected",
    [
        (200, (True, "Logged in"), (True, "Logged in")),
        (422, None, (False, "Password must have at least 5 characters")),
        (500, None, (False, "Failed to register")),
    ],
)
def test_register_user(mocker, mock_client, reg_status, login_return, expected):
    mock_client.post.return_value = Response(reg_status)
    if reg_status == 200:
        mocker.patch("src.app.frontend.auth_page.login_user", return_value=login_return)
    result = register_user("user", "password")
    assert result == expected


def test_register_user_request_error(mock_client):
    mock_client.post.side_effect = RequestError("Cannot connect")
    success, msg = register_user("u", "p")
    assert not success
    assert "Error connecting to server" in msg


@pytest.mark.parametrize(
    "status_code, cookie_val, expected_result, expected_state",
    [
        (
            200,
            "token123",
            (True, "You successfully registered!"),
            {"logged_in": True, "username": "username", "access_token": "token123"},
        ),
        (401, None, (False, "Failed to login"), {}),
    ],
)
def test_login_user_status(
    mock_client, status_code, cookie_val, expected_result, expected_state
):
    mock_client.post.return_value = Response(
        status_code, json={"message": "You successfully registered!"}
    )
    mock_client.cookies.get.return_value = cookie_val
    result = login_user("username", "password")
    assert result == expected_result
    for key, val in expected_state.items():
        assert st.session_state.get(key) == val
    if status_code != 200:
        assert "logged_in" not in st.session_state


def test_login_user_request_error(mock_client):
    mock_client.post.side_effect = RequestError("Down")
    success, msg = login_user("username", "password")
    assert not success
    assert "Error connecting to server" in msg
