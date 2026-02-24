import pandas as pd
import os
from datetime import datetime

LOG_FILE = '/root/nba-engine/bet_ledger.csv'

def generate_professional_report():
    if not os.path.isfile(LOG_FILE):
        print("\n[!] DATA ERROR: No scouting ledger found.")
        return

    try:
        df = pd.read_csv(LOG_FILE)
        
        # Data Cleaning
        df['EV_Edge'] = pd.to_numeric(df['EV_Edge'], errors='coerce')
        df['Kelly_Rec'] = pd.to_numeric(df['Kelly_Rec'], errors='coerce')
        df['Odds'] = pd.to_numeric(df['Odds'], errors='coerce')
        
        # Calculate Actual Profit per bet
        # Formula: (Decimal Odds - 1) * Wager if WIN, else -Wager
        def calc_profit(row):
            if row['Result'] == 'WIN':
                # Convert American to Decimal for easy math
                odds = row['Odds']
                decimal_odds = (odds/100 + 1) if odds > 0 else (100/abs(odds) + 1)
                return (decimal_odds - 1) * row['Kelly_Rec']
            elif row['Result'] == 'LOSS':
                return -row['Kelly_Rec']
            return 0

        df['Actual_Profit'] = df.apply(calc_profit, axis=1)

        # High-Level Metrics
        total_signals = len(df)
        graded_bets = df[df['Result'].isin(['WIN', 'LOSS'])]
        wins = len(df[df['Result'] == 'WIN'])
        losses = len(df[df['Result'] == 'LOSS'])
        
        actual_profit = df['Actual_Profit'].sum()
        total_volume = graded_bets['Kelly_Rec'].sum()
        actual_roi = (actual_profit / total_volume * 100) if total_volume > 0 else 0
        expected_profit = (df['EV_Edge'].mean() / 100) * df['Kelly_Rec'].sum()

        # Dashboard Output
        print("="*55)
        print(f" NBA ANALYTICS - EXECUTIVE PROFIT REPORT")
        print(f" Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print("="*55)
        
        stats = [
            ["Total Market Triggers", f"{total_signals}"],
            ["Graded Record (W-L)", f"{wins}W - {losses}L"],
            ["Win Percentage", f"{(wins/len(graded_bets)*100 if len(graded_bets)>0 else 0):.1f}%"],
            ["Total Units Exposed", f"{total_volume:.2f}u"],
            ["Expected Net Profit", f"{expected_profit:.2f}u"],
            ["ACTUAL NET PROFIT", f"{actual_profit:.2f}u"],
            ["ACTUAL YIELD / ROI", f"{actual_roi:.2f}%"]
        ]

        for label, val in stats:
            print(f"{label:<30} | {val:>20}")

        print("-" * 55)
        if actual_profit > expected_profit:
            print(" PERFORMANCE: OVER-PERFORMING MODEL (Positive Variance)")
        elif actual_profit < 0:
            print(" PERFORMANCE: UNDER-PERFORMING (Check Model Calibration)")
        else:
            print(" PERFORMANCE: TRACKING WITHIN EXPECTED MARGINS")
        print("="*55 + "\n")

    except Exception as e:
        print(f"\n[!] ERROR: {e}\n")

if __name__ == "__main__":
    generate_professional_report()
