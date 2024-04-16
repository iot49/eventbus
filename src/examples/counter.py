import asyncio

import eventbus
from eventbus import EventBus
from eventbus.bus import CurrentState, Printer
from eventbus.events import GetState, State, StateAction


class Counter(EventBus):
    """Resettable counter"""

    def __init__(self, entity_id: str, bus: EventBus, interval: float = 0.1):
        super().__init__()
        self.bus = bus
        self.interval = interval
        self.state: State = State(entity_id=entity_id, value=0)
        # Subscribe to the bus to receive StateAction events
        bus.subscribe(self)

    async def _count_task(self):
        state = self.state
        for _ in range(10):
            state.value += 1  # type: ignore
            # post the event to the bus
            await self.bus.post(state)
            await asyncio.sleep(self.interval)

    async def post(self, event):
        # Called by bus when an event is posted
        if isinstance(event, StateAction):
            if event.entity_id == self.state.entity_id and event.kind == "reset":
                # reset counter and post its new value
                self.state.value = 0
                await self.post(self.state)


eventbus.SRC_ADDR = "tree.branch"  # noqa: F811


async def main():
    async def reset_task():
        for i in range(3):
            await broadcast_bus.post(counter1.state.action("reset", param=i))
            await asyncio.sleep(0.35)

    async def current_state_task():
        for i in range(3):
            await broadcast_bus.post(GetState())
            await asyncio.sleep(0.7)

    broadcast_bus = EventBus()
    CurrentState(broadcast_bus)
    Printer(broadcast_bus)
    counter1 = Counter("counter1.up", broadcast_bus, interval=0.10)
    counter2 = Counter("counter2.up", broadcast_bus, interval=0.17)
    await asyncio.gather(counter1._count_task(), counter2._count_task(), reset_task(), current_state_task())
