
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def forecast_next_month(transactions_df):
    if transactions_df.empty or 'amount' not in transactions_df.columns or 'date' not in transactions_df.columns:
        return "Insufficient data to forecast."

    transactions_df['date'] = pd.to_datetime(transactions_df['date'])
    transactions_df.set_index('date', inplace=True)

    # Group by month and sum amounts
    monthly_data = transactions_df.resample('M').sum(numeric_only=True)

    if len(monthly_data) < 2:
        return "Not enough monthly data to forecast."

    # Simple forecast using average of previous months
    forecast = monthly_data['amount'].mean()
    next_month = (monthly_data.index[-1] + pd.DateOffset(months=1)).strftime('%B %Y')

    return f"Forecasted spending for {next_month}: ${forecast:.2f}"
