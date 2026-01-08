import psycopg2
from psycopg2 import sql
from .config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

def create_database():
    # postgres veritabanına bağlanma
    conn = psycopg2.connect(
        dbname="postgres", user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )
    conn.autocommit = True
    cur = conn.cursor()

    # Database varsa atla, yoksa oluştur
    cur.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"), [DB_NAME])
    exists = cur.fetchone()
    if not exists:
        print(f"{DB_NAME} oluşturuluyor...")
        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))
    else:
        print(f"{DB_NAME} zaten var.")

    cur.close()
    conn.close()

if __name__ == "__main__":
    create_database()
