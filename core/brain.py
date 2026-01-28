from core.security_wall import on_system_event
from core.events import Event

class VisionBrain:

    def handle_input(self, text: str):
        # normal user input
        return f"আমি বুঝেছি: {text}"

    def system_event(self, event_type, source="system"):
        event = Event(event_type, source)
        on_system_event(event)
