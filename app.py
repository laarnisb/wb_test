import streamlit as st
from transaction import submit_transaction
from forecast import forecast_next_month
from recommender import generate_recommendation

st.set_page_config(page_title="WiseBudget", layout="centered")

st.title("💸 WiseBudget: Personal Finance Assistant")

menu = st.sidebar.selectbox("Navigation", ["Add Transaction", "Forecast", "Get Recommendation"])

if menu == "Add Transaction":
    st.subheader("Add a New Transaction")
    user_id = st.text_input("User ID")
    amount = st.number_input("Amount", step=0.01)
    category = st.text_input("Category")
    description = st.text_input("Description")
    if st.button("Submit"):
        submit_transaction(user_id, amount, category, description)
        st.success("Transaction submitted successfully.")

elif menu == "Forecast":
    st.subheader("Spending Forecast")
    user_id = st.text_input("User ID for Forecast")
    if st.button("Generate Forecast"):
        prediction = forecast_next_month(user_id)
        st.info(f"Predicted spending for next month: ${prediction:.2f}")

elif menu == "Get Recommendation":
    st.subheader("Personalized Financial Recommendation")
    user_id = st.text_input("User ID for Recommendation")
    if st.button("Get Tip"):
        tip = generate_recommendation(user_id)
        st.success(tip)
