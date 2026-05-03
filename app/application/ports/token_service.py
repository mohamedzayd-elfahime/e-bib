from abc import ABC, abstractmethod


class TokenService(ABC):
    @abstractmethod
    def generate(self, user_id: int) -> dict:
        pass
