from typing import List, Optional

from .event import Event


class EventBus:
    """Post and get events."""

    def __init__(self):
        self.subscribers: Optional[List["EventBus"]] = None

    async def post(self, event: Event) -> None:
        """Post one (or several) event(s) to this eventbus."""
        if self.subscribers is None:
            return
        for subscriber in self.subscribers:
            # TODO: detect loops
            await subscriber.post(event)

    def subscribe(self, bus: "EventBus") -> None:
        """Subscribe to this eventbus."""
        if self.subscribers is None:
            self.subscribers = [bus]
        else:
            self.subscribers.append(bus)

    def unsubscribe(self, bus: "EventBus") -> None:
        """Unsubscribe from this eventbus."""
        if self.subscribers is not None:
            self.subscribers.remove(bus)
