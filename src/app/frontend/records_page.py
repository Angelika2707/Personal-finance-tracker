import streamlit as st

from app.frontend.api_helpers import logout_user
from components import render_create_form, render_records


def render_records_page():
    st.title("Financial Records")

    if "refresh" not in st.session_state:
        st.session_state.refresh = True

    if st.session_state.refresh:
        from api_helpers import get_data

        st.session_state.records = get_data()
        st.session_state.refresh = False

    render_create_form()
    render_records()

    if st.button("Logout"):
        logout_user()
        st.session_state["page"] = "auth"
        st.rerun()
