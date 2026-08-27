import pytest
from pydantic import ValidationError

from schemas import DEFAULT_EXPIRATION_MINUTES, MAX_EXPIRATION_MINUTES, MIN_EXPIRATION_MINUTES, LinkInput


def test_default_expiration_is_seven_days():
    link = LinkInput(url="https://exemplo.com")
    assert link.expires_in_minutes == DEFAULT_EXPIRATION_MINUTES


@pytest.mark.parametrize("minutes", [MIN_EXPIRATION_MINUTES, MAX_EXPIRATION_MINUTES, 1440])
def test_accepts_values_within_bounds(minutes):
    link = LinkInput(url="https://exemplo.com", expires_in_minutes=minutes)
    assert link.expires_in_minutes == minutes


@pytest.mark.parametrize(
    "minutes", [0, MIN_EXPIRATION_MINUTES - 1, MAX_EXPIRATION_MINUTES + 1, -10]
)
def test_rejects_values_outside_bounds(minutes):
    with pytest.raises(ValidationError):
        LinkInput(url="https://exemplo.com", expires_in_minutes=minutes)
