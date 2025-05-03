import datetime
import ssl
from pathlib import Path
from typing import Dict, List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, APIRouter
from websockets.exceptions import ConnectionClosed
import uvicorn
import time


class TestDataStreams(object):

    @staticmethod
    def trade() -> Dict:
        timestamp: str = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000000Z")
        ''' To subscribe
            {
              "reqid": 3,
              "type": "subscribe",
              "streams": [
                {
                  "name": "Trade",
                  "StartDate": "2019-02-12T17:00:00.000000Z"
                }
              ]
            }
        '''

        return {
            "reqid": 3,
            "type": "Trade",
            "seq": 1,
            "initial": True,
            "ts": timestamp,
            "data": [
                {
                    "Timestamp": timestamp,
                    "User": "Talos",
                    "Symbol": "BTC-USD",
                    "OrderID": "cfa501f4-5a8f-4f42-a911-1804e16daf93",
                    "TradeID": "c4744fbc-7ed6-4191-9c74-ca0f357f26d9",
                    "Side": "Buy",
                    "Currency": "BTC",
                    "AmountCurrency": "USD",
                    "DealtCurrency": "BTC",
                    "FeeCurrency": "USD",
                    "Amount": "60000.00000000",
                    "Fee": "3.00",
                    "Price": "6000.00",
                    "PriceAllIn": "6000.30",
                    "Quantity": "10",
                    "Market": "gemini",
                    "TradeStatus": "Confirmed",
                    "TransactTime": timestamp,
                    "AggressorSide": "Buy",
                    "MarketTradeID": "12409809",
                    "TradeSource": "Market",
                    "Revision": 0
                }
            ]
        }


class ConnectionManager:

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    @staticmethod
    async def send_message(message: str, websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_json(message)


class Server(APIRouter):

    def __init__(self):
        super().__init__()
        self.manager = ConnectionManager()
        self.add_websocket_route("/test_endpoint", self.test_endpoint_handler)
        self.add_websocket_route("/ws/v1", self.handle_trade_events)

    async def test_endpoint_handler(self, websocket: WebSocket):
        await self.manager.connect(websocket)
        try:
            while True:
                data = await websocket.receive_json()
                response = {'station': data['station'], 'timestamp': time.ctime()}
                await self.manager.send_message(response, websocket)
        except (WebSocketDisconnect, ConnectionClosed):
            self.manager.disconnect(websocket)

    async def handle_trade_events(self, websocket: WebSocket):
        await self.manager.connect(websocket)
        try:
            while True:
                time.sleep(1)
                trade_data: Dict = TestDataStreams.trade()
                await self.manager.send_message(trade_data, websocket)
        except (WebSocketDisconnect, ConnectionClosed):
            self.manager.disconnect(websocket)


if __name__ == '__main__':

    certs_folder: str = f'{Path(__file__).parent.absolute()}/certs'
    print(certs_folder)

    '''
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.check_hostname = False
    ssl_context.load_cert_chain(certfile=f'{certs_folder}/server.crt',
                                keyfile=f'{certs_folder}/server.key')
    '''
    api: FastAPI = FastAPI()
    api.include_router(Server())

    uvicorn.run(app=api,
                host="0.0.0.0",
                port=8443,
                log_level="debug",
                # ssl_keyfile=f'{certs_folder}/server.key',
                # ssl_certfile=f'{certs_folder}/server.crt'
                )
