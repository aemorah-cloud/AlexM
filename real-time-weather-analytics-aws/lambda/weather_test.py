import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")

CITY = "Toronto"

url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
print("Fetching weather data for:", CITY)

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    
    print("🌦️ Weather Data Retrieved Successfully")
    print(json.dumps(data, indent=2))
else:
    print("❌ Error:", response.status_code)
    print(response.text)