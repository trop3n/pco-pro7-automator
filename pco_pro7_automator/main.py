# env setup
import os
import requests
from datetime import datetime, timedelta
import logging
from dotenv import load_dotenv

load_dotenv() # load creds from .env

# configuration
PLANNING_CENTER_APP_ID = os.getenv('PC_APP_ID')
PLANNING_CENTER_SECRET = os.getenv('PC_SECRET')
PROPRESENTER_API_KEY = os.getenv('PROP_API_KEY')
SERVICE_DATE = (datetime.now() + timedelta(days=7)).date()

# Planning Center API Client
class PlanningCenterClient:
    def __init__(self):
        self.base_url = "https://api.planningcenteronline.com/services/v2"
        self.auth = (PLANNING_CENTER_APP_ID, PLANNING_CENTER_SECRET)

    def get_service_plan(self. date):
        endpoint = f"{self.base_url}/service_plans"
        params = {'filter': f'future|{date}'}
        response = requests.get(endpoint, params=params, auth=self.auth)
        response.raise_for_status()
        return response.json()