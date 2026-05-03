from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware

from app.config import settings
from app.presentation.api.routes.pages import router as pages_router
from app.presentation.api.routes.auth import router as auth_router
from app.presentation.api.routes.favorite import router as favorite_router
from app.presentation.api.routes.borrow import router as borrow_router
from app.presentation.api.routes.returnb import router as return_router
from app.presentation.api.routes.reservation import router as reservation_router
from app.presentation.api.routes.reviews import router as reviews_router
from app.presentation.middlewares import (
    SecurityHeadersMiddleware,
    CSRFSessonInitMiddleware,
    CSRFMiddleware,
    AuthRequiredMiddleware,
)
from app.presentation.ws.notifications import notifications_ws

middleware = [
    Middleware(
        SessionMiddleware,
        secret_key=settings.SESSION_SECRET_KEY,
        https_only=False,
        same_site="lax",
    ),
    Middleware(CSRFSessonInitMiddleware),
    Middleware(CSRFMiddleware),
    Middleware(AuthRequiredMiddleware),
    Middleware(SecurityHeadersMiddleware),
]

app = FastAPI(
    title="e-bib",
    middleware=middleware,
)

app.mount(
    "/static",
    StaticFiles(directory="app/presentation/static"),
    name="static",
)

app.include_router(pages_router)
app.include_router(auth_router)
app.include_router(favorite_router)
app.include_router(borrow_router)
app.include_router(return_router)
app.include_router(reservation_router)
app.include_router(reviews_router)
app.add_api_websocket_route("/ws/notifications", notifications_ws)


@app.get("/health")
async def health():
    return {"status": "ok"}
