import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from sqlalchemy import create_engine
import os
import datetime
import psycopg2

df=pd.read_parquet("data/source/telemetry.parquet")

df["day"]=df["timestamp"].dt.date

table=pa.Table.from_pandas(df)

pq.write_to_dataset(
table,
root_path="data/cold_storage",
partition_cols=["station_region","day"]
)

print("Cold storage written")

latest=df["timestamp"].max()

cutoff=latest-pd.Timedelta(hours=72)

hot=df[df["timestamp"]>cutoff]

engine=create_engine("postgresql://postgres:postgres@hot-db:5432/evdb")

hot.to_sql("telemetry",engine,if_exists="replace",index=False)

print("Hot storage written",len(hot))