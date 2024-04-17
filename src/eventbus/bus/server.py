import asyncio
from abc import abstractmethod
from typing import Any

from .. import Event, EventBus
from ..event import bye, bye_timeout, hello_connected, ping, pong
from . import Bridge


class Protocol:
    pass


class Transport(Protocol):
    @abstractmethod
    async def send_json(self, data: Any) -> None:
        pass

    @abstractmethod
    async def receive_json(self) -> Any:
        pass

    @abstractmethod
    async def close(self) -> Any:
        pass


class Server(EventBus):
    CLIENT_ADDR = 0

    def __init__(self, transport: Transport, bridge: Bridge, timeout: float = 1):
        self.transport = transport
        self.bridge = bridge
        self.timeout = timeout
        self.closed = False
        self.client_addr = f"@{Server.CLIENT_ADDR}"
        Server.CLIENT_ADDR += 1

    async def run(self):
        """Returns when the connection is closed."""
        self.bridge.subscribe(self)
        hello_connected["dst"] = self.client_addr
        hello_connected["param"] = {"timeout_interval": self.timeout}
        await self.bridge.post(hello_connected)
        await self.receiver_task()

    async def post(self, event: Event) -> None:
        # TODO: filter
        # TODO: group events in lists
        try:
            if not self.closed:
                await self.transport.send_json(event)
        except RuntimeError:
            self.closed = True

    async def process_event(self, event: Event) -> None:
        if event == ping:
            await self.post(pong)
        elif event == bye:
            self.closed = True
        else:
            await self.bridge.post(event)

    async def receiver_task(self):
        while not self.closed:
            try:
                event = await asyncio.wait_for(self.transport.receive_json(), timeout=self.timeout + 1)
                if isinstance(event, list):
                    for e in event:
                        await self.process_event(e)
                else:
                    await self.bridge.post(event)  # type: ignore
            except asyncio.TimeoutError:
                print("Server Timeout - disconnecting")
                await self.bridge.post(bye_timeout)
                self.closed = True
            except Exception as e:
                print("Server Error", e)
                self.closed = True
        try:
            await self.transport.close()
        except RuntimeError as e:
            print("RuntimeError closing transport", e)
        except Exception as e:
            print("Server Error closing transport", e)
