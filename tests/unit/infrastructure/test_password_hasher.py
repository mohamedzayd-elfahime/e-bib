from app.infrastructure.security.password_hasher import Argon2PasswordHasher


def test_password_hash_and_verify():
    hasher = Argon2PasswordHasher()

    password = "secret"
    hashed = hasher.hash_password(password)

    assert hashed != password
    assert hasher.verify(password, hashed) is True
    assert hasher.verify("wrong", hashed) is False

