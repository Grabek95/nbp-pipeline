# NBP Exchange Rates Pipeline

Simple ETL pipeline that fetches daily average exchange rates (table A)
from the NBP API and loads them into PostgreSQL.

## Stack

- Python (requests, psycopg, python-dotenv)
- PostgreSQL 16 running in Docker
- Docker Compose

## How it works

1. **Extract** – fetch table A from the NBP API
2. **Transform** – parse JSON, keep rates as `Decimal` for precision
3. **Load** – insert into `exchange_rates`; `ON CONFLICT DO NOTHING`
   makes reruns safe (idempotent)

## Setup

```
cp .env.example .env        # fill in credentials
docker compose up -d
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
Get-Content sql\001_create_exchange_rates.sql | docker compose exec -T db psql -U <user> -d <db>
python src/load_rates.py
```

## Roadmap

- [ ] Historical backfill
- [ ] Logging and error handling
- [ ] Scheduling
- [ ] Raw data layer
