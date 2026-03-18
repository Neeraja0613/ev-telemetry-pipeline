import duckdb
import sys
import json

r1=sys.argv[1]
r2=sys.argv[2]

con=duckdb.connect()

def peak(region):

    df=con.execute(f"""
    SELECT EXTRACT(hour from timestamp) as hr,
    avg(power) as p
    FROM 'data/cold_storage/**/*.parquet'
    WHERE station_region='{region}'
    GROUP BY hr
    ORDER BY p desc
    LIMIT 1
    """).fetchone()

    return int(df[0])

output={
r1:{"peak_hour_utc":peak(r1)},
r2:{"peak_hour_utc":peak(r2)}
}

print(json.dumps(output))