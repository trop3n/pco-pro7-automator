import requests
import schedule
import time
from datetime import datetime, timedelta

# configuration
PLANNING_CENTER_API_KEY = 'your_pc_api_key'
PROPRESENTER_API_URL = 'http://localhost:8080' # Propresenter API Endpoint
PROPRESENTER_AUTH = ('user', 'pass') # if auth is required

def get_planning_center_plan():
    headers = {
        'Authorization': f'Bearer {PLANNING_CENTER_API_KEY}',
        'Content-Type': 'application/json'
    }

    # Get next Sunday's plan (adjust date logic as needed)
    next_sunday = datetime.now() + timedelta(days=(6 - datetime.now().weekday()))
    response = 