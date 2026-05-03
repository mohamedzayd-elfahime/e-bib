from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response, RedirectResponse, JSONResponse
from jwt import ExpiredSignatureError

from app.infrastructure.security.csrf_service import generate_csrf_token
from app.infrastructure.security.jwt_service import JwtTokenService
from app.config import settings


jwt_service = JwtTokenService()


# -------------------------------------------------
# Security headers
# -------------------------------------------------
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response


# -------------------------------------------------
# CSRF session init (SESSION USED ONLY FOR CSRF)
# -------------------------------------------------
class CSRFSessonInitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if "csrf_token" not in request.session:
            request.session["csrf_token"] = generate_csrf_token()
        return await call_next(request)


# -------------------------------------------------
# CSRF validation
# -------------------------------------------------
class CSRFMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method in ("POST", "PUT", "PATCH", "DELETE"):
            session_token = request.session.get("csrf_token")
            header_token = request.headers.get("X-CSRF-Token")

            if not session_token or session_token != header_token:
                return JSONResponse(
                    status_code=403,
                    content={"detail": "CSRF validation failed"},
                )

        return await call_next(request)


# -------------------------------------------------
# JWT Auth middleware (SINGLE SOURCE OF TRUTH)
# -------------------------------------------------
PUBLIC_PATHS = {
    "/login",
    "/auth/google",
    "/auth/google/callback",
    "/auth/refresh",
    "/logout",
    "/health",
}



class AuthRequiredMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # Static files
        if path.startswith("/static"):
            return await call_next(request)

        # Public routes
        if path in PUBLIC_PATHS:
            return await call_next(request)

        token = request.cookies.get("access_token")
        if not token:
            return RedirectResponse("/login", status_code=302)

        try:
            payload = jwt_service.decode(token)

            if payload.get("type") != "access":
                raise ValueError("Invalid token type")

            request.state.user_id = int(payload["sub"])

        except ExpiredSignatureError:
            return RedirectResponse("/auth/refresh", status_code=302)

        except Exception:
            return RedirectResponse("/login", status_code=302)

        return await call_next(request)
