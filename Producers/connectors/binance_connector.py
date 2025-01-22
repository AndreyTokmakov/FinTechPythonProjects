import json
import logging
import random
import signal
import socket
import string
import sys
import textwrap
import time
from enum import Enum, IntEnum
import websocket
import requests
import multiprocessing.queues

from dataclasses import dataclass
from http import HTTPStatus
from multiprocessing import Process, Queue, Event
from queue import Empty
from typing import Any, List, Tuple, Dict
from requests import Response
from websocket import WebSocket

host, port = '0.0.0.0', 52525


class EventType(IntEnum):
    DepthSnapshot = 1
    DepthUpdate = 2


class BinanceConnector(object):
    MAX_PAYLOAD_SIZE: int = 1024
    BINANCE_TESTNET_HOST: str = 'wss://testnet.binance.vision'

    def __init__(self):
        self.message_queue: Queue = Queue()
        self.stop_event: Event = Event()

        self.forwarder: Process = Process(target=self.even_forwarder)
        # self.consumer: Process = Process(target=self.event_consumer)

        self.web_socket = websocket.WebSocketApp(f'{self.BINANCE_TESTNET_HOST}/stream',
                                                 on_message=self.on_message,
                                                 on_error=self.on_error,
                                                 on_close=self.on_close,
                                                 on_open=self.on_open,
                                                 on_ping=self.on_ping)

        signal.signal(signal.SIGINT, self.signal_handler)

    def send_event(self,
                   udp_socket: socket.socket,
                   event_type: EventType,
                   msg: str):
        chunks: List[str] = textwrap.wrap(msg, self.MAX_PAYLOAD_SIZE)
        parts: int = len(chunks)
        for block in chunks:
            parts -= 1
            payload: bytes = json.dumps({'p': parts, 't': event_type, 'd': block}).encode('utf-8')
            bytes_send: int = udp_socket.sendto(payload, (host, port))
            print(f'{bytes_send} bytes send')

    def even_forwarder(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            while True:
                try:
                    event_type, data = self.message_queue.get(timeout=0.25)
                    self.send_event(udp_socket=sock, event_type=event_type, msg=data)
                except Empty:
                    if self.stop_event.is_set():
                        break
                    continue

    def event_consumer(self) -> None:
        while True:
            if self.stop_event.is_set():
                return
            # self.message_queue.put((event_type, message))
            time.sleep(0.1)

    def on_message(self,
                   ws_socket: WebSocket,
                   message: Any):
        self.message_queue.put((EventType.DepthUpdate, message))

    @staticmethod
    def on_error(ws_socket: WebSocket,
                 error: Any):
        sys.stderr.write(f"Error: {error}")

    @staticmethod
    def on_close(ws_socket: WebSocket,
                 close_status_code: Any,
                 close_msg: Any):
        print(f"WebSocket connection closed: {close_status_code} - {close_msg}")

    @staticmethod
    def on_open(ws_socket: WebSocket):
        subscribe_message: Dict = {
            "method": "SUBSCRIBE",
            "params": [
                # "btcusdt@aggTrade",
                "btcusdt@depth"
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
        self.forwarder.start()
        # self.consumer.start()
        self.web_socket.run_forever()


# TODO: Redis instead UDP ?? https://opstree.com/blog/2019/04/16/redis-best-practices-and-performance-tuning/

if __name__ == '__main__':
    connector: BinanceConnector = BinanceConnector()
    connector.start()
