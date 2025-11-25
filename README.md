# Law-N SQL API (`law-n-sql-api`)

Minimal **HTTP API** for Law-N:

- Accepts `network.routes` rows over HTTP
- Stores them in an in-memory table
- Exposes simple endpoints to:
  - list current rows
  - load/replace rows
  - run an **N-SQL query** over `network.routes` (if `law-n-sql-core` is available)

This is the first Law-N microservice: a small but real step toward **CLSI (Cloud Layer Signal Interface)**.

---

## ✨ Features

- `POST /tables/network-routes/load`  
  Load or replace `network.routes` with JSON rows

- `GET /tables/network-routes`  
  Read back all rows (with optional basic filters)

- `POST /query/nsql`  
  Run an N-SQL query like:

  ```sql
  SELECT device, tower_id, latency_ms, signal_quality
  FROM network.routes
  WHERE g_layer = '5G'
    AND signal_quality > 0.9;
