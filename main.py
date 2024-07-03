import csv
from datetime import datetime
import requests

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

def save_to_csv(data, city, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['city', 'date', 'temperature', 'feels_like', 'humidity', 'description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for date, weather in data.items():
            writer.writerow({
                'city': city,
                'date': date,
                'temperature': weather['temp'],
                'feels_like': weather['feels_like'],
                'humidity': weather['humidity'],
                'description': weather['description']
            })

def main():
    # Replace 'YOUR_API_KEY' with your actual OpenWeatherMap API key
    api_key = 'YOUR_API_KEY'
    cities = ['London', 'Manchester', 'Edinburgh']
    
    for city in cities:
        print(f"Fetching weather data for {city}...")
        weather_data = get_weather_data(city, api_key)
        
        if weather_data:
            filename = f"{city.lower()}_weather_data.csv"
            save_to_csv(weather_data, city, filename)
            print(f"Weather data for {city} saved to {filename}")
        else:
            print(f"Failed to fetch weather data for {city}")
        
        print("---")

if __name__ == "__main__":
    main()
