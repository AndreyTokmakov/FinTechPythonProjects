import asyncio
import websockets

talos_trading_url: str = 'wss://tal-1.sandbox.talostrading.com/ws/v1'


async def hello():
    async with websockets.connect(talos_trading_url) as websocket:
        name = input("What's your name? ")
        await websocket.send(name)
        print(f">>> {name}")

        greeting = await websocket.recv()
        print(f"<<< {greeting}")


if __name__ == "__main__":
    asyncio.run(hello())
