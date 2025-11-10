import os
import json
import requests
import csv
import io

# Use the free NPS parks dataset from GitHub
url = 'https://raw.githubusercontent.com/gvenzl/sample-data/main/national-parks/parks.csv'

response = requests.get(url)
response.raise_for_status()

# Parse CSV
csv_reader = csv.DictReader(io.StringIO(response.text))

parks = []
for row in csv_reader:
    if 'National Park' in row['DESIGNATION']:
        lat = float(row['LATITUDE']) if row['LATITUDE'] else None
        lon = float(row['LONGITUDE']) if row['LONGITUDE'] else None
        if lat is not None and lon is not None:
            parks.append({
                'id': row['PARK_CODE'],
                'name': row['NAME'],
                'state': row['STATES'],
                'lat': lat,
                'lon': lon
            })

# Sort by name
parks.sort(key=lambda x: x['name'])

# Write to file
data_path = os.path.join(os.path.dirname(__file__), 'data', 'parks.json')
with open(data_path, 'w', encoding='utf-8') as f:
    json.dump(parks, f, indent=2)

print(f"Updated {len(parks)} parks in {data_path}")
