import websocket
import json

testnet_ws_host: str = 'wss://testnet.binance.vision'
stream_url: str = f'{testnet_ws_host}/stream'


def on_message(ws, message):
    data = json.loads(message)
    print(data)


def on_error(ws, error):
    print(f"Error: {error}")


def on_close(ws, close_status_code, close_msg):
    print(f"WebSocket connection closed: {close_status_code} - {close_msg}")


def on_open(ws):
    subscribe_message = {
        "method": "SUBSCRIBE",
        "params": [
            "btcusdt@miniTicker",
            # "btcusdt@bookTicker",
            # "btcusdt@ticker",
            # "btcusdt@depth@100ms",
            # "btcusdt@depth@1000ms",
            # "btcusdt@aggTrade",
            # "btcusdt@trade"
            # "btcusdt@kline_1000ms"
            "btcusdt@avgPrice"
        ],
        "id": 1
    }
    ws.send(json.dumps(subscribe_message))


def on_ping(ws, message):
    print('=' * 90, ' PING ', '-' * 90)
    ws.send(message, websocket.ABNF.OPCODE_PONG)
    print('=' * 186)


if __name__ == "__main__":
    websocket.enableTrace(True)
    web_socket = websocket.WebSocketApp(stream_url,
                                        on_message=on_message,
                                        on_error=on_error,
                                        on_close=on_close,
                                        on_open=on_open,
                                        on_ping=on_ping)
    web_socket.run_forever()

'''
"btcusdt@bookTicker"
    Individual Symbol Book Ticker Streams
    Pushes any update to the best bid or ask's price or quantity in real-time for a specified symbol. 
    Multiple <symbol>@bookTicker streams can be subscribed to over one connection.
    
    {
      "u":400900217,     // order book updateId
      "s":"BNBUSDT",     // symbol
      "b":"25.35190000", // best bid price
      "B":"31.21000000", // best bid qty
      "a":"25.36520000", // best ask price
      "A":"40.66000000"  // best ask qty
    }


'''
