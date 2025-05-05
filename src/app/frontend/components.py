from datetime import datetime

import streamlit as st

from app.frontend.api_helpers import (
    create_record,
    update_record,
    delete_record,
    create_category,
    delete_category,
)


def render_create_form():
    with st.expander("➕ Add financial record", expanded=False):
        with st.form("create_form"):
            record_type = st.selectbox("Type", ["Income", "Expense"])
            description = st.text_input("Description")
            amount = st.number_input("Amount", step=100.00, format="%.2f")
            date = st.date_input("Date")
            time = st.time_input("Time", step=60)
            category_options = ["➕ Add And Select New Category"] + [
                c["name"] for c in st.session_state.categories
            ]
            selected_category = st.selectbox(
                "Category", options=category_options, index=1
            )
            new_category = None
            if selected_category == "➕ Add And Select New Category":
                new_category = st.text_input(
                    "New Category Name", placeholder="Enter new category name"
                )
            submitted = st.form_submit_button("Create")
            if submitted:
                if selected_category == "➕ Add And Select New Category":
                    if not new_category or not new_category.strip():
                        st.info(
                            "Enter a name for the new category to add it to the list"
                        )
                        return
                    created = create_category({"name": new_category.strip()})
                    if created:
                        st.session_state.categories.append(created)
                        category_id = created["id"]
                    else:
                        st.error("Failed to create category")
                        return
                else:
                    category = next(
                        (
                            c
                            for c in st.session_state.categories
                            if c["name"] == selected_category
                        ),
                        None,
                    )
                    if category:
                        category_id = category["id"]
                    else:
                        st.error("Invalid category selection")
                        return
                data = {
                    "type": record_type.lower(),
                    "description": description.strip(),
                    "amount": float(amount),
                    "date": str(datetime.combine(date, time)),
                    "category_id": category_id,
                }
                if create_record(data):
                    st.success("Record created!")
                    st.session_state.refresh_records = True
                    st.rerun()
                else:
                    st.error("Server validation failed")


def render_edit_form(record):
    with st.form(f"edit_form_{record['id']}"):
        edit_key = f"edit_mode_{record['id']}"
        st.markdown(f"#### ✏️ Edit Record {record['id']}")
        record_type = st.selectbox(
            "Type",
            ["Income", "Expense"],
            index=0 if record["type"].lower() == "income" else 1,
        )
        description = st.text_input("Description", value=record["description"])
        amount = st.number_input("Amount", step=100.00, value=float(record["amount"]))
        record_datetime = datetime.fromisoformat(record["date"])
        date = st.date_input("Date", value=record_datetime.date())
        time = st.time_input("Time", value=record_datetime.time(), step=60)
        category_options = ["➕ Add And Select New Category"] + [
            c["name"] for c in st.session_state.categories
        ]
        current_category = next(
            (
                c["name"]
                for c in st.session_state.categories
                if c["id"] == record["category_id"]
            ),
            None,
        )
        selected_category = st.selectbox(
            "Category",
            options=category_options,
            index=(
                category_options.index(current_category)
                if current_category in category_options
                else 0
            ),
        )
        new_category = None
        if selected_category == "➕ Add And Select New Category":
            new_category = st.text_input(
                "New Category Name", placeholder="Enter new category name"
            )
        submitted = st.form_submit_button("Save")
        if submitted:
            if not description.strip():
                st.error("Description cannot be empty")
                return
            if selected_category == "➕ Add And Select New Category":
                if not new_category or not new_category.strip():
                    st.info("Enter a name for the new category to add it to the list")
                    return
                created = create_category({"name": new_category.strip()})
                if created:
                    st.session_state.categories.append(created)
                    category_id = created["id"]
                else:
                    st.error("Failed to create category")
                    return
            else:
                category = next(
                    (
                        c
                        for c in st.session_state.categories
                        if c["name"] == selected_category
                    ),
                    None,
                )
                if category:
                    category_id = category["id"]
                else:
                    st.error("Invalid category selection")
                    return
            updated_data = {
                "type": record_type.lower(),
                "description": description.strip(),
                "amount": float(amount),
                "date": datetime.combine(date, time).isoformat(),
                "category_id": category_id,
            }
            if update_record(record["id"], updated_data):
                st.success("Record updated successfully")
                st.session_state[edit_key] = False
                st.session_state.refresh_records = True
                st.rerun()
            else:
                st.error("Failed to update record")


def render_records():
    st.header("All financial records")
    records = st.session_state.records
    if not records:
        st.info("There are no financial records.")
        return
    category_map = {c["id"]: c["name"] for c in st.session_state.categories}
    st.markdown("---")
    for record in records:
        edit_key = f"edit_mode_{record['id']}"
        if edit_key not in st.session_state:
            st.session_state[edit_key] = False
        col1, col2, col3, col4, col5, col6 = st.columns([1.25, 3, 1.5, 2, 2.5, 1.75])
        with col1:
            color = "green" if record["type"] == "income" else "red"
            text = record["type"].capitalize()
            st.markdown(
                f"<span style='color: {color}; font-weight: 700;'>{text}</span>",
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(f"**{record['description']}**")
        with col3:
            st.write(f"{record['amount']:.2f}")
        with col4:
            date_str = record["date"].replace("Z", "")
            date_obj = datetime.fromisoformat(date_str)
            st.write(date_obj.strftime("%b %d, %Y %H:%M"))
        with col5:
            category_name = category_map.get(record["category_id"])
            st.markdown(f"<span class='badge'>{category_name}</span>", unsafe_allow_html=True)
        with col6:
            cols_btn = st.columns([1, 1])
            with cols_btn[0]:
                if st.button("✏️", key=f"edit_{record['id']}"):
                    st.session_state[edit_key] = not st.session_state[edit_key]
            with cols_btn[1]:
                if st.button("🗑", key=f"delete_{record['id']}"):
                    if delete_record(record["id"]):
                        st.success("✔")
                        st.session_state.refresh_records = True
                        st.rerun()
                    else:
                        st.error("✖")
        if st.session_state[edit_key]:
            render_edit_form(record)
        st.markdown("---")


def render_categories():
    st.header("Categories")
    for category in st.session_state.categories:
        col1, col2, col3 = st.columns([6, 2, 2])
        with col1:
            st.write(f"**{category['name']}**")
        with col2:
            st.write("")
        with col3:
            if st.button("🗑 Delete", key=f"delete_cat_{category['id']}"):
                if delete_category(category["id"]):
                    st.success("Category deleted successfully")
                    st.session_state.categories = [
                        c
                        for c in st.session_state.categories
                        if c["id"] != category["id"]
                    ]
                    st.session_state.refresh_records = True
                    st.rerun()
                else:
                    st.error("Failed to delete category (may be in use)")
    with st.form("create_category_form"):
        new_category_name = st.text_input("New Category Name")
        if st.form_submit_button("Add Category"):
            if new_category_name.strip():
                created = create_category({"name": new_category_name.strip()})
                if created:
                    st.success("Category created")
                    st.session_state.categories.append(created)
                    st.rerun()
                else:
                    return
            else:
                st.error("Category name cannot be empty")
