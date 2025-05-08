import ssl

import httpx
import streamlit as st

from app.config import settings

if "client" not in st.session_state:
    context = ssl.create_default_context(
        cafile=str(settings.auth_jwt.cert_path)
    )
    st.session_state.client = httpx.Client(verify=context)

client = st.session_state.client


def get_data():
    """Retrieves all financial records."""
    try:
        response = client.get(settings.api_endpoints.financial_records_url)
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Error getting data")
    except httpx.RequestError as e:
        st.error(f"Connection error: {e}")
    return []


def create_record(data):
    """Creates a new financial record."""
    try:
        response = client.post(
            settings.api_endpoints.financial_records_url, json=data
        )
        return response.status_code == 200
    except httpx.RequestError as e:
        st.error(f"Failed to create record: {e}")
        return False


def delete_record(record_id):
    """Deletes a financial record by its ID."""
    try:
        response = client.delete(
            f"{settings.api_endpoints.financial_records_url}{record_id}"
        )
        return response.status_code == 204
    except httpx.RequestError as e:
        st.error(f"Failed to delete record: {e}")
        return False


def update_record(record_id, data):
    """Updates an existing financial record."""
    try:
        response = client.put(
            f"{settings.api_endpoints.financial_records_url}{record_id}",
            json=data,
        )
        return response.status_code == 204
    except httpx.RequestError as e:
        st.error(f"Failed to update record: {e}")
        return False


def logout_user():
    """Log out the current user."""
    try:
        response = client.post(settings.api_endpoints.logout_url)
        if response.status_code == 200:
            client.cookies.clear()
            st.session_state.clear()
            st.success("Logged out successfully")
        else:
            st.error(
                f"Logout failed: "
                f"{response.json().get('detail', 'Unknown error')}"
            )
    except httpx.RequestError as e:
        st.error(f"Error connecting to server: {str(e)}")

    st.rerun()


def get_categories():
    """Retrieves all categories."""
    try:
        response = client.get(settings.api_endpoints.categories_url)
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Error getting categories")
            return []
    except httpx.RequestError as e:
        st.error(f"Connection error: {e}")
        return []


def create_category(data):
    """Creates a new category."""
    try:
        existing_categories = get_categories()
        category_name = data.get("name", "").strip()
        if not category_name:
            st.error("The name of a category cannot be empty")
            return None
        for category in existing_categories:
            if category.get("name").strip().lower() == category_name.lower():
                st.error(
                    f"Category with name '{category_name}' already exists"
                )
                return None
        data["name"] = category_name.capitalize()
        response = client.post(
            settings.api_endpoints.categories_url, json=data
        )
        if response.status_code == 200:
            return response.json()
    except httpx.RequestError as e:
        st.error(f"Failed to create category: {e}")
        return None


def delete_category(category_id: int):
    """Deletes a category by its ID."""
    try:
        response = client.delete(
            f"{settings.api_endpoints.categories_url}{category_id}"
        )
        return response.status_code == 204
    except httpx.RequestError as e:
        st.error(f"Failed to delete category: {e}")
        return False
