import pandas as pd
import streamlit as st

def compare_budget_vs_actual(data):
    df = pd.DataFrame(data)
    category_totals = df.groupby("category")["amount"].sum()

    budget = {
        "Needs": 50,
        "Wants": 30,
        "Savings": 20
    }

    actual = category_totals.to_dict()
    actual_percent = {
        k: (v / category_totals.sum()) * 100 for k, v in actual.items()
    }

    st.subheader("Budget Comparison")
    st.write("Expected Budget Distribution:")
    st.json(budget)
    st.write("Your Actual Spending Distribution:")
    st.json({k: f"{v:.2f}%" for k, v in actual_percent.items()})
