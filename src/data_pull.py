import requests
import json
import csv

url = 'https://api.tomorrow.io/v4/historical/normals'

#To get your tomorrow.io api key you will need to sign up at https://app.tomorrow.io/signup?planid=60d46beae90c3b3549a59ff3
apikey = 'YOUR API KEY'

locations = [
    "40.730610, -73.935242", # New York, NY
    "34.052235, -118.243683", # Los Angeles, CA
    "41.875562, -87.624421", # Chicago, IL
    "29.760427, -95.369803", # Houston, TX
    "33.448376, -112.074036" # Phoenix, AZ
]

fields = [
    'temperatureMin', 'temperatureMax', 'temperatureAvg',
    'dewPointMin', 'dewPointMax', 'dewPointAvg',
    'humidityMin', 'humidityMax', 'humidityAvg',
    'windSpeedMax', 'windSpeedMin', 'windSpeedAvg',
    'windSpeed100Max', 'windSpeed100Min', 'windSpeed100Avg',
    'windGustMin', 'windGustMax', 'windGustAvg',
    'cloudCoverMin', 'cloudCoverMax', 'cloudCoverAvg',
    'precipitationAccumulationSum', 'potentialEvaporationSum'
]
timesteps = ['1d']
start_date = '01-01'
end_date = '12-30'
units = 'metric'

for location in locations:
    data = {
        'location': location,
        'fields': fields,
        'timesteps': timesteps,
        'startDate': start_date,
        'endDate': end_date,
        'units': units
    }

    headers = {
        'Accept-Encoding': 'gzip',
        'accept': 'application/json',
        'content-type': 'application/json',
        'apikey': apikey
    }

    response = requests.post(url, data=json.dumps(data), headers=headers)

    if response.status_code != 200:
        print(f'Error: {response.content}')
        continue

    data = json.loads(response.content)

    filename = f'{location}.csv'
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['date', *fields])

        for item in data['data']['timelines'][0]['intervals']:
            row = [item['startDate']]
            for field in fields:
                row.append(item['values'][field])
            writer.writerow(row)
    print(f'Data for {location} is stored in {filename}')
