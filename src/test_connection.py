import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

conn_str = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@localhost:5432/{os.getenv('POSTGRES_DB')}"
)

with psycopg.connect(conn_str) as conn:
    print(conn.execute("SELECT version()").fetchone())