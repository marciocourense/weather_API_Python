import requests
from datetime import datetime

def get_weather_data(city, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    
    params = {
        "q": f"{city},UK",
        "appid": api_key,
        "units": "metric"
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        daily_data = {}
        
        for item in data['list']:
            date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
            
            if date not in daily_data:
                daily_data[date] = {
                    'temp': item['main']['temp'],
                    'feels_like': item['main']['feels_like'],
                    'humidity': item['main']['humidity'],
                    'description': item['weather'][0]['description']
                }
        
        return daily_data
    else:
        print(f"Error: {response.status_code}")
        return None

# Replace 'YOUR_API_KEY' with your actual OpenWeatherMap API key
api_key = 'YOUR_API_KEY'
city = 'London'

weather_data = get_weather_data(city, api_key)

if weather_data:
    for date, data in weather_data.items():
        print(f"Date: {date}")
        print(f"Temperature: {data['temp']}°C")
        print(f"Feels like: {data['feels_like']}°C")
        print(f"Humidity: {data['humidity']}%")
        print(f"Description: {data['description']}")
        print("---")
