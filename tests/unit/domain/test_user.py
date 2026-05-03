from app.domain.entities.user import User


def test_user_creation():
    user = User(
        id=1,
        email="a@test.com",
        password_hash="hash",
        is_active=True,
    )

    assert user.id == 1
    assert user.email == "a@test.com"
    assert user.is_active is True
