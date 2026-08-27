import uuid
from datetime import datetime
from typing import NamedTuple, Optional

from repositories.link_repository import LinkRepository


class ShortenedLink(NamedTuple):
    codigo: str
    expires_at: datetime


class LinkService:
    def __init__(self, repository: LinkRepository):
        self._repository = repository


    def shorten(self, url: str, expires_in_minutes: int) -> ShortenedLink:
        existing = self._repository.find_active_by_url(url)
        if existing is not None:
            codigo, expires_at = existing
            return ShortenedLink(codigo, expires_at)

        codigo = self._generate_unique_code()
        expires_at = self._repository.insert(codigo, url, expires_in_minutes)
        return ShortenedLink(codigo, expires_at)


    def resolve(self, codigo: str) -> Optional[str]:
        return self._repository.get_original_url(codigo)


    def _generate_unique_code(self) -> str:
        codigo = str(uuid.uuid4())[:6]
        while self._repository.exists(codigo):
            codigo = str(uuid.uuid4())[:6]
        return codigo
