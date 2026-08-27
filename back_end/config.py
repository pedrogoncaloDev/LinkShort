import os

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://127.0.0.1:5500/front_end/index.html")
# URL pública pela qual o navegador do usuário alcança o back-end (usada para
# montar o link encurtado retornado por /shorten)
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

BACKEND_HOST = os.getenv("BACKEND_HOST", "127.0.0.1")
# PORT é a variável usada por padrão em plataformas como Render/Railway/Heroku
BACKEND_PORT = int(os.getenv("PORT", os.getenv("BACKEND_PORT", "8000")))

ALLOWED_ORIGINS = [origin.strip() for origin in os.getenv("ALLOWED_ORIGINS", "*").split(",")]

# Defaults pensados para rodar fora do Docker (debug local): host = localhost
# e port = a porta publicada pelo docker-compose (ver DB_PORT no .env). Dentro
# do container, o docker-compose sobrescreve DB_HOST=db e DB_PORT=5432.
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5434"))
DB_NAME = os.getenv("DB_NAME", "link_shortener")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
