import asyncio

from eventbus import EventBus, event, event_type
from eventbus.bus import CurrentState, Printer
from eventbus.event import get_state, state, state_action, state_update


class Counter(EventBus):
    """Resettable counter"""

    def __init__(self, entity_id: str, bus: EventBus, interval: float = 0.1, N: int = 10):
        super().__init__()
        self.bus = bus
        self.interval = interval
        self.N = N
        self.state = state(entity_id=entity_id, value=0)
        # Subscribe to the bus to receive StateAction events
        bus.subscribe(self)

    async def _count_task(self):
        state = self.state
        for _ in range(self.N):
            state_update(state, value=state["value"] + 1)
            # post the event to the bus
            await self.bus.post(state)
            await asyncio.sleep(self.interval)

    async def post(self, event):
        # Called by bus when an event is posted
        if event["et"] == event_type.STATE_ACTION:
            device_id = ".".join(self.state["entity_id"].split(".")[:3])
            if event["device_id"] == device_id and event["action"] == "reset":
                # reset counter and post its new value
                state_update(self.state, value=0)
                await self.post(self.state)


event.SRC_ADDR = "tree.branch"  # noqa: F811


async def main():
    async def reset_task():
        for i in range(3):
            await asyncio.sleep(0.35)
            await broadcast_bus.post(state_action(counter1.state, "reset", param=i))

    async def current_state_task():
        for i in range(3):
            get_state["src"] = f"tree.branch{i}"
            await asyncio.sleep(0.7)
            await broadcast_bus.post(get_state)

    broadcast_bus = EventBus()
    CurrentState(broadcast_bus)
    Printer(broadcast_bus)
    counter1 = Counter("counter1.up", broadcast_bus, interval=0.10)
    counter2 = Counter("counter2.up", broadcast_bus, interval=0.17)
    await asyncio.gather(counter1._count_task(), counter2._count_task(), reset_task(), current_state_task())
