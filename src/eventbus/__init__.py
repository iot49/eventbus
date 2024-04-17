from abc import abstractmethod

"""
EventBus - a simple interface for routing events (dicts).

Typically you would create a Bridge and one or more clients
post and receive events. The Bridge and clients (if interested
in receiving events) all implement the EventBus interface.

To send an event, post it on the Bridge. Clients are notified
of new events by the Bridge calling their post method.

Beware of recursion: events posted on the Bridge will be received
by all clients, including the one that posted the event.
"""

Event = dict


class EventBus:
    """Post and get events."""

    @abstractmethod
    async def post(self, event: Event) -> None:
        """Post one (or several) event(s) to this eventbus."""
        pass
