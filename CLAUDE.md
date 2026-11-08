# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Small learning ETL pipeline: fetches NBP (Polish central bank) table A average exchange rates from `https://api.nbp.pl/api/exchangerates/tables/A` and loads them into PostgreSQL 16 running in Docker. Development is on Windows (PowerShell). Commit messages and script output are in Polish.

## Commands

```powershell
docker compose up -d                       # start Postgres (reads credentials from .env)
.venv\Scripts\activate
pip install -r requirements.txt            # versions are pinned; keep it that way
Get-Content sql\001_create_exchange_rates.sql | docker compose exec -T db psql -U <user> -d <db>   # apply schema
python src/test_connection.py              # sanity check DB connectivity
python src/load_rates.py                   # load the latest table A
python src/backfill.py                     # load history from 2025-01-01 to today
```

There is no test suite, linter, or migration tool. Schema changes go in new numbered files under `sql/` (`002_...sql`) and are applied manually via `psql` as above.

## Architecture

- `src/load_rates.py` is the core module; other scripts import from it. It exposes `fetch_tables(url)` (returns `[]` on HTTP 404, which NBP returns for dates/ranges with no published table, e.g. weekends/holidays), `tables_to_rows(tables)` and `save_rates(rows)`.
- JSON is parsed with `parse_float=Decimal` so rates stay exact all the way into the `NUMERIC(12,6)` column — don't introduce floats.
- Loads are idempotent: the insert uses `ON CONFLICT (rate_date, currency_code) DO NOTHING` against the table's primary key, so re-running any script is safe (but it will not update already-stored rates).
- `src/backfill.py` splits the date range into 93-day chunks because the NBP API rejects date ranges longer than 93 days. Start date is hardcoded in `main()`.
- Scripts import siblings by bare module name (`from load_rates import ...`), so run them as `python src/<script>.py` (which puts `src/` on `sys.path`), not as `python -m src.<script>`.
- DB connection string is built from `POSTGRES_USER` / `POSTGRES_PASSWORD` / `POSTGRES_DB` in `.env` (loaded via python-dotenv; the same `.env` feeds the Docker container) and always points to `localhost:5432`.

## Roadmap (from README)

Historical backfill is done (`src/backfill.py`). Logging and error handling, scheduling, and a raw data layer are planned next.

## Zasady współpracy

- Uczę się Pythona: zanim zmienisz kod, wyjaśnij co i dlaczego
- Proponuj zmiany małymi krokami, nie przepisuj całych plików
- Odpowiadaj po polsku
- Nie commituj bez mojej zgody
