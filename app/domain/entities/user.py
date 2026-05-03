class User:
    def __init__(self, id: int, email: str, password_hash: str, is_active: bool):
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.is_active = is_active

    def can_login(self) -> bool:
        return self.is_active
