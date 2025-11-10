
# 📦 InfluxDB 3 Processing Engine & Python Plugins – Complete Guide

The **Processing Engine** in InfluxDB 3 Core allows you to **extend your database using custom Python code**. With Python plugins, you can trigger scripts on:

- **Data writes** – transform or enrich incoming data
- **Scheduled intervals** – perform regular analysis or system checks
- **HTTP requests** – build custom endpoints and integrations

---

## 🚀 What Is the Processing Engine?

At its core, the Processing Engine is an **embedded Python VM** inside InfluxDB 3. You configure *triggers* to run your Python code in response to:

| Trigger Type   | Description                                  |
|----------------|----------------------------------------------|
| `table:` / `all_tables` | Trigger on data writes (WAL flush)     |
| `every:` / `cron:`     | Run on a schedule                     |
| `request:`             | Run on HTTP endpoint access          |

You can also use an **in-memory cache** to retain state between executions – enabling stateful plugins.

---

## 🛠️ Setting Up the Processing Engine

Start the server with a plugin directory:
```bash
influxdb3 serve \
  --NODE_ID node1 \
  --object-store file \
  --plugin-dir /path/to/plugins
```

> Ensure plugins are available on all nodes in distributed setups. Use shared storage or sync methods to replicate plugin files.

---

## 📁 Add a Processing Engine Plugin

Plugins are **Python scripts** stored in the plugin directory with predefined function signatures. You can:

1. Use **example plugins** from the [InfluxDB3 Plugin Repo](https://github.com/influxdata/influxdb3_plugins)
2. Write **custom plugins** for custom use cases

---

### 🔄 Example: Cloning and Using a Sample Plugin

```bash
# Clone the plugin repo
git clone https://github.com/influxdata/influxdb3_plugins.git

# Copy an example to your plugin directory
cp influxdb3_plugins/examples/schedule/system_metrics/system_metrics.py /path/to/plugins/
```

Or reference the plugin directly from GitHub:
```bash
influxdb3 create trigger \
  --trigger-spec "every:1m" \
  --plugin-filename "gh:examples/schedule/system_metrics/system_metrics.py" \
  --database my_database \
  system_metrics
```

---

## ✨ Creating a Custom Plugin

### 🔧 Plugin Types

| Type         | Ideal For                            |
|--------------|---------------------------------------|
| Data Write   | Transform or enrich data on ingestion |
| Scheduled    | Reports, aggregations, health checks |
| HTTP Request | Custom APIs, Webhooks                |

---

### 1️⃣ Data Write Plugin

**Trigger Spec:** `table:sensor_data` or `all_tables`

```python
def process_writes(influxdb3_local, table_batches, args=None):
    for table_batch in table_batches:
        table_name = table_batch["table_name"]
        rows = table_batch["rows"]
        influxdb3_local.info(f"Processing {len(rows)} rows from {table_name}")

        line = LineBuilder("processed_data")
        line.tag("source_table", table_name)
        line.int64_field("row_count", len(rows))
        influxdb3_local.write(line)
```

---

### 2️⃣ Scheduled Plugin

**Trigger Spec:** `every:5m` or `cron:0 0 8 * * *`

```python
def process_scheduled_call(influxdb3_local, call_time, args=None):
    results = influxdb3_local.query("SELECT * FROM metrics WHERE time > now() - INTERVAL '1 hour'")
    if results:
        influxdb3_local.info(f"Found {len(results)} recent metrics")
    else:
        influxdb3_local.warn("No recent metrics found")
```

---

### 3️⃣ HTTP Request Plugin

**Trigger Spec:** `request:webhook`

```python
def process_request(influxdb3_local, query_parameters, request_headers, request_body, args=None):
    influxdb3_local.info(f"Request params: {query_parameters}")
    if request_body:
        import json
        data = json.loads(request_body)
        influxdb3_local.info(f"Data: {data}")
    return {"status": "success", "message": "Processed successfully"}
```

---

## 🧩 Creating Triggers

```bash
influxdb3 create trigger \
  --trigger-spec "table:sensor_data" \
  --plugin-filename "process_sensors.py" \
  --database my_database \
  sensor_processor
```

### 🎯 Trigger Examples

| Goal                    | Example Trigger CLI |
|-------------------------|---------------------|
| All table writes        | `--trigger-spec "all_tables"` |
| Cron schedule (daily 8am) | `--trigger-spec "cron:0 0 8 * * *"` |
| HTTP request            | `--trigger-spec "request:webhook"` |

---

## 🧠 Pass Arguments to Plugins

```bash
influxdb3 create trigger \
  --trigger-spec "every:1h" \
  --plugin-filename "threshold_check.py" \
  --trigger-arguments "threshold=90,notify_email=admin@example.com" \
  --database my_database \
  threshold_monitor
```

In plugin:
```python
def process_scheduled_call(influxdb3_local, call_time, args=None):
    threshold = float(args.get("threshold", 100))
    email = args.get("notify_email")
    influxdb3_local.info(f"Threshold: {threshold}, notify: {email}")
```

---

## ⚙️ Execution Controls

- Run async:
```bash
--run-asynchronous
```

- On error:
  - `--error-behavior log` *(default)*
  - `--error-behavior retry`
  - `--error-behavior disable`

---

## 📦 Managing Dependencies

```bash
# Install third-party Python packages
influxdb3 install package pandas
```

> These go into a virtual environment at `<plugin-dir>/venv`

---