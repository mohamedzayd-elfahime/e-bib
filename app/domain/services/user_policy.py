from domain.entities.user import User


def can_user_interact(user: User) -> bool:
    return user.is_active
