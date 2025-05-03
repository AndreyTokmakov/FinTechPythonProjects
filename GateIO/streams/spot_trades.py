import logging
from credentials.credentials import GateIoConfiguration, Credentials
from GateIO.streams.GateIOWebSocketClient import GateIOWebSocketClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
creds: Credentials = GateIoConfiguration.read_credentials()


def on_message(ws: GateIOWebSocketClient, message: str):
    logger.info("message received from server: {}".format(message))


def on_open(ws: GateIOWebSocketClient):
    logger.info('websocket connected')
    ws.subscribe(['BTC_USDT'], False)


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.DEBUG)
    ws_client = GateIOWebSocketClient(url="wss://api.gateio.ws/ws/v4/",
                                      channel="spot.trades",
                                      api_key=creds.api_key,
                                      api_secret=creds.api_secret,
                                      on_open=on_open,
                                      on_message=on_message)
    ws_client.run_forever(ping_interval=5)
