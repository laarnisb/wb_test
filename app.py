import streamlit as st
from database import insert_transaction, fetch_transactions, test_db_connection

st.set_page_config(page_title="WiseBudget App", layout="centered")

# App title
st.title("💸 WiseBudget: Personal Finance Tracker")

# Tabs for navigation
tab1, tab2, tab3 = st.tabs(["📥 Submit Transaction", "📊 View Transactions", "🔧 Diagnostics"])

# Submit Tab
with tab1:
    st.header("Add a Transaction")

    user_id = st.text_input("User ID")
    amount = st.number_input("Amount ($)", step=0.01)
    category = st.selectbox("Category", ["Needs", "Wants", "Savings"])
    description = st.text_input("Description")

    if st.button("Submit"):
        if user_id and description:
            try:
                insert_transaction(user_id, amount, category, description)
                st.success("Transaction submitted successfully!")
            except Exception as e:
                st.error(f"Failed to submit transaction: {e}")
        else:
            st.warning("Please fill in both User ID and Description.")

# View Tab
with tab2:
    st.header("Transaction History")

    view_user_id = st.text_input("Enter User ID to view transactions", key="view_user_id")

    if st.button("View Transactions"):
        if view_user_id:
            try:
                transactions = fetch_transactions(view_user_id)
                if transactions:
                    for t in transactions:
                        st.write(f"💵 **Amount**: ${t['amount']}")
                        st.write(f"📂 **Category**: {t['category']}")
                        st.write(f"📝 **Description**: {t['description']}")
                        st.write(f"📅 **Date**: {t['timestamp']}")
                        st.markdown("---")
                else:
                    st.info("No transactions found.")
            except Exception as e:
                st.error(f"Error fetching transactions: {e}")
        else:
            st.warning("Please enter a User ID.")

# Diagnostic Tab
with tab3:
    st.header("Connection Diagnostics")
    if st.button("Test Database Connection"):
        test_db_connection()
