LATEST_WEATHER_QUERY = """
SELECT *
FROM weather_clean
ORDER BY timestamp DESC
LIMIT 1;
"""

HISTORY_QUERY = """
SELECT timestamp, temperature
FROM weather_clean
ORDER BY timestamp DESC
LIMIT 20;
"""