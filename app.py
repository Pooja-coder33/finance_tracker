import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from db import init_db, add_transaction, fetch_data, add_user, login_user

# --- MUST be first Streamlit command ---
st.set_page_config(page_title="💰 Personal Finance Manager", layout="wide")

# --- Initialize Database ---
init_db()

# --- Session States ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None

# --- App Title ---
st.title("💰 Personal Finance Manager")

menu = ["Login", "Register"]
choice = st.sidebar.selectbox("Menu", menu)

# --- REGISTER SECTION ---
if choice == "Register":
    st.subheader("Create New Account")
    new_username = st.text_input("Username")
    new_password = st.text_input("Password", type="password")

    if st.button("Register"):
        result = add_user(new_username, new_password)
        if result == "exists":
            st.warning("⚠️ Username already exists. Please choose another.")
        else:
            st.success("✅ Account created successfully! Please log in.")

# --- LOGIN SECTION ---
elif choice == "Login":
    st.subheader("Login to Your Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user_id = login_user(username, password)
        if user_id:
            st.session_state.logged_in = True
            st.session_state.user_id = user_id
            st.success(f"✅ Logged in as {username}")
        else:
            st.error("❌ Invalid credentials")

# --- MAIN APP SECTION ---
if st.session_state.logged_in:
    st.sidebar.success("You are logged in.")
    option = st.sidebar.radio("Navigation", ["Add Transaction", "View Transactions"])

    # --- ADD TRANSACTION ---
    if option == "Add Transaction":
        st.subheader("➕ Add New Transaction")
        date = st.date_input("Date")
        category = st.selectbox("Category", ["Food", "Travel", "Shopping", "Bills", "Salary", "Other"])
        amount = st.number_input("Amount", min_value=0.0, format="%.2f")
        type_ = st.radio("Type", ["Income", "Expense"])
        description = st.text_input("Description")
        notes = st.text_area("Notes")

        if st.button("Add"):
            add_transaction(st.session_state.user_id, date, category, amount, type_, description, notes)
            st.success("✅ Transaction added successfully!")

    # --- VIEW TRANSACTIONS ---
    elif option == "View Transactions":
        st.subheader("📜 Transaction History")

        df = fetch_data(st.session_state.user_id)

        if not df.empty:
            st.dataframe(df)

            total_income = df[df["type"] == "Income"]["amount"].sum()
            total_expense = df[df["type"] == "Expense"]["amount"].sum()
            balance = total_income - total_expense

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Income", f"₹{total_income:.2f}")
            col2.metric("Total Expense", f"₹{total_expense:.2f}")
            col3.metric("Balance", f"₹{balance:.2f}")

            # --- Visualization Section ---
            st.subheader("📊 Visualize Your Finances")

            # Pie chart: Expense distribution by category
            expense_data = df[df["type"] == "Expense"].groupby("category")["amount"].sum()

            if not expense_data.empty:
                fig1, ax1 = plt.subplots()
                ax1.pie(expense_data, labels=expense_data.index, autopct="%1.1f%%", startangle=90)
                ax1.axis("equal")
                st.pyplot(fig1)
            else:
                st.info("No expenses to display in chart.")

            # Bar chart: Income vs Expense
            income_expense = df.groupby("type")["amount"].sum()
            if not income_expense.empty:
                fig2, ax2 = plt.subplots()
                ax2.bar(income_expense.index, income_expense.values)
                ax2.set_title("Income vs Expense")
                ax2.set_ylabel("Amount (₹)")
                st.pyplot(fig2)
            else:
                st.info("No transactions for bar chart visualization.")
        else:
            st.info("No transactions yet.")

else:
    st.info("👋 Please log in or register to use the Finance Manager.")
