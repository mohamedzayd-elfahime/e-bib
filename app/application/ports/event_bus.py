from abc import ABC, abstractmethod
from typing import Iterable


class EventBus(ABC):
    """
    Port responsible for publishing domain events
    after a successful transaction.
    """

    @abstractmethod
    def publish_all(self, events: Iterable[object]) -> None:
        """
        Publish one or more domain events to subscribed handlers.

        - Called by the application layer
        - After transaction commit
        - No business logic here
        """
        raise NotImplementedError
