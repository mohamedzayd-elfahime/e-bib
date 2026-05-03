import pytest
from app.application.use_cases.login_user import LoginUser
from app.domain.entities.user import User
from app.application.use_cases.login_user import InvalidCredentials


class FakeUserRepository:
    def __init__(self, user=None):
        self.user = user

    def get_by_email(self, email: str):
        return self.user


class FakePasswordHasher:
    def verify(self, password: str, password_hash: str) -> bool:
        return password == "correct-password"


class FakeTokenService:
    def generate(self, user_id: int) -> dict:
        return {
            "access": "access-token",
            "refresh": "refresh-token",
        }


def test_login_success():
    user = User(
        id=1,
        email="a@test.com",
        password_hash="hash",
        is_active=True,
    )

    use_case = LoginUser(
        user_repo=FakeUserRepository(user),
        password_hasher=FakePasswordHasher(),
        token_service=FakeTokenService(),
    )

    result = use_case.execute("a@test.com", "correct-password")

    assert "access" in result
    assert "refresh" in result


def test_login_invalid_password():
    user = User(
        id=1,
        email="a@test.com",
        password_hash="hash",
        is_active=True,
    )

    use_case = LoginUser(
        user_repo=FakeUserRepository(user),
        password_hasher=FakePasswordHasher(),
        token_service=FakeTokenService(),
    )

    with pytest.raises(InvalidCredentials):
        use_case.execute("a@test.com", "wrong-password")


def test_login_inactive_user():
    user = User(
        id=1,
        email="a@test.com",
        password_hash="hash",
        is_active=False,
    )

    use_case = LoginUser(
        user_repo=FakeUserRepository(user),
        password_hasher=FakePasswordHasher(),
        token_service=FakeTokenService(),
    )

    with pytest.raises(InvalidCredentials):
        use_case.execute("a@test.com", "correct-password")
