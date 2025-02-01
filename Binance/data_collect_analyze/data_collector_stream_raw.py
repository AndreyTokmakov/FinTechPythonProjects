import datetime
import json
import os
import signal
import sys
import websocket

from multiprocessing import Process, Queue, Event
from queue import Empty
from typing import Any, Dict
from websocket import WebSocket


class BinanceDataCollector(object):

    MAX_PAYLOAD_SIZE: int = 1024
    BINANCE_TESTNET_HOST: str = 'wss://testnet.binance.vision'

    def __init__(self):
        self.symbol: str = 'BTCUSDT'
        self.data_store_folder: str = f'{os.getcwd()}/../storage/raw_data'

        self.message_queue: Queue = Queue()
        self.stop_event: Event = Event()
        self.even_processor: Process = Process(target=self.even_dumper)

        self.web_socket = websocket.WebSocketApp(f'{self.BINANCE_TESTNET_HOST}/stream',
                                                 on_message=self.on_message,
                                                 on_error=self.on_error,
                                                 on_close=self.on_close,
                                                 on_open=self.on_open,
                                                 on_ping=self.on_ping)

        signal.signal(signal.SIGINT, self.signal_handler)

    def store_event(self,
                    event: Dict):
        try:
            stream_name, data = event.get('stream'), event.get('data')
            if not stream_name or not data:
                return

            stream_name = stream_name.replace('@', '_')
            data['timestamp'] = str(datetime.datetime.now())
            with open(file=f'{self.data_store_folder}/{stream_name}', mode='a') as file:
                file.write(json.dumps(data) + '\n')
        except Exception as exc:
            sys.stderr.write(str(exc))

    def even_dumper(self):
        while not self.stop_event.is_set():
            try:
                event: Dict = self.message_queue.get(timeout=0.25)
                self.store_event(event)
            except Empty:
                if self.stop_event.is_set():
                    break
                continue

    def on_message(self,
                   ws_socket: WebSocket,
                   message: Any):
        self.message_queue.put(json.loads(message))

    @staticmethod
    def on_error(ws_socket: WebSocket,
                 error: Any):
        sys.stderr.write(f"Error: {error}")

    @staticmethod
    def on_close(ws_socket: WebSocket,
                 close_status_code: Any,
                 close_msg: Any):
        print(f"WebSocket connection closed: {close_status_code} - {close_msg}")

    def on_open(self,
                ws_socket: WebSocket):
        subscribe_message: Dict = {
            "method": "SUBSCRIBE",
            "params": [
                f"{self.symbol.lower()}@miniTicker",
                f"{self.symbol.lower()}@bookTicker",
                f"{self.symbol.lower()}@ticker",
                f"{self.symbol.lower()}@@aggTrade",
                f"{self.symbol.lower()}@trade",
                f"{self.symbol.lower()}@kline_1000ms",
                f"{self.symbol.lower()}@depth"
                f"{self.symbol.lower()}@avgPrice"
            ],
            "id": 1
        }
        ws_socket.send(json.dumps(subscribe_message))

    @staticmethod
    def on_ping(ws_socket: WebSocket,
                message: Any):
        ws_socket.send(message, websocket.ABNF.OPCODE_PONG)

    def signal_handler(self, sig, frame):
        print('Stopping connector')
        self.stop_event.set()

    def start(self):
        self.even_processor.start()
        self.web_socket.run_forever()


if __name__ == '__main__':
    collector: BinanceDataCollector = BinanceDataCollector()
    collector.start()
