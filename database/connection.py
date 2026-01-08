import psycopg2
from .config import DB_DSN


def get_connection():
	return psycopg2.connect(**DB_DSN)
