import streamlit as st
from user import register_user, authenticate_user
from transaction import submit_transaction, fetch_transactions
from forecast import forecast_spending
from recommender import generate_recommendations
from budget import compare_budget_vs_actual
from database import create_tables
from datetime import date

# Initialize database tables
create_tables()

st.set_page_config(page_title="WiseBudget", layout="wide")
st.title("💸 WiseBudget: Personal Finance Assistant")
st.markdown("Securely manage your expenses, forecast future spending, and receive personalized financial tips.")

menu = ["Login", "Register", "Dashboard"]
choice = st.sidebar.selectbox("Navigation", menu)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None

# Registration Page
if choice == "Register":
    st.subheader("Create New Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        if register_user(username, password):
            st.success("Account created successfully. Please log in.")
        else:
            st.error("Username already exists.")

# Login Page
elif choice == "Login":
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user_id = authenticate_user(username, password)
        if user_id:
            st.session_state.logged_in = True
            st.session_state.user_id = user_id
            st.success(f"Welcome, {username}!")
        else:
            st.error("Invalid username or password.")

# Dashboard
elif choice == "Dashboard" and st.session_state.logged_in:
    st.success(f"Logged in as user ID: {st.session_state.user_id}")
    tab1, tab2, tab3, tab4 = st.tabs(["💾 Add Transaction", "📊 Budget Dashboard", "🔮 Forecast", "🎯 Recommendations"])

    with tab1:
        st.subheader("Add Transaction")
        category = st.selectbox("Category", ["Income", "Needs", "Wants", "Savings"])
        amount = st.number_input("Amount", min_value=0.0, step=0.01)
        description = st.text_input("Description")
        txn_date = st.date_input("Date", value=date.today())
        if st.button("Submit Transaction"):
            submit_transaction(st.session_state.user_id, str(txn_date), category, amount, description)
            st.success("Transaction added!")

    with tab2:
        st.subheader("Budget Overview")
        data = fetch_transactions(st.session_state.user_id)
        if data:
            compare_budget_vs_actual(data)
        else:
            st.info("No transaction data found.")

    with tab3:
        st.subheader("Forecast Future Spending")
        data = fetch_transactions(st.session_state.user_id)
        if data:
            forecast = forecast_spending(data)
            st.metric("Next Forecasted Spending", f"${forecast:.2f}")
        else:
            st.warning("Forecasting requires transaction data.")

    with tab4:
        st.subheader("Recommendations")
        data = fetch_transactions(st.session_state.user_id)
        if data:
            for txn in data:
                tip = generate_recommendations(txn["category"], txn["amount"])
                st.info(f"{txn['date']} - {tip}")
        else:
            st.warning("No transactions to analyze.")

elif choice == "Dashboard":
    st.warning("Please log in to access the dashboard.")
