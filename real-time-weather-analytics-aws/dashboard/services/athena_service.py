import boto3
import pandas as pd
import time
import os
from dotenv import load_dotenv

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

    query_id = response["QueryExecutionId"]

    # Wait for completion
    while True:
        result = athena.get_query_execution(QueryExecutionId=query_id)
        state = result["QueryExecution"]["Status"]["State"]

        if state in ["SUCCEEDED", "FAILED", "CANCELLED"]:
            break
        time.sleep(1)

    if state != "SUCCEEDED":
        raise Exception("Athena query failed")

    results = athena.get_query_results(QueryExecutionId=query_id)

    rows = results["ResultSet"]["Rows"]

    # Convert to readable format
    data = [row["Data"] for row in rows[1:]]

    return data


def get_latest_weather():
    query = f"""
    SELECT *
    FROM {TABLE}
    ORDER BY timestamp DESC
    LIMIT 20;
    """

    return run_query(query)