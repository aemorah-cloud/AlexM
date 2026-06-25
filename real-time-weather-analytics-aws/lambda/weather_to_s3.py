import requests
import json
import boto3
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# ---------- CONFIG ----------
API_KEY = os.getenv("WEATHER_API_KEY")
CITY = "Toronto"
BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

# ---------- GET WEATHER ----------
url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
response = requests.get(url)

data = response.json()

# ---------- CREATE FILE ----------
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
file_name = f"weather_{CITY}_{timestamp}.json"

# ---------- SAVE LOCALLY (optional) ----------
with open(file_name, "w") as f:
    json.dump(data, f, indent=2)

# ---------- UPLOAD TO S3 ----------
s3 = boto3.client("s3")

s3.upload_file(file_name, BUCKET_NAME, f"raw/{file_name}")

print("✅ Uploaded to S3 successfully!")