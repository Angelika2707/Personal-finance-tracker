import streamlit as st

from auth_page import render_auth_page
from records_page import render_records_page

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
