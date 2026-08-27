import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import ALLOWED_ORIGINS, BACKEND_HOST, BACKEND_PORT
from routes import router

app = FastAPI()

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
