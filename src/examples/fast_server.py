import asyncio
import json
from contextlib import asynccontextmanager

import uvicorn
from eventbus import EventBus
from eventbus.bus import CurrentState, Server
from eventbus.event import get_state, state_action
from fastapi import FastAPI, WebSocket

from examples.counter import Counter

N = 100_000  # basically run forever


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(main())
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def get():
    return "Hello World"


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    server = Server(websocket, bus=broadcast_bus, timeout=1000)
    try:
        await server.run()
    finally:
        try:
            await websocket.close()
        except Exception as e:
            print("Error closing websocket", type(e), e)


async def reset_task():
    for i in range(N):
        await broadcast_bus.post(state_action(counter1.state, "reset", param=i))
        await asyncio.sleep(20)


broadcast_bus = EventBus()
CurrentState(broadcast_bus)
# Printer(broadcast_bus)
counter1 = Counter("counter1.up", broadcast_bus, interval=3, N=N)
counter2 = Counter("counter2.up", broadcast_bus, interval=5, N=N)

print("Action", json.dumps(state_action(counter1.state, "reset", param=777)))
print("GetState", json.dumps(get_state))


async def main():
    print("main!")
    await asyncio.gather(counter1._count_task(), counter2._count_task(), reset_task())


if __name__ == "__main__":
    uvicorn.run(app, port=8055, host="0.0.0.0")
