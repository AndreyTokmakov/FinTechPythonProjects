
import asyncio
import pathlib
import ssl
import websockets

testnet_ws_host: str = 'wss://testnet.binance.vision'
stream_url: str = f'{testnet_ws_host}/stream'

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)


async def hello():
    async with websockets.connect(uri=stream_url, ssl=ssl_context) as websocket:

        await websocket.send(name)
        print(f">>> {name}")

        greeting = await websocket.recv()
        print(f"<<< {greeting}")


if __name__ == "__main__":
    asyncio.run(hello())
