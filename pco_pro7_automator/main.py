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
    
    def get_song_details(self, song_id):
        endpoint = f"{self.base_url}/songs/{song_id}"
        response = requests.get(endpoint, auth=self.auth)
        return response.json()
    
# ProPresenter API Client
class ProPresenterClient:
    def __init__(self):
        self.base_url = "http://propresenter.local:5000/api/v1"
        self.headers = {'Authorization': f'Bearer {PROPRESENTER_API_KEY}'}

    def create_playlist(self, playlist_name):
        endpoint = f"{self.base_url}/playlists"
        data = {'name': playlist_name}
        response = requests.post(endpoint, json=data, headers=self.headers)
        return response.json()
    
    def add_slide_group(self, playlist_id, song_data):
        endpoint = f"{self.base_url}/playlists/{playlist_id}/items"
        response= requests.post(endpoint, json=self._format_slide_data(song_data), headers=self.headers)
        return response.json()

    def _format_slide_data(self, song_data):
        return {
            'type': 'slide_group',
            'name': song_data['title'],
            'slides': self._parse_lyrics(song_data['lyrics'])
        }
    
# Main Workflow
def main():
    # init clients
    pc_client = PlanningCenterClient()
    prop_client = ProPresenterClient()

    try:
        # get service plan data
        service_plan = pc_client.get_service_plan(SERVICE_DATE)

        # create new playlist in ProPresenter
        playlist = prop_client.create_playlist(f"Service - {SERVICE_DATE}")

        # process each item in service plan
        for item in service_plan['data']:
            if item['type'] == 'Song':
                song_details = pc_client.get_song_details(item['relationships']['song']['data']['id'])
                prop_client.add_slide_group(playlist['id'], song_details)
        logging.info(f"Successfully created playlist {playlist['name']}")
    
    except Exception as e:
        logging.error(f"Error processing service plan: {str(e)}")

# Scheduling
if __name__ == "__main__":
    # For production: Use cron jon or AWS EventBridge
    main() # Test immediate execution