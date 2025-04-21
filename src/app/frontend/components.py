import streamlit as st

from app.frontend.api_helpers import create_record, update_record, delete_record


def render_create_form():
    with st.expander("➕ Add financial record", expanded=False):
        with st.form("create_form"):
            record_type = st.selectbox("Type", ["income", "expense"])
            description = st.text_input("Description")
            amount = st.number_input("Amount", step=0.1)
            date = st.date_input("Date")

            submitted = st.form_submit_button("Create")
            if submitted:
                data = {
                    "type": record_type,
                    "description": description,
                    "amount": amount,
                    "date": str(date),
                }
                if create_record(data):
                    st.success("Successfully created record")
                    st.session_state.refresh = True
                    st.rerun()
                else:
                    st.error("Error creating record")


def render_edit_form(record):
    with st.form(f"edit_form_{record['id']}"):
        st.markdown(f"#### ✏️ Edit Record {record['id']}")
        record_type = st.selectbox(
            "Type", ["income", "expense"], index=0 if record["type"] == "income" else 1
        )
        description = st.text_input("Description", value=record["description"])
        amount = st.number_input("Amount", step=0.1, value=record["amount"])
        date = st.date_input("Date", value=record["date"])

        submitted = st.form_submit_button("Save")
        if submitted:
            updated_data = {
                "type": record_type,
                "description": description,
                "amount": amount,
                "date": str(date),
            }
            if update_record(record["id"], updated_data):
                st.success("Record updated successfully")
                st.session_state.refresh = True
                st.rerun()
            else:
                st.error("Failed to update record")


def render_records():
    st.header("All financial records")
    records = st.session_state.records

    if not records:
        st.info("There are no financial records.")
        return

    st.markdown("---")
    for record in records:
        edit_key = f"edit_mode_{record['id']}"
        if edit_key not in st.session_state:
            st.session_state[edit_key] = False

        col1, col2, col3, col4, col5, col6 = st.columns([1, 1.5, 2, 1.5, 2, 2])
        with col1:
            st.write(record["id"])
        with col2:
            st.write(record["type"])
        with col3:
            st.write(record["description"])
        with col4:
            st.write(record["amount"])
        with col5:
            st.write(record["date"])
        with col6:
            cols_btn = st.columns([1, 1])
            with cols_btn[0]:
                if st.button("✏️", key=f"edit_{record['id']}"):
                    st.session_state[edit_key] = not st.session_state[edit_key]
            with cols_btn[1]:
                if st.button("🗑", key=f"delete_{record['id']}"):
                    if delete_record(record["id"]):
                        st.success(f"Deleted: {record['description']}")
                        st.session_state.refresh = True
                        st.rerun()
                    else:
                        st.error("Error deleting record")

        if st.session_state[edit_key]:
            render_edit_form(record)

        st.markdown("---")
