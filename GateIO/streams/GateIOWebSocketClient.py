import hashlib
import hmac
import json
import logging
import time
import threading

from websocket import WebSocketApp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GateIOWebSocketClient(WebSocketApp):

    def __init__(self, url: str,
                 channel: str,
                 api_key: str,
                 api_secret: str,
                 **kwargs):
        super(GateIOWebSocketClient, self).__init__(url, **kwargs)
        self.channel = channel
        self.api_key = api_key
        self.api_secret = api_secret
        self.event = threading.Event()

    def _send_ping(self):
        while not self.event.wait(10):
            self.last_ping_tm = time.time()
            if self.sock:
                try:
                    self.sock.ping()
                except Exception as ex:
                    logger.warning("send_ping routine terminated: {}".format(ex))
                    break
                try:
                    self.request("spot.ping", auth_required=False)
                except Exception as e:
                    raise e

    def request(self,
                channel: str,
                event=None,
                payload=None,
                auth_required=True):
        current_time: int = int(time.time())
        data = {
            "time": current_time,
            "channel": channel,
            "event": event,
            "payload": payload,
        }
        if auth_required:
            message = f'channel={channel}&event={event}&time={current_time}'
            data['auth'] = {
                "method": "api_key",
                "KEY": self.api_key,
                "SIGN": self.get_sign(message),
            }
        data = json.dumps(data)
        logger.info(f'request: {data}')
        self.send(data)

    def get_sign(self, message):
        h = hmac.new(self.api_secret.encode("utf8"), message.encode("utf8"), hashlib.sha512)
        return h.hexdigest()

    def subscribe(self, payload=None, auth_required=True):
        self.request(self.channel, "subscribe", payload, auth_required)

    def unsubscribe(self, payload=None, auth_required=True):
        self.request(self.channel, "unsubscribe", payload, auth_required)


def on_message(ws: GateIOWebSocketClient, message: str):
    logger.info("message received from server: {}".format(message))


def on_open(ws: GateIOWebSocketClient):
    logger.info('websocket connected')
    ws.subscribe(['BTC_USDT'], False)

