import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import asyncio
import json
import random

from starlette.staticfiles import StaticFiles

app = FastAPI()

# === Отдаём статические файлы ===
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# пример данных стакана
orderbook = {
    "bids": [],
    "asks": [],
    "last_price": 0.0
}


async def generate_fake_orderbook():
    """Фейковая генерация стакана (для демо)."""
    while True:
        mid = random.uniform(100, 110)

        orderbook["bids"] = [
            [round(mid - i * 0.1, 2), random.randint(1, 10)]
            for i in range(10)
        ]
        orderbook["asks"] = [
            [round(mid + i * 0.1, 2), random.randint(1, 10)]
            for i in range(10)
        ]
        orderbook["last_price"] = mid

        await asyncio.sleep(1)


@app.on_event("startup")
async def start_data_feed():
    asyncio.create_task(generate_fake_orderbook())


@app.websocket("/ws/book")
async def websocket_endpoint(ws: WebSocket):
    print('websocket_endpoint()')
    await ws.accept()
    while True:
        await ws.send_text(json.dumps(orderbook))
        await asyncio.sleep(0.5)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")