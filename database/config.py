import os

# Centralized PostgreSQL configuration. Values can be overridden via environment variables.

DB_NAME = os.getenv("PGDATABASE", "kutuphanedb")
DB_USER = os.getenv("PGUSER", "admin")
DB_PASSWORD = os.getenv("PGPASSWORD", "14642812")
DB_HOST = os.getenv("PGHOST", "localhost")
DB_PORT = int(os.getenv("PGPORT", "5432"))

DB_DSN = {
    "host": DB_HOST,
    "database": DB_NAME,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "port": DB_PORT,
}
