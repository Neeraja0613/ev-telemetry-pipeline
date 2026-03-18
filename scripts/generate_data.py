import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

stations=[f"st-{i:03d}" for i in range(1,11)]
regions=["north","south","east","west"]

start=datetime(2023,10,1)
minutes=30*24*60

timestamps=[start+timedelta(minutes=i) for i in range(minutes)]

data=[]

for i,st in enumerate(stations):

    region=regions[i%4]

    session=0

    for ts in timestamps:

        voltage=np.random.normal(240,5)
        current=np.random.normal(15,2)

        # voltage spike anomaly
        if st=="st-003" and ts.date()==datetime(2023,10,10).date():
            voltage=320

        power=voltage*current

        # session drop anomaly (reduce distinct sessions)
        if st=="st-007" and ts.date() in [datetime(2023,10,15).date(), datetime(2023,10,16).date()]:
            session = 1
        else:
            session+=1
            session_id=session

        data.append([
            ts,st,region,voltage,current,power,session_id
        ])

df=pd.DataFrame(data,columns=[
"timestamp",
"station_id",
"station_region",
"voltage",
"current",
"power",
"session_id"
])

os.makedirs("data/source",exist_ok=True)

df.to_parquet("data/source/telemetry.parquet")

print("Dataset created:",len(df))