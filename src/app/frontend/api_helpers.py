import requests

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
    response = requests.post(settings.api_url_records, json=data)
    return response.status_code == 200


def delete_record(record_id):
    response = requests.delete(f"{settings.api_url_records}{record_id}")
    return response.status_code == 204


def update_record(record_id, data):
    response = requests.put(f"{settings.api_url_records}{record_id}", json=data)
    return response.status_code == 204
