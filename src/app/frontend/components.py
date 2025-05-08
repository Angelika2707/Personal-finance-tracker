import io
from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

from app.frontend.api_helpers import (
    create_record,
    update_record,
    delete_record,
    create_category,
    delete_category,
)
from app.frontend.api_helpers import generate_pdf_report


def render_create_form():
    """Renders the form for creating a new financial record."""
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
                            "Enter a name for the new category "
                            "to add it to the list"
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
    """Renders the form for editing an existing financial record."""
    with st.form(f"edit_form_{record['id']}"):
        edit_key = f"edit_mode_{record['id']}"
        st.markdown(f"#### ✏️ Edit Record {record['id']}")
        record_type = st.selectbox(
            "Type",
            ["Income", "Expense"],
            index=0 if record["type"].lower() == "income" else 1,
        )
        description = st.text_input("Description", value=record["description"])
        amount = st.number_input(
            "Amount", step=100.00, value=float(record["amount"])
        )
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
                    st.info(
                        "Enter a name for the new category "
                        "to add it to the list"
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
    """Displays all financial records in a tabular layout."""
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
        col1, col2, col3, col4, col5, col6 = st.columns(
            [1.25, 3, 1.5, 2, 2.5, 1.75]
        )
        with col1:
            color = "green" if record["type"] == "income" else "red"
            text = record["type"].capitalize()
            st.markdown(
                f"<span style='color: {color}; "
                f"font-weight: 700;'>{text}</span>",
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
            st.markdown(
                f"<span class='badge'>{category_name}</span>",
                unsafe_allow_html=True,
            )
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
    """Displays and manages financial categories."""
    st.header("Categories")
    for category in st.session_state.categories:
        col1, col2, col3 = st.columns([6, 2, 2])
        with col1:
            st.markdown(
                f"<span class='badge'>{category['name']}</span>",
                unsafe_allow_html=True,
            )
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


def render_analytics():
    """Renders financial analytics."""
    st.header("Financial Analytics")

    records = st.session_state.records
    if not records:
        st.info("No records available for analysis")
        return

    df = pd.DataFrame(records)
    df["date"] = pd.to_datetime(df["date"])
    df["amount"] = pd.to_numeric(df["amount"])

    category_map = {c["id"]: c["name"] for c in st.session_state.categories}
    df["category_name"] = df["category_id"].map(category_map)

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start date", value=df["date"].min().date())
    with col2:
        end_date = st.date_input("End date", value=df["date"].max().date())

    mask = (df["date"] >= pd.to_datetime(start_date)) & (
        df["date"] <= pd.to_datetime(end_date)
    )
    filtered_df = df.loc[mask]

    selected_categories = st.multiselect(
        "Filter by categories",
        options=[c["name"] for c in st.session_state.categories],
        default=None,
    )

    if selected_categories:
        filtered_df = filtered_df[
            filtered_df["category_name"].isin(selected_categories)
        ]

    income_df = filtered_df[filtered_df["type"] == "income"]
    expense_df = filtered_df[filtered_df["type"] == "expense"]

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Total Overview",
            "By Category",
            "Daily Trends",
            "Statistics",
        ]
    )

    with tab1:
        st.subheader("Income vs Expenses")
        summary = filtered_df.groupby("type")["amount"].sum().reset_index()
        fig = px.pie(
            summary,
            values="amount",
            names="type",
            title="Income/Expense Distribution",
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Over Time")
        time_df = (
            filtered_df.groupby(["date", "type"])["amount"].sum().reset_index()
        )
        fig = px.line(
            time_df,
            x="date",
            y="amount",
            color="type",
            title="Income and Expenses Over Time",
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Category Analytics")

        if (
            not hasattr(st.session_state, "categories")
            or not st.session_state.categories
        ):
            st.warning("No categories available. Please add categories first.")
        elif filtered_df.empty:
            st.warning("No records available for selected period")
        else:
            category_map = {
                c["id"]: c["name"] for c in st.session_state.categories
            }
            filtered_df["category_name"] = filtered_df["category_id"].map(
                category_map
            )

            selected_categories = st.multiselect(
                "Select categories to analyze",
                options=list(category_map.values()),
                default=list(category_map.values()),
            )

            if selected_categories:
                filtered_df = filtered_df[
                    filtered_df["category_name"].isin(selected_categories)
                ]

            st.markdown("### Income vs Expenses by Category")
            cat_df = (
                filtered_df.groupby(["category_name", "type"])["amount"]
                .sum()
                .reset_index()
            )

            if not cat_df.empty:
                fig = px.bar(
                    cat_df,
                    x="category_name",
                    y="amount",
                    color="type",
                    barmode="group",
                    title="Income and Expenses by Category",
                    labels={
                        "category_name": "Category",
                        "amount": "Amount",
                        "type": "Type",
                    },
                    color_discrete_map={"income": "green", "expense": "red"},
                )
                st.plotly_chart(fig, use_container_width=True)

                st.markdown("### Expenses Distribution")
                expense_df = filtered_df[filtered_df["type"] == "expense"]
                if not expense_df.empty:
                    fig_pie = px.pie(
                        expense_df.groupby("category_name")["amount"]
                        .sum()
                        .reset_index(),
                        values="amount",
                        names="category_name",
                        title="Percentage of Expenses by Category",
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)
                else:
                    st.info("No expense data for selected period/categories")
            else:
                st.warning("No data available for selected filters")

    with tab3:
        st.subheader("Daily Trends")
        daily_df = (
            filtered_df.groupby(["date", "type"])["amount"].sum().reset_index()
        )
        fig = px.bar(
            daily_df,
            x="date",
            y="amount",
            color="type",
            title="Daily Income and Expenses",
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab4:
        st.subheader("Financial Statistics")

        if not expense_df.empty:
            avg_expense_per_day = (
                expense_df.groupby("date")["amount"].sum().mean()
            )
            st.metric("Average Daily Expenses", f"{avg_expense_per_day:.2f}")

        if not income_df.empty:
            avg_income_per_day = (
                income_df.groupby("date")["amount"].sum().mean()
            )
            st.metric("Average Daily Income", f"{avg_income_per_day:.2f}")

        col1, col2 = st.columns(2)
        with col1:
            total_income = income_df["amount"].sum()
            st.metric("Total Income", f"{total_income:.2f}")
        with col2:
            total_expense = expense_df["amount"].sum()
            st.metric("Total Expenses", f"{total_expense:.2f}")

        balance = total_income - total_expense
        st.metric(
            "Balance",
            f"{balance:.2f}",
            delta_color="inverse" if balance < 0 else "normal",
        )

    if not filtered_df.empty:
        st.markdown("---")
        col1, col2 = st.columns(2)

        with col1:

            def prepare_enhanced_csv(df):
                main_data = df[
                    ["date", "type", "category_name", "description", "amount"]
                ]

                category_stats = (
                    df.groupby(["category_name", "type"])["amount"]
                    .agg(["sum", "count", "mean"])
                    .reset_index()
                )
                category_stats.columns = [
                    "Category",
                    "Type",
                    "Total Amount",
                    "Transaction Count",
                    "Average Amount",
                ]

                total_stats = pd.DataFrame(
                    {
                        "Metric": [
                            "Total Income",
                            "Total Expenses",
                            "Balance",
                        ],
                        "Value": [
                            income_df["amount"].sum(),
                            expense_df["amount"].sum(),
                            income_df["amount"].sum()
                            - expense_df["amount"].sum(),
                        ],
                    }
                )

                output = io.StringIO()
                output.write("Main Transactions Data\n")
                main_data.to_csv(output, index=False)
                output.write("\n\nCategory Statistics\n")
                category_stats.to_csv(output, index=False)
                output.write("\n\nSummary Statistics\n")
                total_stats.to_csv(output, index=False)

                return output.getvalue()

            csv_data = prepare_enhanced_csv(filtered_df)
            st.download_button(
                label="Download Enhanced CSV",
                data=csv_data,
                file_name="financial_report_enhanced.csv",
                mime="text/csv",
            )

            with col2:
                if st.button("Generate PDF Report"):
                    with st.spinner("Generating PDF..."):
                        try:
                            pdf_data = generate_pdf_report(filtered_df)
                            if pdf_data:
                                st.download_button(
                                    label="Download PDF Report",
                                    data=pdf_data,
                                    file_name=f"financial_report_"
                                    f"{datetime.now().date()}.pdf",
                                    mime="application/pdf",
                                )
                            else:
                                st.error(
                                    "Failed to generate PDF - no data returned"
                                )
                        except Exception as e:
                            st.error(f"PDF generation failed: {str(e)}")
