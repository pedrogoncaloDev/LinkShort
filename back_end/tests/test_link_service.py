from datetime import datetime, timedelta
from unittest.mock import MagicMock

from services.link_service import LinkService


def test_shorten_generates_code_and_inserts_when_no_active_link():
    repo = MagicMock()
    repo.find_active_by_url.return_value = None
    repo.exists.return_value = False
    expires_at = datetime.now() + timedelta(days=7)
    repo.insert.return_value = expires_at

    service = LinkService(repo)
    result = service.shorten("https://exemplo.com", 60 * 24 * 7)

    repo.insert.assert_called_once()
    codigo_passado = repo.insert.call_args[0][0]
    assert result.codigo == codigo_passado
    assert result.expires_at == expires_at


def test_shorten_reuses_existing_active_link_for_same_url():
    repo = MagicMock()
    expires_at = datetime.now() + timedelta(hours=1)
    repo.find_active_by_url.return_value = ("abc123", expires_at)

    service = LinkService(repo)
    result = service.shorten("https://exemplo.com", 60)

    repo.insert.assert_not_called()
    assert result.codigo == "abc123"
    assert result.expires_at == expires_at


def test_generate_unique_code_retries_on_collision():
    repo = MagicMock()
    # primeira tentativa colide com um código já existente, segunda não
    repo.exists.side_effect = [True, False]

    service = LinkService(repo)
    codigo = service._generate_unique_code()

    assert repo.exists.call_count == 2
    assert len(codigo) == 6
