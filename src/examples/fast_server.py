import asyncio
import json
from contextlib import asynccontextmanager

import uvicorn
from eventbus.bus import Bridge, CurrentState, Printer, Server
from eventbus.event import get_state, state_action
from examples.counter import Counter
from fastapi import FastAPI, WebSocket

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
    server = Server(websocket, bridge=bridge, timeout=3)  # type: ignore
    try:
        await server.run()
    finally:
        try:
            await websocket.close()
        except Exception as e:
            print("Error closing websocket", type(e), e)


async def reset_task():
    for i in range(N):
        await bridge.post(state_action(counter1.state, "reset", param=i))
        await asyncio.sleep(200)


bridge = Bridge()
CurrentState(bridge)
Printer(bridge)
counter1 = Counter("counter1.up", bridge, interval=1, N=N)
counter2 = Counter("counter2.up", bridge, interval=5, N=N)

print("Action", json.dumps(state_action(counter1.state, "reset", param=777)))
print("GetState", json.dumps(get_state))


async def main():
    await asyncio.gather(counter1._count_task(), counter2._count_task(), reset_task())


if __name__ == "__main__":
    uvicorn.run(app, port=8055, host="0.0.0.0")  # , log_level="trace")
