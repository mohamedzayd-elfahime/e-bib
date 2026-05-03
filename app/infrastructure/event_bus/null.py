# app/infrastructure/event_bus/null.py

class NullEventBus:
    def publish(self, event):
        pass

    def publish_all(self, events):
        pass
