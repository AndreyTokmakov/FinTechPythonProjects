
import logging

from Credentials.credentials import GateIoConfiguration, Credentials
from GateIO.streams.GateIOWebSocketClient import GateIOWebSocketClient

creds: Credentials = GateIoConfiguration.read_credentials()


def on_message(ws: GateIOWebSocketClient, message: str):
    print(message)


def on_open(ws: GateIOWebSocketClient):
    ws.subscribe(["BTC_USDT", "100ms"], False)


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.DEBUG)
    ws_client = GateIOWebSocketClient(url="wss://api.gateio.ws/ws/v4/",
                                      channel="spot.order_book_update",
                                      api_key=creds.api_key,
                                      api_secret=creds.api_secret,
                                      on_open=on_open,
                                      on_message=on_message)
    ws_client.run_forever(ping_interval=5)



# wss://api.gateio.ws/api/v4
# wss://api.gateio.ws/ws/v4/