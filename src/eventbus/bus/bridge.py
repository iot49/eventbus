from .. import Event, EventBus


class Bridge:
    """Post and get events."""

    def __init__(self):
        self.subscribers = []

    async def post(self, event: Event) -> None:
        """Forward event to all subscribers."""
        for subscriber in self.subscribers:
            await subscriber.post(event)

    def subscribe(self, bus: EventBus) -> None:
        """Subscribe to this eventbus."""
        self.subscribers.append(bus)

    def unsubscribe(self, bus: EventBus) -> None:
        """Unsubscribe from this eventbus."""
        self.subscribers.remove(bus)
