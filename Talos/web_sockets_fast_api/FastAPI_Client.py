import time

from websockets.exceptions import ConnectionClosed
import websockets
import asyncio
import json

url: str = 'ws://127.0.0.1:52525/chargeStationState'
events_url: str = 'ws://127.0.0.1:52525/ws/v1'


async def main():
    data = json.dumps({'station': '1'})
    async for websocket in websockets.connect(url):
        try:
            while True:
                await websocket.send(data)
                print(await asyncio.wait_for(websocket.recv(), timeout=10))
                await asyncio.sleep(2)
        except ConnectionClosed:
            continue  # attempt reconnecting to the server (otherwise, call break)


async def just_connect():
    async with websockets.connect(url) as websocket:
        print(websocket)


async def subscribe_on_events():
    async for websocket in websockets.connect(events_url):
        try:
            while True:
                message = await asyncio.wait_for(websocket.recv(), timeout=10)
                print(message)
                await asyncio.sleep(2)
        except ConnectionClosed:
            continue  # attempt reconnecting to the server (otherwise, call break)


if __name__ == '__main__':
    # asyncio.run(main())
    # asyncio.run(just_connect())
    asyncio.run(subscribe_on_events())
