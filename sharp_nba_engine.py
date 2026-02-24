import os
from dotenv import load_dotenv
import requests
import time

# Load secrets from the .env file
load_dotenv()

# Professional Secret Management
ODDS_API_KEY = os.getenv('ODDS_API_KEY')
DISCORD_WEBHOOK = os.getenv('DISCORD_WEBHOOK')

# ... your existing logic continues below ...
