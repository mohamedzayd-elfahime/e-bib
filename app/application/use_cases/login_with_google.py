import httpx
from app.config import settings
from app.application.ports.UserRepository import UserRepository
from app.application.ports.token_service import TokenService


class LoginWithGoogle:
    def __init__(self, user_repo, token_service):
        self.user_repo = user_repo
        self.token_service = token_service

    async def execute(self, code: str) -> dict:
        """
        1. Exchange authorization code for Google access token
        2. Fetch user info from Google
        3. Get or create local user
        4. Generate JWT access + refresh tokens
        """

        # -------------------------------------------------
        # 1) Exchange code -> Google access token
        # -------------------------------------------------
        token_url = "https://oauth2.googleapis.com/token"

        token_payload = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }

        async with httpx.AsyncClient() as client:
            token_resp = await client.post(
                token_url,
                data=token_payload,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )

        if token_resp.status_code != 200:
            raise Exception("Google token exchange failed")

        token_data = token_resp.json()
        google_access_token = token_data.get("access_token")

        if not google_access_token:
            raise Exception("No access_token returned by Google")


        # -------------------------------------------------
        # 2) Fetch Google user info
        # -------------------------------------------------
        userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"

        async with httpx.AsyncClient() as client:
            userinfo_resp = await client.get(
                userinfo_url,
                headers={
                    "Authorization": f"Bearer {google_access_token}"
                },
            )

        if userinfo_resp.status_code != 200:
            raise Exception("Failed to fetch Google user info")

        userinfo = userinfo_resp.json()
        email = userinfo.get("email")

        if not email:
            raise Exception("Google account has no email")

        # -------------------------------------------------
        # 3) Get or create local user
        # -------------------------------------------------
        user = self.user_repo.get_by_email(email)

        if not user:
            # Minimal user creation (Google-auth users)
            user = self.user_repo.create_google_user(
                email=email,
                is_active=True,
            )

        if not user.is_active:
            raise Exception("User is inactive")

        # -------------------------------------------------
        # 4) Generate JWT tokens
        # -------------------------------------------------
        tokens = self.token_service.generate(user.id)

        return tokens