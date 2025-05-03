import ssl
import time
from pathlib import Path

from websockets.exceptions import ConnectionClosed
import websockets
import asyncio
import json

events_url: str = 'wss://127.0.0.1:52525/ws/v1'


async def read_events(ssl_ctx):
    async for websocket in websockets.connect(uri=events_url, ssl=ssl_ctx):
        try:
            while True:
                message = await asyncio.wait_for(websocket.recv(), timeout=10)
                print(message)
        except ConnectionClosed:
            continue  # attempt reconnecting to the server (otherwise, call break)


if __name__ == '__main__':

    certs_folder: str = f'{Path(__file__).parent.absolute()}/certs'
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = False
    ssl_context.load_cert_chain(certfile=f'{certs_folder}/server.crt',
                                keyfile=f'{certs_folder}/server.key')

    asyncio.run(read_events(ssl_context))
