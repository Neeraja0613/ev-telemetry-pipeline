import duckdb
import pandas as pd
import os

con=duckdb.connect()

df=con.execute("""
SELECT 
    station_region,
    DATE(timestamp) AS day,
    EXTRACT(hour FROM timestamp) AS hour,
    AVG(power) AS avg_power,
    MAX(voltage) AS max_voltage,
    COUNT(DISTINCT session_id) AS session_count
FROM 'data/cold_storage/**/*.parquet'
GROUP BY 
    station_region,
    DATE(timestamp),
    EXTRACT(hour FROM timestamp)
""").df()

os.makedirs("data/cold_storage_summary",exist_ok=True)

df.to_parquet("data/cold_storage_summary/summary.parquet")

print("Compaction completed")