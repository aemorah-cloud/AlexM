import json
import boto3
import urllib.request
import os
from datetime import datetime

s3 = boto3.client("s3")


def fetch_weather():
    API_KEY = os.environ["WEATHER_API_KEY"]
    CITY = "Toronto"

    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())

    return data

def transform_weather(data):
    return {
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "city": data["name"],
        "country": data["sys"]["country"],

        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "temp_min": data["main"]["temp_min"],
        "temp_max": data["main"]["temp_max"],

        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "visibility": data.get("visibility", None),

        "wind_speed": data["wind"]["speed"],
        "wind_direction": data["wind"].get("deg", None),
        "wind_gust": data["wind"].get("gust", None),

        "cloudiness": data["clouds"]["all"],

        "weather": data["weather"][0]["main"],
        "description": data["weather"][0]["description"],

        "sunrise": data["sys"]["sunrise"],
        "sunset": data["sys"]["sunset"]
    }


def upload_to_s3(clean_data):
    BUCKET_NAME = os.environ["S3_BUCKET_NAME"]

    timestamp = clean_data["timestamp"].replace(":", "-")
    file_name = f"weather_Toronto_{timestamp}.json"

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=f"raw/{file_name}",
        Body=json.dumps(clean_data)
    )


def lambda_handler(event, context):
    raw_data = fetch_weather()
    clean_data = transform_weather(raw_data)
    upload_to_s3(clean_data)

    return {
        "statusCode": 200,
        "body": json.dumps("Weather data uploaded successfully")
    }