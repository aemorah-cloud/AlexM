import boto3
import pandas as pd
import time
import os
from dotenv import load_dotenv
from .sql_queries import (
    LATEST_WEATHER_QUERY,
    HISTORY_QUERY,
)

load_dotenv()

DATABASE  = os.getenv("ATHENA_DATABASE")
TABLE  = os.getenv("ATHENA_TABLE")
OUTPUT  = os.getenv("ATHENA_OUTPUT")

athena = boto3.client("athena", region_name="us-east-2")


def run_query(query):
    response = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={"Database": DATABASE},
        ResultConfiguration={"OutputLocation": OUTPUT}
    )

    query_execution_id = response["QueryExecutionId"]

    # WAIT for completion
    while True:
        result = athena.get_query_execution(QueryExecutionId=query_execution_id)
        state = result["QueryExecution"]["Status"]["State"]

        if state in ["SUCCEEDED", "FAILED", "CANCELLED"]:
            break

        time.sleep(1)

    if state != "SUCCEEDED":
        raise Exception(f"Athena query failed: {state}")

    return query_execution_id

def fetch_results(query_execution_id):
    result = athena.get_query_results(QueryExecutionId=query_execution_id)

    rows = result["ResultSet"]["Rows"]

    # safe header extraction
    headers = [col.get("VarCharValue", "") for col in rows[0]["Data"]]

    data = []

    for row in rows[1:]:
        values = row.get("Data", [])

        record = {}

        for i, col in enumerate(values):
            record[headers[i]] = col.get("VarCharValue")

        data.append(record)

    return data

def format_weather(data):
    latest = data[0]

    history = [
        {
            "timestamp": d.get("timestamp"),
            "temperature": float(d.get("temperature", 0))
        }
        for d in data[1:10]
    ]

    return {
        "latest": {
            "city": latest.get("city"),
            "temperature": float(latest.get("temperature", 0)),
            "humidity": float(latest.get("humidity", 0)),
            "weather": latest.get("weather"),
            "description": latest.get("description"),
            "timestamp": latest.get("timestamp")
        },
        "history": history
    }



def get_latest_weather():
    query = LATEST_WEATHER_QUERY

    qid = run_query(query)
    data = fetch_results(qid)

    return format_weather(data)