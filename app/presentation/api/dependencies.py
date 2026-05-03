from app.infrastructure.repos.user_repository_mysql import MySQLUserRepository
from app.infrastructure.security.jwt_service import JwtTokenService
from app.infrastructure.security.password_hasher import Argon2PasswordHasher
from app.infrastructure.security.jwt_service import JwtTokenService
from fastapi import  Request, HTTPException, status
from app.infrastructure.repos.favorite_repository_mysql import MySQLFavoriteRepository
from fastapi import WebSocket, WebSocketException, status

def get_user_repository():
    return MySQLUserRepository()

def get_token_service():
    return JwtTokenService()

def get_password_hasher():
    return Argon2PasswordHasher()


def get_current_user_id(request: Request) -> int:

    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    jwt_service = JwtTokenService()
    payload = jwt_service.decode(token)
    return int(payload["sub"])

def get_favorite_repository():
    return MySQLFavoriteRepository()




async def get_current_user_id_ws(websocket: WebSocket) -> int:
    """
    Authentifie un utilisateur sur WebSocket via JWT.
    Le token est passé en query param: ?token=...
    """

    token = websocket.query_params.get("token")
    if not token:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)

    try:
        jwt_service = JwtTokenService()
        payload = jwt_service.decode(token)

        user_id = payload.get("sub")
        if user_id is None:
            raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)

        return int(user_id)

    except Exception:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)