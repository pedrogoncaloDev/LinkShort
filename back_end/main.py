import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from config import ALLOWED_ORIGINS, BACKEND_HOST, BACKEND_PORT
from rate_limit import limiter
from routes import router

app = FastAPI(
    title="LinkShortener API",
    version="1.0.0",
    description=(
        "API do LinkShortener — encurtador de URLs.\n\n"
        "- `POST /shorten` cria (ou reaproveita) um link curto com expiração configurável.\n"
        "- `GET /{codigo}` redireciona para a URL original.\n"
        "- `GET /health` health check.\n\n"
        "Docs interativas: **/docs** (Swagger UI) e **/redoc** (ReDoc). "
        "Especificação: **/openapi.json**."
    ),
    contact={
        "name": "Pedro Gonçalo",
        "url": "https://github.com/pedrogoncaloDev/LinkShortener",
    },
    openapi_tags=[
        {"name": "Links", "description": "Criação e resolução de links curtos."},
        {"name": "Sistema", "description": "Health check e monitoramento."},
    ],
)

# Protege /shorten de abuso (bot martelando o endpoint pra inflar o banco).
# Ver @limiter.limit em routes.py.
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


if __name__ == "__main__":
    if os.getenv("DEBUG") == "1":
        import debugpy

        debug_host = os.getenv("DEBUG_HOST", "0.0.0.0")
        debug_port = int(os.getenv("DEBUG_PORT", "5678"))
        debugpy.listen((debug_host, debug_port))
        print(f"[debugpy] Aguardando conexão do debugger em {debug_host}:{debug_port}...")

        # Por padrão não bloqueia: o servidor sobe normalmente e o debugger
        # pode anexar a qualquer momento. Ligue DEBUG_WAIT_FOR_CLIENT=true
        # se precisar pausar breakpoints logo na inicialização.
        if os.getenv("DEBUG_WAIT_FOR_CLIENT", "false").lower() == "true":
            debugpy.wait_for_client()

    import uvicorn
    uvicorn.run("main:app", host=BACKEND_HOST, port=BACKEND_PORT)
