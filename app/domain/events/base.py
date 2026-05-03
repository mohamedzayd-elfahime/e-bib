# domain/events/base.py
from datetime import datetime


class DomainEvent:
    def __init__(self):
        self.occurred_at = datetime.utcnow()
