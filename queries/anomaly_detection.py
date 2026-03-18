import duckdb
import sys
import json

station=sys.argv[1]

con=duckdb.connect()

df=con.execute(f"""
SELECT 
    DATE(timestamp) AS day,
    COUNT(DISTINCT session_id) AS sessions
FROM 'data/cold_storage/**/*.parquet'
WHERE station_id='{station}'
GROUP BY DATE(timestamp)
ORDER BY day
""").df()

mean=df.sessions.mean()
std=df.sessions.std()

df["z"] = (df.sessions - mean) / std

# detect BOTH high and low anomalies
anomalies = df[(df.z > 2) | (df.z < -2)]["day"].astype(str).tolist()

print(json.dumps({"station_id":station,"anomalous_dates":anomalies}))