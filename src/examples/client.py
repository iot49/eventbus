import asyncio

import aiohttp
from eventbus.eid import getSrcAddr, setSrcAddr
from eventbus.event import get_state, hello_connected, ping


async def ping_task(ws, interval):
    while True:
        print("Ping")
        await ws.send_json(ping)
        await asyncio.sleep(interval)


async def main(url="ws://localhost:8055/ws"):
    async with aiohttp.ClientSession() as session:
        n = 0
        async with session.ws_connect(url) as ws:
            connect_msg = await ws.receive_json()
            if connect_msg["et"] == hello_connected["et"]:
                print("Connected", connect_msg)
                setSrcAddr(connect_msg["dst"])
                print("src addr", getSrcAddr())
                asyncio.create_task(ping_task(ws, connect_msg["param"]["timeout_interval"]))
                await ws.send_json(get_state)
            else:
                print("Connection failed.", connect_msg)
                return
            async for msg in ws:
                print("GOT", msg.data)
                n += 1
                if n % 10 == 0:
                    await ws.send_json(
                        {
                            "et": 11,
                            "device_id": "tid.bid.counter1",
                            "action": "reset",
                            "param": 777,
                            "src": getSrcAddr(),
                            "dst": "tid.bid",
                        }
                    )


if __name__ == "__main__":
    asyncio.run(main())
