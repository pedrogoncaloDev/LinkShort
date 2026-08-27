from datetime import datetime, timedelta
from typing import Optional, Tuple

from db.connection import get_connection


class LinkRepository:
    def find_active_by_url(self, url: str) -> Optional[Tuple[str, datetime]]:
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            # Reaproveita um link já existente pra mesma URL, se ainda
            # válido — evita que repetir o mesmo encurtamento infle o banco.
            # ORDER BY data_expiracao DESC pega o que vai durar mais, caso
            # existam vários (não deveria com uso normal, mas não é único
            # no schema).
            cur.execute(
                """
                SELECT codigo_encurtado, data_expiracao FROM links
                WHERE url_original = %s AND data_expiracao > NOW()
                ORDER BY data_expiracao DESC
                LIMIT 1
                """,
                (url,),
            )
            row = cur.fetchone()
            return (row[0], row[1]) if row else None
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()


    def insert(self, codigo: str, url: str, expires_in_minutes: int) -> datetime:
        creation_date = datetime.now()
        expiration_date = creation_date + timedelta(minutes=expires_in_minutes)

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
            return expiration_date
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
            # NOW() vem do Postgres (não do relógio da app) pra não haver
            # divergência de fuso/clock entre app e banco
            cur.execute(
                "SELECT url_original FROM links WHERE codigo_encurtado = %s AND data_expiracao > NOW()",
                (codigo,),
            )
            row = cur.fetchone()
            return row[0] if row else None
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
