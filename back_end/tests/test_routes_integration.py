from db.connection import get_connection


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_shorten_and_redirect_roundtrip(client):
    response = client.post("/shorten", json={"url": "https://exemplo.com/pagina"})
    assert response.status_code == 200
    body = response.json()
    assert "expires_at" in body
    codigo = body["shortened_url"].rsplit("/", 1)[-1]

    redirect = client.get(f"/{codigo}", follow_redirects=False)
    assert redirect.status_code == 307
    assert redirect.headers["location"] == "https://exemplo.com/pagina"


def test_shorten_rejects_empty_url(client):
    response = client.post("/shorten", json={"url": ""})
    assert response.status_code == 400


def test_shorten_rejects_out_of_range_expiration(client):
    response = client.post(
        "/shorten", json={"url": "https://exemplo.com", "expires_in_minutes": 1}
    )
    assert response.status_code == 422


def test_shorten_deduplicates_same_url(client):
    first = client.post("/shorten", json={"url": "https://exemplo.com/dedup"}).json()
    second = client.post("/shorten", json={"url": "https://exemplo.com/dedup"}).json()
    assert first["shortened_url"] == second["shortened_url"]


def test_expired_link_falls_back_to_frontend(client):
    created = client.post(
        "/shorten",
        json={"url": "https://exemplo.com/vai-expirar", "expires_in_minutes": 5},
    ).json()
    codigo = created["shortened_url"].rsplit("/", 1)[-1]

    # Força a expiração direto no banco em vez de esperar 5 minutos de verdade
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE links SET data_expiracao = NOW() - INTERVAL '1 minute' WHERE codigo_encurtado = %s",
        (codigo,),
    )
    conn.commit()
    cur.close()
    conn.close()

    redirect = client.get(f"/{codigo}", follow_redirects=False)
    assert redirect.status_code == 307
    assert "codigo=" in redirect.headers["location"]
    assert "exemplo.com" not in redirect.headers["location"]


def test_unknown_code_falls_back_to_frontend(client):
    redirect = client.get("/does-not-exist", follow_redirects=False)
    assert redirect.status_code == 307
    assert "codigo=does-not-exist" in redirect.headers["location"]


def test_rate_limit_blocks_after_ten_requests_per_minute(client):
    for i in range(10):
        response = client.post("/shorten", json={"url": f"https://exemplo.com/rl-{i}"})
        assert response.status_code == 200

    blocked = client.post("/shorten", json={"url": "https://exemplo.com/rl-onze"})
    assert blocked.status_code == 429
