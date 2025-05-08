import streamlit as st
import httpx
from app.frontend.api_helpers import client
from app.config import settings


def register_user(username, password):
    """Registers a new user and log them in upon success."""
    try:
        response = client.post(
            settings.api_endpoints.register_url,
            json={"username": username, "password": password},
        )
        if response.status_code == 200:
            return login_user(username, password)
        elif response.status_code == 422:
            return False, "Password must have at least 5 characters"
        else:
            return False, "Failed to register"
    except httpx.RequestError as e:
        return False, f"Error connecting to server: {str(e)}"


def login_user(username, password):
    """Authenticates a user."""
    try:
        response = client.post(
            settings.api_endpoints.login_url,
            json={"username": username, "password": password},
        )
        if response.status_code == 200:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.session_state["access_token"] = client.cookies.get(
                "access_token"
            )
            return True, response.json().get("message")
        else:
            error_detail = response.json().get("detail", "Failed to login")
            return False, error_detail
    except httpx.RequestError as e:
        return False, f"Error connecting to server: {str(e)}"


def render_auth_page():
    """Displays the authentication page."""
    st.title("Personal Finance Tracker")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        st.header("Login")
        login_username = st.text_input("Username", key="login_username")
        login_password = st.text_input(
            "Password", type="password", key="login_password"
        )

        if st.button("Login"):
            if login_username and login_password:
                success, message = login_user(login_username, login_password)
                if success:
                    st.success(message)
                    st.session_state["page"] = "records"
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.error("Please fill in all fields")

    with tab2:
        st.header("Register")
        reg_username = st.text_input("Username", key="reg_username")
        reg_password = st.text_input(
            "Password", type="password", key="reg_password"
        )

        if st.button("Register"):
            if reg_username and reg_password:
                success, message = register_user(reg_username, reg_password)
                if success:
                    st.success(message)
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = reg_username
                    st.session_state["page"] = "records"
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.error("Please fill in all fields")
