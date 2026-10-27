from datetime import date, timedelta

from load_rates import NBP_BASE, fetch_tables, save_rates, tables_to_rows

CHUNK_DAYS = 93


def date_chunks(start, end, size=CHUNK_DAYS):
    current = start
    while current <= end:
        chunk_end = min(current + timedelta(days=size - 1), end)
        yield current, chunk_end
        current = chunk_end + timedelta(days=1)


def main():
    start = date(2025, 1, 1)
    end = date.today()

    for chunk_start, chunk_end in date_chunks(start, end):
        url = f"{NBP_BASE}/{chunk_start}/{chunk_end}/?format=json"
        rows = tables_to_rows(fetch_tables(url))
        save_rates(rows)
        print(f"{chunk_start} – {chunk_end}: {len(rows)} kursów")


if __name__ == "__main__":
    main()