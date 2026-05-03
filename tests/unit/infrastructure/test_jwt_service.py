import pytest
from jwt import ExpiredSignatureError
from app.infrastructure.security.jwt_service import JwtTokenService
from app.config import settings
import time


def test_generate_tokens():
    service = JwtTokenService(
    )

    tokens = service.generate(user_id=1)

    assert "access" in tokens
    assert "refresh" in tokens


def test_access_token_expired(monkeypatch):
    monkeypatch.setattr(settings, "JWT_ACCESS_TTL_SECONDS", 1)
    service = JwtTokenService(
    )

    token = service.generate(1)["access"]

    time.sleep(2)

    with pytest.raises(ExpiredSignatureError):
        service.decode(token)
