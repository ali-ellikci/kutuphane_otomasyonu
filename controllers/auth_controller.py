from typing import Tuple

import psycopg2

from database.connection import get_connection


class AuthController:
	def login(self, username: str, password: str) -> Tuple[bool, str]:
		if not username or not password:
			return False, "Kullanıcı adı ve şifre gerekli"

		try:
			with get_connection() as conn:
				with conn.cursor() as cur:
					cur.execute(
						"SELECT id, username, role FROM KULLANICI WHERE username=%s AND password=%s",
						(username, password),
					)
					row = cur.fetchone()
					if row:
						return True, f"Hoş geldiniz, {row[1]}"
					return False, "Geçersiz kullanıcı adı veya şifre"
		except psycopg2.Error as e:
			return False, f"Veritabanı hatası: {e.pgerror or str(e)}"
		except Exception as e:
			return False, f"Beklenmeyen hata: {str(e)}"
