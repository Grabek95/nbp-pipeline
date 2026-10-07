import os
from decimal import Decimal

import psycopg
import requests
from dotenv import load_dotenv

load_dotenv()

NBP_URL = "https://api.nbp.pl/api/exchangerates/tables/A/?format=json"

INSERT_SQL = """
    INSERT INTO exchange_rates (rate_date, currency_code, currency_name, mid_rate, table_no)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (rate_date, currency_code) DO NOTHING
"""


def fetch_rates():
    response = requests.get(NBP_URL, timeout=10)
    response.raise_for_status()
    table = response.json(parse_float=Decimal)[0]
    return [
        (table["effectiveDate"], r["code"], r["currency"], r["mid"], table["no"])
        for r in table["rates"]
    ]


def save_rates(rows):
    conn_str = (
        f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
        f"@localhost:5432/{os.getenv('POSTGRES_DB')}"
    )
    with psycopg.connect(conn_str) as conn:
        with conn.cursor() as cur:
            cur.executemany(INSERT_SQL, rows)


def main():
    rows = fetch_rates()
    save_rates(rows)
    print(f"Pobrano {len(rows)} kursów z dnia {rows[0][0]}")


if __name__ == "__main__":
    main()