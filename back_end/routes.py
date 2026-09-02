from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import RedirectResponse

from config import BACKEND_URL, FRONTEND_URL
from rate_limit import limiter
from repositories.link_repository import LinkRepository
from schemas import ErrorResponse, HealthResponse, LinkInput, ShortenResponse
from services.link_service import LinkService

router = APIRouter()
link_service = LinkService(LinkRepository())


@router.post(
    "/shorten",
    response_model=ShortenResponse,
    tags=["Links"],
    summary="Encurtar uma URL",
    description=(
        "Gera um código curto de 6 caracteres para a URL informada e devolve o "
        "link pronto.\n\n"
        "Se a **mesma URL** já tiver um link curto ainda válido, o código "
        "existente é reaproveitado em vez de criar outro — evita inflar o banco "
        "com duplicatas.\n\n"
        "**Rate limit:** 10 requisições por minuto por IP."
    ),
    responses={
        400: {"model": ErrorResponse, "description": "URL vazia"},
        422: {
            "model": ErrorResponse,
            "description": "`expires_in_minutes` fora do intervalo permitido",
        },
        429: {
            "model": ErrorResponse,
            "description": "Limite de 10 requisições por minuto excedido",
        },
    },
)
@limiter.limit("10/minute")
def shorten_link(request: Request, dados: LinkInput):
    if not dados.url:
        raise HTTPException(status_code=400, detail="URL não pode ser vazia")

    link = link_service.shorten(dados.url, dados.expires_in_minutes)
    return {
        "shortened_url": f"{BACKEND_URL}/{link.codigo}",
        "expires_at": link.expires_at.isoformat(),
    }


@router.get(
    "/health",
    response_model=HealthResponse,
    tags=["Sistema"],
    summary="Health check",
    description="Verifica se o serviço está no ar. Usado pelo Render e por monitoramento.",
)
def health_check():
    return {"status": "ok"}


# Precisa vir DEPOIS de /health: rotas são casadas na ordem de registro, e
# "/{codigo}" combinaria com "/health" (codigo="health") se viesse antes.
@router.get(
    "/{codigo}",
    tags=["Links"],
    summary="Redirecionar para a URL original",
    description=(
        "Redireciona (HTTP 307) para a URL original associada ao código.\n\n"
        "Se o código **não existir** ou estiver **expirado**, redireciona para "
        "`FRONTEND_URL?codigo={codigo}` em vez de retornar erro — assim o "
        "front-end mostra uma mensagem amigável."
    ),
    response_class=RedirectResponse,
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    responses={
        307: {
            "description": (
                "Redirect para a URL original, ou para o front-end quando o "
                "código é inválido/expirado"
            )
        }
    },
)
def redirecionar(codigo: str):
    url = link_service.resolve(codigo)
    if url is None:
        # Redireciona para o front-end com o código na query string
        return RedirectResponse(f"{FRONTEND_URL}?codigo={codigo}")
    return RedirectResponse(url)
