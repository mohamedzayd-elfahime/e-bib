from abc import ABC, abstractmethod
from datetime import datetime


class Clock(ABC):
    """
    Port responsible for providing the current time.
    """

    @abstractmethod
    def now(self) -> datetime:
        """
        Return the current UTC time.
        """
        raise NotImplementedError
