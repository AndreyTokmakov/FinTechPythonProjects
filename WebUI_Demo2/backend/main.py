import asyncio
import json
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import websockets

app = FastAPI()

# Разрешаем фронтенду подключаться из любого места (Vite dev server)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подписка на Binance BTC/USDT order book (depth)
BINANCE_WS_URL = "wss://stream.binance.com:9443/ws/btcusdt@depth@100ms"

clients = set()
orderbook = {"bids": [], "asks": [], "last_price": 0.0}


# --- WebSocket endpoint для frontend ---
@app.websocket("/ws/book")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    clients.add(ws)
    try:
        while True:
            await asyncio.sleep(0.1)
    except Exception:
        pass
    finally:
        clients.remove(ws)


# --- Функция пуша данных всем подключенным клиентам ---
async def broadcast_orderbook():
    while True:
        if clients:
            message = json.dumps(orderbook)
            await asyncio.gather(*[client.send_text(message) for client in clients])
        await asyncio.sleep(0.1)


# --- Получаем данные с Binance ---
async def binance_orderbook():
    global orderbook
    async with websockets.connect(BINANCE_WS_URL) as ws:
        async for message in ws:
            data = json.loads(message)
            # bids и asks приходят в формате [["price","qty"], ...]
            orderbook["bids"] = [[float(p), float(q)] for p, q in data.get("b", [])]
            orderbook["asks"] = [[float(p), float(q)] for p, q in data.get("a", [])]
            # last price = mid между лучшей bid и ask
            if orderbook["bids"] and orderbook["asks"]:
                orderbook["last_price"] = (orderbook["bids"][0][0] + orderbook["asks"][0][0]) / 2


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(binance_orderbook())
    asyncio.create_task(broadcast_orderbook())
