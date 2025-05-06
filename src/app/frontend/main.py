import streamlit as st

from auth_page import render_auth_page
from records_page import render_records_page

st.markdown(
    """
    <style>
        div.stTabs button div p {
            font-size: 1.25rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


if __name__ == "__main__":
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "username" not in st.session_state:
        st.session_state["username"] = ""
    if "access_token" not in st.session_state:
        st.session_state["access_token"] = ""
    if "page" not in st.session_state:
        st.session_state["page"] = "auth"

    if st.session_state["logged_in"]:
        render_records_page()
    else:
        render_auth_page()
