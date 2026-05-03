import jwt
from datetime import datetime, timedelta, timezone
from app.config import settings
from app.application.ports.token_service import TokenService


class JwtTokenService(TokenService):
    def generate(self, user_id: int) -> dict:
        now = datetime.now(timezone.utc)

        access = jwt.encode(
            {
                "sub": str(user_id),
                "type": "access",
                "exp": now + timedelta(seconds=settings.JWT_ACCESS_TTL_SECONDS),
            },
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALG,
        )

        refresh = jwt.encode(
            {
                "sub": str(user_id),
                "type": "refresh",
                "exp": now + timedelta(seconds=settings.JWT_REFRESH_TTL_SECONDS),
            },
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALG,
        )

        return {
            "access": access,
            "refresh": refresh,
        }

    def decode(self, token: str) -> dict:
        return jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALG],
        )
