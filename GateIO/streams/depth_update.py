import websocket
import json

stream_url: str = "wss://ws.gate.io/v3/"


def on_message(ws, message):
    data = json.loads(message)
    print(data)


def on_error(ws, error):
    print(f"Error: {error}")


def on_close(ws, close_status_code, close_msg):
    print(f"WebSocket connection closed: {close_status_code} - {close_msg}")


def on_open(ws):
    subscribe_message = {
        "id": 12312,
        "method": "depth.query",
        "params": ["BTC_USDT", 5, "1"]
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
