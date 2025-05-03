from pybit.unified_trading import WebSocket
from time import sleep


def handle_message(message):
    # print(message.replace('\'', '\"'))
    print(message)


if __name__ == '__main__':

    ws = WebSocket(testnet=False,
                   channel_type="linear")
    ws.orderbook_stream(depth=50,
                        symbol="BTCUSDT",
                        callback=handle_message)
    while True:
        sleep(1)
