class InvalidCredentials(Exception):
    pass


class LoginUser:
    def __init__(self, user_repo, password_hasher, token_service):
        self.user_repo = user_repo
        self.password_hasher = password_hasher
        self.token_service = token_service

    def execute(self, email: str, password: str):
        user = self.user_repo.get_by_email(email)

        if not user:
            raise InvalidCredentials()

        verified = self.password_hasher.verify(password, user.password_hash)

        if not user.can_login():
            raise InvalidCredentials()

        if not verified:
            raise InvalidCredentials()

        tokens = self.token_service.generate(user.id)
        return {
            "user_id": user.id,
            "access": tokens["access"],
            "refresh": tokens["refresh"],
        }


