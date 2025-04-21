import streamlit as st

from app.frontend.api_helpers import get_data
from app.frontend.components import render_create_form, render_records


def main():
    st.title("Financial Records")

    if "refresh" not in st.session_state:
        st.session_state.refresh = True

    if st.session_state.refresh:
        st.session_state.records = get_data()
        st.session_state.refresh = False

    render_create_form()
    render_records()


if __name__ == "__main__":
    main()
