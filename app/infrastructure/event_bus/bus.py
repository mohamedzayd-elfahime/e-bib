# app/infrastructure/event_bus/bus.py
from app.infrastructure.event_bus.in_memory import InMemoryEventBus
from app.infrastructure.handlers.borrowing_returned_handler import on_borrowing_returned
from app.domain.events.borrowing_events import BorrowingReturned

event_bus = InMemoryEventBus()

event_bus.subscribe(BorrowingReturned, on_borrowing_returned)
