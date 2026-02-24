import pandas as pd
import os

LOG_FILE = '/root/nba-engine/bet_ledger.csv'

def update_ledger_results():
    if not os.path.isfile(LOG_FILE):
        print("[!] No ledger found.")
        return

    df = pd.read_csv(LOG_FILE)
    
    # Ensure a 'Result' column exists
    if 'Result' not in df.columns:
        df['Result'] = 'PENDING'

    # Filter for bets that haven't been graded yet
    pending = df[df['Result'] == 'PENDING']
    
    if pending.empty:
        print("\n✅ All logged bets have been graded. Nothing to update.")
        return

    print(f"\n--- UNGRADED SCOUTING REPORTS ({len(pending)} FOUND) ---")
    
    for idx, row in pending.iterrows():
        print(f"\nID: {idx} | {row['Timestamp']}")
        print(f"Player: {row['Player']} | {row['Side']} {row['Line']} {row['Market']}")
        print(f"Odds: {row['Odds']} | Edge: {row['EV_Edge']}%")
        
        choice = input("Result? (w = Win, l = Loss, s = Skip/Push): ").lower()
        
        if choice == 'w':
            df.at[idx, 'Result'] = 'WIN'
        elif choice == 'l':
            df.at[idx, 'Result'] = 'LOSS'
        elif choice == 's':
            continue
            
    # Save the updated ledger
    df.to_csv(LOG_FILE, index=False)
    print("\n[+] Ledger updated successfully.")

if __name__ == "__main__":
    update_ledger_results()
