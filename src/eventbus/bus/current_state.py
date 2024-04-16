from eventbus import Event, EventBus
from eventbus.events import GetState, State


class CurrentState(EventBus):
    """Keep tack of state values."""

    def __init__(self, bus: EventBus):
        super().__init__()
        self.bus = bus
        self.state = {}
        bus.subscribe(self)

    async def process(self, event: Event) -> None:
        if isinstance(event, State):
            self.state[event.entity_id] = event
        elif isinstance(event, GetState):
            for s in self.state.values():
                s.dst = event.src
                print("CurrentState", s.to_dict())
                await self.bus.post(s)

    async def post(self, event: Event | list[Event]) -> None:
        if isinstance(event, Event):
            await self.process(event)
        else:
            for e in event:
                await self.process(e)
