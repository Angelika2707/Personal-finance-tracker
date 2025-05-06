import streamlit as st

from app.frontend.api_helpers import logout_user
from app.frontend.api_helpers import get_data, get_categories
from app.frontend.components import (
    render_create_form,
    render_records,
    render_categories,
    render_analytics,
)


def init_session_state():
    if "records" not in st.session_state or st.session_state.get(
        "refresh_records", False
    ):
        st.session_state.records = get_data()
        st.session_state.refresh_records = False
    if "categories" not in st.session_state or st.session_state.get(
        "refresh_categories", False
    ):
        st.session_state.categories = get_categories()
        st.session_state.refresh_categories = False


def render_records_page():
    st.markdown(
        """
            <style>
                div[class*="stColumn"] > div {
                    text-align: center;
                }
                div[class*="stColumn"] div.stButton {
                    display: flex;
                    justify-content: center;
                }
                div[class*="stColumn"] div.stColumns {
                    display: flex;
                    justify-content: center;
                }
                .badge {
                    display: inline-block;
                    background-color: #e0f2fe;
                    color: #1e3a8a;
                    padding: 4px 8px; 
                    border-radius: 12px;
                    font-size: 0.9rem;
                    font-weight: 700;
                }
            </style>
            """,
        unsafe_allow_html=True,
    )
    col1, col2 = st.columns([9, 1.25])
    with col2:
        if st.button("Logout"):
            logout_user()
            st.session_state["page"] = "auth"
            st.rerun()
    st.title("Financial Records")
    init_session_state()

    tab1, tab2, tab3 = st.tabs(["Records", "Categories", "Analytics"])
    with tab1:
        render_create_form()
        render_records()
    with tab2:
        render_categories()
    with tab3:
        render_analytics()
