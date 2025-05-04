import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

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
    tab1, tab2 = st.tabs(["Records", "Analytics"])
    
    records = st.session_state.records

    if not records:
        st.info("There are no financial records.")
        return

    st.markdown("---")
    with tab1:

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
        
    with tab2:
        render_analytics()

def render_analytics():
    st.header("📊 Financial Analytics")
    
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
