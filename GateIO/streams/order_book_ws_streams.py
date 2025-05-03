import json
import time
from typing import List, Dict
from websocket import create_connection

testnet_ws_url: str = 'wss://fx-ws-testnet.gateio.ws/v4/ws/btc'


def get_subscription_params(channel: str, payload: List) -> str:
    return json.dumps({
        'time': int(time.time()),
        'channel': channel,
        'event': 'subscribe',
        'payload': payload
    })


def book_ticker():
    ws = create_connection(testnet_ws_url)
    ws.send(get_subscription_params(channel='futures.book_ticker', payload=['BTC_USDT']))
    print(ws.recv())


def order_book_update():
    ws = create_connection(testnet_ws_url)
    ws.send(get_subscription_params(channel='futures.order_book_update', payload=['BTC_USD']))
    print(ws.recv())


def depth_query():
    ws = create_connection("wss://ws.gate.io/v3/")
    ws.send('{"id":12312, "method":"depth.query", "params":["BTC_USDT", 5, "0.0001"]}')
    print(ws.recv())


# https://www.gate.io/docs/developers/futures/ws/en/#best-ask-bid-subscription
if __name__ == '__main__':
    # book_ticker()
    # order_book_update()
    depth_query()
