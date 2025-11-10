
# 🔍 Querying Data in InfluxDB 3 Core

This guide walks you through how to query time-series data from **InfluxDB 3 Core** using the CLI, HTTP API, and the web-based **InfluxDB 3 Explorer**.

---

## 🚀 Overview

InfluxDB 3 Core supports querying with the following:

- ✅ **InfluxDB CLI (`influxdb3 query`)**
- ✅ **HTTP API (`/api/v3/query/sql`)**
- ✅ **InfluxDB 3 Explorer** (Graphical interface)

InfluxDB 3 uses **SQL-like syntax** for querying time-series data.

---

## ✍️ Example Data

Let’s assume you've written this sensor data into a bucket named `home_data`:

```
home,room=Living\ Room temp=21.1,hum=35.9,co=0i 1641024000
home,room=Kitchen     temp=21.0,hum=35.9,co=0i 1641024000
```

Your measurement is `home`, and the tags include `room`, while fields are `temp`, `hum`, and `co`.

---

## 🔧 Using the InfluxDB CLI

### Basic Query

```bash
influxdb3 query   --bucket home_data   --sql "SELECT * FROM home LIMIT 10;"   --token $INFLUXDB3_AUTH_TOKEN
```

You can filter using tags or time ranges:

```bash
--sql "SELECT * FROM home WHERE room = 'Kitchen' AND time > NOW() - INTERVAL '1 day';"
```

> ℹ️ `--bucket` defines the target dataset. Use `--output table` or `--output json` to change result format.

---

## 🌐 Query with HTTP API

Send SQL queries directly using the `/api/v3/query/sql` endpoint.

### Example using cURL

```bash
curl -X POST "http://localhost:8181/api/v3/query/sql?bucket=home_data"   -H "Authorization: Bearer $INFLUXDB3_AUTH_TOKEN"   -H "Content-Type: application/json"   -d '{ "sql": "SELECT * FROM home LIMIT 5;" }'
```

You can include filters and aggregations:

```json
{ "sql": "SELECT room, AVG(temp) FROM home GROUP BY room;" }
```

---

## 🧭 Query in InfluxDB 3 Explorer

**InfluxDB 3 Explorer** provides a GUI for running queries and managing results.

- Navigate to `http://<your-host>:8080/explorer`
- Choose a bucket and run SQL queries interactively
- View results in table or graph formats

---

## 📌 Tips & Best Practices

- Use `WHERE time > NOW() - INTERVAL 'X'` to limit by time
- Use `ORDER BY time DESC` for latest data first
- Aggregate using `AVG()`, `MAX()`, `MIN()`, `COUNT()`
- Filter tags using `WHERE tag = 'value'`

---

## ✅ Summary

| Method             | Tool/Endpoint               | Use Case                              |
|--------------------|-----------------------------|----------------------------------------|
| CLI                | `influxdb3 query`            | Quick local queries                    |
| HTTP API           | `/api/v3/query/sql`          | Programmatic access (apps, scripts)    |
| InfluxDB Explorer  | Web GUI                      | Visual query and data inspection       |

---

## 🔗 Next Steps

- Learn [how to write data](./write-to-influxdb3.md)
- Explore advanced SQL capabilities and window functions
- Connect InfluxDB with Grafana for time-series dashboards

> 📘 For full reference, visit the [InfluxDB 3 Core Documentation](https://docs.influxdata.com/influxdb3/core/).
