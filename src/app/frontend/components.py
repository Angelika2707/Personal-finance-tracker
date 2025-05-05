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


def render_analytics():
    st.header("Financial Analytics")

    # Получаем данные из сессии
    records = st.session_state.records
    if not records:
        st.info("No records available for analysis")
        return

    # Конвертируем в DataFrame
    df = pd.DataFrame(records)
    df['date'] = pd.to_datetime(df['date'])
    df['amount'] = pd.to_numeric(df['amount'])

    # Фильтры даты
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start date", value=df['date'].min().to_pydatetime())
    with col2:
        end_date = st.date_input("End date", value=df['date'].max().to_pydatetime())

    # Фильтрация данных
    mask = (df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))
    filtered_df = df.loc[mask]

    # Разделяем доходы и расходы
    income_df = filtered_df[filtered_df['type'] == 'income']
    expense_df = filtered_df[filtered_df['type'] == 'expense']

    # Вкладки для разных графиков
    tab1, tab3, tab4 = st.tabs(["Total Overview",
                                #   "By Category",
                                "Daily Trends",
                                "Statistics"])

    with tab1:
        # График общих доходов/расходов
        st.subheader("Income vs Expenses")
        summary = filtered_df.groupby('type')['amount'].sum().reset_index()
        fig = px.pie(summary, values='amount', names='type',
                     title="Income/Expense Distribution")
        st.plotly_chart(fig, use_container_width=True)

        # График по времени
        st.subheader("Over Time")
        time_df = filtered_df.groupby(['date', 'type'])['amount'].sum().reset_index()
        fig = px.line(time_df, x='date', y='amount', color='type',
                      title="Income and Expenses Over Time")
        st.plotly_chart(fig, use_container_width=True)

    # with tab2:
    #     # График по категориям
    #     st.subheader("By Category")
    #     if 'category' in filtered_df.columns:
    #         cat_df = filtered_df.groupby(['category', 'type'])['amount'].sum().reset_index()
    #         fig = px.bar(cat_df, x='category', y='amount', color='type',
    #                     barmode='group', title="Spending by Category")
    #         st.plotly_chart(fig, use_container_width=True)
    #     else:
    #         st.warning("No category data available")

    with tab3:
        # Ежедневные тренды
        st.subheader("Daily Trends")
        daily_df = filtered_df.groupby(['date', 'type'])['amount'].sum().reset_index()
        fig = px.bar(daily_df, x='date', y='amount', color='type',
                     title="Daily Income and Expenses")
        st.plotly_chart(fig, use_container_width=True)

    with tab4:
        # Статистика
        st.subheader("Financial Statistics")

        # Средние значения
        if not expense_df.empty:
            avg_expense_per_day = expense_df.groupby('date')['amount'].sum().mean()
            st.metric("Average Daily Expenses", f"{avg_expense_per_day:.2f}")

        if not income_df.empty:
            avg_income_per_day = income_df.groupby('date')['amount'].sum().mean()
            st.metric("Average Daily Income", f"{avg_income_per_day:.2f}")

        # Суммарные значения
        col1, col2 = st.columns(2)
        with col1:
            total_income = income_df['amount'].sum()
            st.metric("Total Income", f"{total_income:.2f}")
        with col2:
            total_expense = expense_df['amount'].sum()
            st.metric("Total Expenses", f"{total_expense:.2f}")

        # Баланс
        balance = total_income - total_expense
        st.metric("Balance", f"{balance:.2f}",
                  delta_color="inverse" if balance < 0 else "normal")