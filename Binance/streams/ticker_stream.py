import websocket
import json

testnet_ws_host: str = 'wss://testnet.binance.vision'
stream_url: str = f'{testnet_ws_host}/stream'


def on_message(ws, message):
    data = json.loads(message)

    print(str(data).replace('\'', '\"'))
    '''
    if 'stream' in data:
        # you can pipeline this data to your function, analysis or backtesting
        print(f"Symbol: {data['data']['s']}, Price: {data['data']['c']}, Time: {data['data']['E']}")
    else:
        print(f"Received message: {message}")
    '''


def on_error(ws, error):
    print(f"Error: {error}")


def on_close(ws, close_status_code, close_msg):
    print(f"WebSocket connection closed: {close_status_code} - {close_msg}")


def on_open(ws):
    subscribe_message = {
        "method": "SUBSCRIBE",
        "params": [
            "ethusdt@ticker",
            "btcusdt@ticker",
            "xrpusdt@ticker",
            "bnbusdt@ticker",
            "pythusdt@ticker",
            "memeusdt@ticker",
            "tstusdt@ticker",
        ],
        "id": 1
    }
    ws.send(json.dumps(subscribe_message))


def on_ping(ws, message):
    print(f"Received ping: {message}")
    ws.send(message, websocket.ABNF.OPCODE_PONG)
    print(f"Sent pong: {message}")


if __name__ == "__main__":
    websocket.enableTrace(True)
    web_socket = websocket.WebSocketApp(stream_url,
                                        on_message=on_message,
                                        on_error=on_error,
                                        on_close=on_close,
                                        on_open=on_open,
                                        on_ping=on_ping)
    web_socket.run_forever()
