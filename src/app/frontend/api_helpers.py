import httpx
import streamlit as st
from app.config import settings


if "client" not in st.session_state:
    st.session_state.client = httpx.Client(verify=False)

client = st.session_state.client


def get_data():
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
    try:
        response = client.post(settings.api_endpoints.financial_records_url, json=data)
        return response.status_code == 200
    except httpx.RequestError as e:
        st.error(f"Failed to create record: {e}")
        return False


def delete_record(record_id):
    try:
        response = client.delete(
            f"{settings.api_endpoints.financial_records_url}{record_id}"
        )
        return response.status_code == 204
    except httpx.RequestError as e:
        st.error(f"Failed to delete record: {e}")
        return False


def update_record(record_id, data):
    try:
        response = client.put(
            f"{settings.api_endpoints.financial_records_url}{record_id}", json=data
        )
        return response.status_code == 204
    except httpx.RequestError as e:
        st.error(f"Failed to update record: {e}")
        return False


def logout_user():
    try:
        response = client.post(settings.api_endpoints.logout_url)
        if response.status_code == 200:
            client.cookies.clear()
            st.session_state.clear()
            st.success("Logged out successfully")
        else:
            st.error(f"Logout failed: {response.json().get('detail', 'Unknown error')}")
    except httpx.RequestError as e:
        st.error(f"Error connecting to server: {str(e)}")

    st.rerun()


def get_categories():
    try:
        response = requests.get(settings.api_url_categories)
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Error getting categories")
    except Exception as e:
        st.error(f"Connection error: {e}")
    return []


def create_category(data):
    try:
        response = requests.post(settings.api_url_categories, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error creating category. This name may already be in use")
            return None
    except Exception as e:
        st.error(f"Connection error: {e}")
        return None


def delete_category(category_id: int):
    response = requests.delete(f"{settings.api_url_categories}{category_id}")
    return response.status_code == 204
