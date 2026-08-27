from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse

from config import BACKEND_URL, FRONTEND_URL
from rate_limit import limiter
from repositories.link_repository import LinkRepository
from schemas import LinkInput
from services.link_service import LinkService

router = APIRouter()
link_service = LinkService(LinkRepository())


@router.post("/shorten")
@limiter.limit("10/minute")
def shorten_link(request: Request, dados: LinkInput):
    if not dados.url:
        raise HTTPException(status_code=400, detail="URL não pode ser vazia")

    link = link_service.shorten(dados.url, dados.expires_in_minutes)
    return {
        "shortened_url": f"{BACKEND_URL}/{link.codigo}",
        "expires_at": link.expires_at.isoformat(),
    }


@router.get("/{codigo}")
def redirecionar(codigo: str):
    url = link_service.resolve(codigo)
    if url is None:
        # Redireciona para o front-end com o código na query string
        return RedirectResponse(f"{FRONTEND_URL}?codigo={codigo}")
    return RedirectResponse(url)
