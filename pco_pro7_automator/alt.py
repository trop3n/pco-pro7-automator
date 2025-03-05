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
    response = requests.get(
        'https://api.planningcenteronline.com/services/v2/service_types/1/plans',
        headers=headers,
        params={'filter': f'week_start:{next_sunday.strftime("%Y-%m-%d")}'}
    )
    return response.json()['data'][0]

def parse_plan_data(plan):
    service_order = []
    for item in plan['attributes']['items']:
        if item['type'] == 'song':
            service_order.append({
                'title': item['title'],
                'lyrics': item['lyrics'],
                'presentation_order': item['presentation_order']
            })
    return sorted(service_order, key=lambda x: x['presentation_order'])

def create_propresenter_playlist(songs):
    for song in songs:
        presentation_data = {
            "name": song['title'],
            "slides": [{"text": line} for line in song['lyrics'].split('\n\n')]
        }
        response = requests.post(
            f'{PROPRESENTER_API_URL}/presentations',
            json=presentation_data,
            auth=PROPRESENTER_AUTH
        )

        # add to playlist
        requests.post(
            f'{PROPRESENTER_API_URL}/playlist',
            json={"presentationId": response.json()['id']},
            auth=PROPRESENTER_AUTH
        )

def weekly_sync():
    print("Starting weekly sync...")
    plan = get_planning_center_plan()
    service_data = parse_plan_data(plan)
    create_propresenter_playlist(service_data)
    print("Sync completed successfully")

# schedule the job
schedule.every().wednesday.at("08:00").do(weekly_sync)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)