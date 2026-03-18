import sys
import json
from sqlalchemy import create_engine
import pandas as pd

station=sys.argv[1]
ts=sys.argv[2]

engine=create_engine("postgresql://postgres:postgres@hot-db:5432/evdb")

query=f"""
SELECT avg(power)
FROM telemetry
WHERE station_id='{station}'
AND timestamp BETWEEN '{ts}'::timestamp - interval '1 hour'
AND '{ts}'
"""

result=pd.read_sql(query,engine)

output={
"station_id":station,
"timestamp":ts,
"avg_power_1h":float(result.iloc[0,0])
}

print(json.dumps(output))