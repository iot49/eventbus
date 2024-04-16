import time

from eventbus import Event, EventBus


class Printer(EventBus):
    """Print events to the console."""

    def __init__(self, subscribe: EventBus):
        super().__init__()
        self.start_time = time.time_ns()
        subscribe.subscribe(self)

    async def post(self, event: Event | list[Event]) -> None:
        if isinstance(event, Event):
            event = [event]
        for e in event:
            print(f"PRINT {(time.time_ns()-self.start_time)/1e9:3.4f}", e.to_dict())
