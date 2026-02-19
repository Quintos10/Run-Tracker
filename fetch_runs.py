import os, json
from garminconnect import Garmin

email = os.environ["GARMIN_EMAIL"]
password = os.environ["GARMIN_PASSWORD"]

client = Garmin(email, password)
client.login()

activities = client.get_activities(0, 100)
runs = [a for a in activities if 'RUN' in a.get('activityType', {}).get('typeKey', '').upper()]

clean = [{
    'date': a['startTimeLocal'][:10],
    'name': a['activityName'],
    'distance_km': round(a['distance'] / 1000, 2),
    'moving_time_min': round(a['movingDuration'] / 60),
    'avg_pace_min_per_km': round(1000 / a['averageSpeed'] / 60, 2) if a.get('averageSpeed') else None,
    'elevation_m': a.get('elevationGain'),
    'avg_hr': a.get('averageHR'),
    'max_hr': a.get('maxHR'),
    'calories': a.get('calories'),
    'avg_cadence': a.get('averageRunningCadenceInStepsPerMinute')
} for a in runs]

with open('runs.json', 'w') as f:
    json.dump(clean, f)

print(f"Saved {len(clean)} runs to runs.json")
