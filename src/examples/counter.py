import asyncio

from eventbus import EventBus, event_type
from eventbus.bus import Bridge, CurrentState, Printer
from eventbus.event import get_state, state, state_action, state_update


class Counter(EventBus):
    """Resettable counter"""

    def __init__(self, eid: str, bridge: Bridge, interval: float = 0.1, N: int = 10):
        super().__init__()
        self.bridge = bridge
        self.interval = interval
        self.N = N
        self.state = state(eid=eid, value=0)
        # Subscribe to the bus to receive StateAction events
        bridge.subscribe(self)

    async def _count_task(self):
        state = self.state
        for _ in range(self.N):
            state_update(state, value=state["value"] + 1)
            # post the event to the bus
            await self.bridge.post(state)
            await asyncio.sleep(self.interval)

    async def post(self, event):
        # Called by bus when an event is posted
        if event["et"] == event_type.STATE_ACTION:
            device_id = ".".join(self.state["eid"].split(".")[:3])
            if event["device_id"] == device_id and event["action"] == "reset":
                # reset counter and post its new value
                state_update(self.state, value=0)
                await self.post(self.state)


async def main():
    async def reset_task():
        for i in range(3):
            await asyncio.sleep(0.35)
            await bridge.post(state_action(counter1.state, "reset", param=i))

    async def current_state_task():
        for i in range(3):
            await asyncio.sleep(0.7)
            await bridge.post(get_state)

    bridge = Bridge()
    CurrentState(bridge)
    Printer(bridge)
    counter1 = Counter("counter1.up", bridge, interval=0.10)
    counter2 = Counter("counter2.up", bridge, interval=0.17)
    await asyncio.gather(counter1._count_task(), counter2._count_task(), reset_task(), current_state_task())
