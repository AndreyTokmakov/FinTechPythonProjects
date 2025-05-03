from typing import List, Dict

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from websockets.exceptions import ConnectionClosed
import uvicorn
import time


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_json(message)


app = FastAPI()
manager = ConnectionManager()


@app.websocket('/chargeStationState')
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            response = {'station': data['station'], 'timestamp': time.ctime()}
            await manager.send_personal_message(response, websocket)
    except (WebSocketDisconnect, ConnectionClosed):
        manager.disconnect(websocket)


@app.websocket('/ws/v1')
async def handle_trade_events(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            time.sleep(1)
            response: Dict = {'type': 'notification', 'timestamp': time.ctime()}
            await manager.send_personal_message(response, websocket)
    except (WebSocketDisconnect, ConnectionClosed):
        manager.disconnect(websocket)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=52525, log_level="error")
