import pytest
from fastapi.testclient import TestClient

from config import DB_NAME
from db.connection import get_connection
from main import app
from rate_limit import limiter

if not DB_NAME.endswith("_test"):
    raise RuntimeError(
        f"DB_NAME='{DB_NAME}' não parece ser um banco de teste (não termina em "
        "'_test'). Os testes de integração apagam o conteúdo da tabela 'links' "
        "a cada execução — rode contra um banco dedicado, ex.: "
        "DB_NAME=link_shortener_test, pra não perder dados reais."
    )


@pytest.fixture(autouse=True)
def _isolate_between_tests():
    """Zera o rate limiter e esvazia a tabela 'links' antes de cada teste,
    pra um teste não vazar estado pro próximo."""
    limiter.reset()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM links")
    conn.commit()
    cur.close()
    conn.close()

    yield


@pytest.fixture
def client():
    return TestClient(app)
