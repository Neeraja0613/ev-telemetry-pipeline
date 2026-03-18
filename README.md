# EV Telemetry Data Pipeline (Hot/Cold Architecture)

## 🚀 Project Overview

This project implements a **scalable data pipeline** for processing Electric Vehicle (EV) charging telemetry data using a **Hot/Cold storage architecture**.

It simulates real-world IoT data engineering challenges where:
- **Recent data** must be accessed quickly (real-time monitoring)
- **Historical data** must be stored efficiently (analytics & reporting)

---

## 🧠 Architecture

```

Data Generator → Ingestion → Hot Storage (DB)
→ Cold Storage (Parquet)

```

- **Hot Storage** → Stores last 72 hours (fast queries)
- **Cold Storage** → Stores full 30-day dataset (analytics)
- **Compaction Layer** → Converts old data into summaries

---

## 🛠️ Tech Stack

- **Python** → Data generation, ingestion, queries
- **TimescaleDB (PostgreSQL)** → Hot storage
- **Parquet (PyArrow)** → Cold storage
- **DuckDB** → Analytical queries
- **Docker & Docker Compose** → Containerization

---

## 📂 Project Structure

```

ev-telemetry-pipeline/
│
├── scripts/
│   ├── generate_data.py
│   ├── ingest_data.py
│   └── compact_data.py
│
├── queries/
│   ├── rolling_avg.py
│   ├── anomaly_detection.py
│   └── peak_load.py
│
├── data/
│   ├── source/
│   ├── cold_storage/
│   └── cold_storage_summary/
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
├── README.md
└── SCALABILITY.md

````

---

## ⚙️ Setup Instructions

### 1️⃣ Clone / Navigate

```bash
cd ev-telemetry-pipeline
````

---

### 2️⃣ Setup Environment Variables

```bash
copy .env.example .env
```

---

### 3️⃣ Start Services

```bash
docker-compose up --build -d
```

Verify:

```bash
docker ps
```

---

## 📊 Step-by-Step Execution

### 1️⃣ Generate Data

```bash
docker exec -it data-tools python scripts/generate_data.py
```

✔ Creates:

```
data/source/telemetry.parquet
```

✔ Contains:

* 432,000 records
* 30 days of telemetry data
* Injected anomalies

---

### 2️⃣ Ingest Data (Dual Write)

```bash
docker exec -it data-tools python scripts/ingest_data.py
```

✔ Writes data to:

* **Cold Storage** → Full dataset (Parquet)
* **Hot Storage** → Last 72 hours (TimescaleDB)

---

### 3️⃣ Verify Hot Storage

```bash
docker exec -it hot-db psql -U postgres -d evdb
```

Run:

```sql
SELECT COUNT(*) FROM telemetry;
```

✔ Expected:

```
43200 rows
```

---

## 🔍 Queries

### 1️⃣ Rolling Average (Hot Storage)

```bash
docker exec -it data-tools python queries/rolling_avg.py st-001 "2023-10-29 10:00:00"
```

✔ Output:

```json
{
  "station_id": "st-001",
  "timestamp": "...",
  "avg_power_1h": 123.45
}
```

---

### 2️⃣ Anomaly Detection (Cold Storage)

```bash
docker exec -it data-tools python queries/anomaly_detection.py st-007
```

✔ Detects:

* Days with abnormal session counts

---

### 3️⃣ Peak Load Analysis

```bash
docker exec -it data-tools python queries/peak_load.py north south
```

✔ Output:

```json
{
  "north": {"peak_hour_utc": 18},
  "south": {"peak_hour_utc": 19}
}
```

---

## 📦 Data Storage Design

### 🔥 Hot Storage (TimescaleDB)

* Stores last **72 hours only**
* Optimized for:

  * Fast queries
  * Real-time monitoring

---

### ❄️ Cold Storage (Parquet)

Partitioned as:

```
data/cold_storage/
  station_region=north/
    day=YYYY-MM-DD/
```

✔ Benefits:

* Faster queries
* Efficient storage
* Columnar format

---

## 🔄 Data Compaction

Run:

```bash
docker exec -it data-tools python scripts/compact_data.py
```

✔ Converts:

* Minute-level data → Hourly summaries

✔ Output:

```
data/cold_storage_summary/
```

---

## 📈 Key Features

✔ Dual-write architecture
✔ Time-series data modeling
✔ Partitioned data lake
✔ Real-time + historical analytics
✔ Data lifecycle management
✔ Fully containerized setup

---

## ⚠️ Notes

* Ensure Docker is running before starting
* Remove `version` from docker-compose.yml (optional warning fix)
* All scripts run inside **data-tools container**

---

## 📚 Learning Outcomes

This project demonstrates:

* Data Engineering fundamentals
* Time-series data handling
* Hot vs Cold storage design
* Data partitioning strategies
* Query optimization
* Scalable pipeline thinking

---

## 🚀 Future Improvements

* Kafka for real-time ingestion
* Spark/Flink for distributed processing
* Cloud storage (S3/GCS)
* Distributed query engines (Trino)

---

## 📄 Documentation

* 📘 **SCALABILITY.md** → Scaling to 100x data
* 📘 README.md → Setup & usage guide

---

## 👩‍💻 Author
Neeraja Palla
