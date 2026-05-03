from fastapi import (
    APIRouter,
    Request,
    Form,
    HTTPException,
    status,
    Depends,
)
from fastapi.responses import RedirectResponse, Response
from pydantic import EmailStr
from urllib.parse import urlencode

from app.application.use_cases.login_user import LoginUser, InvalidCredentials
from app.application.use_cases.login_with_google import LoginWithGoogle
from app.config import settings

from app.presentation.api.dependencies import (
    get_user_repository,
    get_password_hasher,
    get_token_service,
)

router = APIRouter()

@router.post("/login")
async def login_post(
    request: Request,
    email: EmailStr = Form(...),
    password: str = Form(min_length=8),
    user_repo = Depends(get_user_repository),
    password_hasher = Depends(get_password_hasher),
    token_service = Depends(get_token_service),
):
    login_user_uc = LoginUser(
        user_repo=user_repo,
        password_hasher=password_hasher,
        token_service=token_service,
    )

    try:
        tokens = login_user_uc.execute(email, password)
    except InvalidCredentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    response = RedirectResponse("/home", status_code=302)

    response.set_cookie(
        key="access_token",
        value=tokens["access"],
        httponly=True,
        secure=False,   # True in prod
        samesite="lax",
        max_age=settings.JWT_ACCESS_TTL_SECONDS,
    )

    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh"],
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=settings.JWT_REFRESH_TTL_SECONDS,
        path="/auth/refresh",
    )

    return response

@router.get("/auth/refresh")
def refresh(
    request: Request,
    token_service = Depends(get_token_service),
):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        return RedirectResponse("/login", status_code=302)

    try:
        payload = token_service.decode(refresh_token)

        if payload.get("type") != "refresh":
            raise ValueError()

        user_id = int(payload["sub"])

        # ROTATION
        tokens = token_service.generate(user_id)

        response = RedirectResponse("/home", status_code=303)

        response.set_cookie(
            "access_token",
            tokens["access"],
            httponly=True,
            samesite="lax",
            max_age=settings.JWT_ACCESS_TTL_SECONDS,
        )

        response.set_cookie(
            "refresh_token",
            tokens["refresh"],
            httponly=True,
            samesite="lax",
            max_age=settings.JWT_REFRESH_TTL_SECONDS,
            path="/auth/refresh",
        )

        return response

    except Exception:
        return RedirectResponse("/login", status_code=302)


@router.get("/auth/google")
def auth_google():
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent",
    }

    google_auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth?"
        + urlencode(params)
    )

    return RedirectResponse(google_auth_url)

@router.get("/auth/google/callback")
async def google_callback(
    request: Request,
    user_repo = Depends(get_user_repository),
    token_service = Depends(get_token_service),
):
    code = request.query_params.get("code")
    if not code:
        return RedirectResponse("/login", status_code=302)

    use_case = LoginWithGoogle(user_repo, token_service)

    try:
        tokens = await use_case.execute(code)
    except Exception:
        return RedirectResponse("/login", status_code=302)

    response = RedirectResponse("/home", status_code=302)

    response.set_cookie(
        "access_token",
        tokens["access"],
        httponly=True,
        samesite="lax",
        max_age=settings.JWT_ACCESS_TTL_SECONDS,
    )
    response.set_cookie(
        "refresh_token",
        tokens["refresh"],
        httponly=True,
        samesite="lax",
        max_age=settings.JWT_REFRESH_TTL_SECONDS,
        path="/auth/refresh",
    )

    return response
@router.get("/logout")
def logout(request: Request):
    # 1) Destroy session (CSRF only)
    request.session.clear()

    # 2) Redirect response
    response = RedirectResponse("/login", status_code=302)

    # 3) Delete access token cookie
    response.delete_cookie(
        key="access_token",
        samesite="lax",
    )

    # 4) Delete refresh token cookie (IMPORTANT: same path)
    response.delete_cookie(
        key="refresh_token",
        path="/auth/refresh",
        samesite="lax",
    )

    return response
