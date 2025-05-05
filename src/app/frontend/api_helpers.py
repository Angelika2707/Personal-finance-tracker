import requests
import streamlit as st

from app.config import settings


def get_data():
    try:
        response = requests.get(settings.api_url_records)
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Error getting data")
    except Exception as e:
        st.error(f"Connection error: {e}")
    return []


def create_record(data):
    print(data)
    response = requests.post(settings.api_url_records, json=data)
    return response.status_code == 200


def delete_record(record_id):
    response = requests.delete(f"{settings.api_url_records}{record_id}")
    return response.status_code == 204


def update_record(record_id, data):
    response = requests.put(f"{settings.api_url_records}{record_id}", json=data)
    return response.status_code == 204


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
