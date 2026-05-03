# app/infrastructure/event_bus/in_memory.py
from collections import defaultdict
from typing import Callable, Iterable, Type


class InMemoryEventBus:
    """
    In-process synchronous event bus.
    """

    def __init__(self):
        self._handlers: dict[
            Type,
            list[Callable[[object], None]]
        ] = defaultdict(list)

    def subscribe(
        self,
        event_type: Type,
        handler: Callable[[object], None],
    ) -> None:
        self._handlers[event_type].append(handler)

    def publish_all(self, events: Iterable[object]) -> None:
        for event in events:
            for handler in self._handlers[type(event)]:
                handler(event)
