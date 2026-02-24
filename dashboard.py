import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Bears Scout: ROI Tracker", layout="wide")
st.title("📊 NBA Scouting Engine: Performance Dashboard")

# Points to your actual betting data
LOG_FILE = '/root/nba-engine/bet_ledger.csv'

if os.path.exists(LOG_FILE):
    df = pd.read_csv(LOG_FILE)
    if not df.empty:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df = df.sort_values('Timestamp')

        # Logic to handle profit/loss visualization
        def get_profit(row):
            if row['Result'] == 'WIN':
                odds = float(row['Odds'])
                dec = (odds/100 + 1) if odds > 0 else (100/abs(odds) + 1)
                return (dec - 1) * float(row['Kelly_Rec'])
            return -float(row['Kelly_Rec']) if row['Result'] == 'LOSS' else 0

        df['Profit'] = df.apply(get_profit, axis=1)
        df['Cumulative_Profit'] = df['Profit'].cumsum()

        # Metrics for the "Halas Hall" resume
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Profit", f"{df['Profit'].sum():.2f} units")
        win_count = len(df[df['Result']=='WIN'])
        total_bets = len(df[df['Result'].isin(['WIN','LOSS'])])
        col2.metric("Win Rate", f"{(win_count/total_bets*100 if total_bets > 0 else 0):.1f}%")
        col3.metric("Avg Edge", f"{df['EV_Edge'].mean():.2f}%")

        # The Chart
        fig = px.line(df, x='Timestamp', y='Cumulative_Profit', 
                      title='Bankroll Evolution Over Time',
                      template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Ledger is empty. Place some bets to see the data!")
else:
    st.warning(f"File not found: {LOG_FILE}. Make sure the engine has run at least once.")
