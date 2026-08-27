from pydantic import BaseModel, Field

MIN_EXPIRATION_MINUTES = 5
MAX_EXPIRATION_MINUTES = 60 * 24 * 30  # 1 mês
DEFAULT_EXPIRATION_MINUTES = 60 * 24 * 7  # 7 dias


class LinkInput(BaseModel):
    url: str
    expires_in_minutes: int = Field(
        default=DEFAULT_EXPIRATION_MINUTES,
        ge=MIN_EXPIRATION_MINUTES,
        le=MAX_EXPIRATION_MINUTES,
    )
