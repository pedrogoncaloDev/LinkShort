from datetime import datetime, timedelta
from typing import Optional

from db.connection import get_connection


class LinkRepository:
    def insert(self, codigo: str, url: str) -> None:
        creation_date = datetime.now()
        expiration_date = creation_date + timedelta(days=7)

        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO links (url_original, codigo_encurtado, data_criacao, data_expiracao)
                VALUES (%s, %s, %s, %s)
            """, (url, codigo, creation_date, expiration_date))
            conn.commit()
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()


    def exists(self, codigo: str) -> bool:
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT 1 FROM links WHERE codigo_encurtado = %s", (codigo,))
            return cur.fetchone() is not None
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()


    def get_original_url(self, codigo: str) -> Optional[str]:
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT url_original FROM links WHERE codigo_encurtado = %s", (codigo,))
            row = cur.fetchone()
            return row[0] if row else None
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
