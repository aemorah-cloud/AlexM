import json
import boto3
import requests
from datetime import datetime
import os

s3 = boto3.client("s3")

def lambda_handler(event, context):

    API_KEY = os.environ["WEATHER_API_KEY"]
    BUCKET_NAME = os.environ["S3_BUCKET_NAME"]
    CITY = "Toronto"

    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"weather_{CITY}_{timestamp}.json"

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=f"raw/{file_name}",
        Body=json.dumps(data)
    )

    return {
        "statusCode": 200,
        "body": json.dumps("Data uploaded successfully")
    }