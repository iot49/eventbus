from .. import Event, EventBus, event_type
from ..event import state


class CurrentState(EventBus):
    """Keep tack of state values."""

    def __init__(self, bus: EventBus):
        super().__init__()
        self.bus = bus
        self.state = {}
        bus.subscribe(self)

    async def process(self, event: Event) -> None:
        et = event["et"]
        if et == event_type.STATE:
            # update current state
            self.state[event["entity_id"]] = (event["value"], event["timestamp"])
        elif et == event_type.GET_STATE:
            # sent all state values
            dst = event["src"]
            assert dst is not None
            for entity_id, (value, ts) in self.state.items():
                await self.bus.post(state(entity_id, value, dst=dst, timestamp=ts))

    async def post(self, event: Event | list[Event]) -> None:
        if isinstance(event, Event):
            await self.process(event)
        else:
            for e in event:
                await self.process(e)
