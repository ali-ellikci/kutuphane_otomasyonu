from database.connection import get_connection

try:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT 1;")
    print("Veritabanı bağlantısı BAŞARILI")
    cur.close()
    conn.close()
except Exception as e:
    print("Veritabanı bağlantı hatası:")
    print(e)
