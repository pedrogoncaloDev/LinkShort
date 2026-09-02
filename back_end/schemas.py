from pydantic import BaseModel, Field

MIN_EXPIRATION_MINUTES = 5
MAX_EXPIRATION_MINUTES = 60 * 24 * 30  # 1 mês
DEFAULT_EXPIRATION_MINUTES = 60 * 24 * 7  # 7 dias


class LinkInput(BaseModel):
    """Corpo da requisição de `POST /shorten`."""

    url: str = Field(
        description="URL de destino a ser encurtada. Não pode ser vazia.",
        examples=["https://exemplo.com/pagina/muito/longa?com=parametros"],
    )
    expires_in_minutes: int = Field(
        default=DEFAULT_EXPIRATION_MINUTES,
        ge=MIN_EXPIRATION_MINUTES,
        le=MAX_EXPIRATION_MINUTES,
        description=(
            "Tempo de vida do link, em minutos. Mínimo "
            f"{MIN_EXPIRATION_MINUTES}, máximo {MAX_EXPIRATION_MINUTES} (30 dias). "
            f"Padrão {DEFAULT_EXPIRATION_MINUTES} (7 dias)."
        ),
        examples=[10080],
    )


class ShortenResponse(BaseModel):
    """Resposta de `POST /shorten`."""

    shortened_url: str = Field(
        description="Link curto pronto para uso.",
        examples=["http://localhost:8000/a1b2c3"],
    )
    expires_at: str = Field(
        description="Data/hora de expiração do link, em ISO 8601.",
        examples=["2026-09-05T14:30:00"],
    )


class HealthResponse(BaseModel):
    """Resposta de `GET /health`."""

    status: str = Field(
        description="`ok` enquanto o serviço estiver de pé.",
        examples=["ok"],
    )


class ErrorResponse(BaseModel):
    """Formato padrão de erro do FastAPI."""

    detail: str = Field(examples=["URL não pode ser vazia"])
