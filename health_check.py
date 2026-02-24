import subprocess
import os
import time
import requests
from datetime import datetime

# --- CONFIGURATION ---
NTFY_TOPIC = "NBA_Tool_Health"

def check_status():
    # Capture current time for logging
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    pgrep = subprocess.run(['pgrep', '-fl', 'sharp_nba_engine.py'], capture_output=True, text=True)
    process_active = pgrep.stdout != ""
    
    tmux_ls = subprocess.run(['tmux', 'ls'], capture_output=True, text=True)
    session_active = "nba_bot" in tmux_ls.stdout

    # This print statement now feeds the timestamp into your health_errors.log
    print(f"[{now}] Process: {'OK' if process_active else 'FAIL'} | Session: {'OK' if session_active else 'FAIL'}")

    if not process_active or not session_active:
        message = f"🚨 ALERT: NBA Engine is DOWN! Time: {now}"
        requests.post(f"https://ntfy.sh/{NTFY_TOPIC}", 
                      data=message.encode(encoding='utf-8'),
                      headers={"Title": "NBA Engine Critical Failure", "Priority": "5"})
