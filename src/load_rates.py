import os
from decimal import Decimal

import psycopg
import requests
from dotenv import load_dotenv

load_dotenv()

NBP_BASE = "https://api.nbp.pl/api/exchangerates/tables/A"

INSERT_SQL = """
    INSERT INTO exchange_rates (rate_date, currency_code, currency_name, mid_rate, table_no)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (rate_date, currency_code) DO NOTHING
"""


def fetch_tables(url):
    response = requests.get(url, timeout=10)
    if response.status_code == 404:
        return []
    response.raise_for_status()
    return response.json(parse_float=Decimal)


def tables_to_rows(tables):
    return [
        (t["effectiveDate"], r["code"], r["currency"], r["mid"], t["no"])
        for t in tables
        for r in t["rates"]
    ]


def save_rates(rows):
    if not rows:
        return
    conn_str = (
        f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
        f"@localhost:5432/{os.getenv('POSTGRES_DB')}"
    )
    with psycopg.connect(conn_str) as conn:
        with conn.cursor() as cur:
            cur.executemany(INSERT_SQL, rows)


def main():
    tables = fetch_tables(f"{NBP_BASE}/?format=json")
    rows = tables_to_rows(tables)
    save_rates(rows)
    print(f"Pobrano {len(rows)} kursów")


if __name__ == "__main__":
    main()