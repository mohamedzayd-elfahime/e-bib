class ToggleFavorite:
    def __init__(self, favorite_repo):
        self.favorite_repo = favorite_repo

    def execute(self, user_id: int, isbn: int) -> str:
        if self.favorite_repo.exists(user_id, isbn):
            self.favorite_repo.remove(user_id, isbn)
            return "removed"

        self.favorite_repo.add(user_id, isbn)
        return "added"
