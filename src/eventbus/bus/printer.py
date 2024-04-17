import time

from .. import Event, EventBus
from . import Bridge


class Printer(EventBus):
    """Print events to the console."""

    def __init__(self, bridge: Bridge):
        super().__init__()
        self.start_time = None
        bridge.subscribe(self)

    async def post(self, event: Event) -> None:
        self.start_time = self.start_time or time.time_ns()
        print(f"PRINT {(time.time_ns()-self.start_time)/1e9:3.4f}", event)
