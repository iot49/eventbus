import asyncio
from abc import abstractmethod
from typing import Any

from .. import Event, EventBus
from ..event import ping, pong

try:
    from typing import Protocol

    from fastapi import WebSocketDisconnect
except ImportError:
    WebSocketDisconnect = Exception
    Protocol = object

# each client gets a unique address
CLIENT_ADDR = 1


class Transport(Protocol):
    @abstractmethod
    async def send_json(self, data: Any) -> None:
        pass

    @abstractmethod
    async def receive_json(self) -> Any:
        pass


class Server(EventBus):
    def __init__(self, transport: Transport, bus: EventBus, timeout: float = 1):
        self.transport = transport
        self.bus = bus
        self.timeout = timeout

    async def run(self):
        """Returns when the connection is closed."""
        self.bus.subscribe(self)
        await self.receiver_task()

    async def post(self, event: Event) -> None:
        # TODO: filter
        # TODO: group events in lists
        print("Server post", event)
        await self.transport.send_json(event)  # type: ignore

    async def process_event(self, event: Event) -> None:
        if event == ping:
            await self.post(pong)
        else:
            await self.bus.post(event)

    async def receiver_task(self):
        global CLIENT_ADDR
        while True:
            try:
                event = await asyncio.wait_for(self.transport.receive_json(), timeout=self.timeout)
                event["src"] = f"@{CLIENT_ADDR}"
                CLIENT_ADDR += 1
                print("GOT", event)
            except asyncio.TimeoutError:
                print("Server Timeout - disconnecting")
                break
            except WebSocketDisconnect as e:
                print("Server Error", e)
                break
            if isinstance(event, list):
                for e in event:
                    await self.process_event(e)
            else:
                await self.bus.post(event)  # type: ignore
