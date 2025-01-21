import logging
import random
import signal
import socket
import string
import time

import requests
import multiprocessing.queues

from dataclasses import dataclass
from http import HTTPStatus
from multiprocessing import Process, Queue, Event
from queue import Empty
from typing import Any, List, Tuple
from requests import Response

host, port = '0.0.0.0', 52525


class BinanceConnector(object):

    def __init__(self):
        self.message_queue: Queue = Queue()
        self.stop_event: Event = Event()

        self.forwarder: Process = Process(target=self.even_forwarder)
        self.consumer: Process = Process(target=self.event_consumer)

        signal.signal(signal.SIGINT, self.signal_handler)

    def even_forwarder(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            while True:
                try:
                    event: str = self.message_queue.get(timeout=0.25)
                    payload: bytes = event.encode('utf-8')
                    bytes_send: int = sock.sendto(payload, (host, port))
                    print(f'{bytes_send} bytes send')
                except Empty:
                    if self.stop_event.is_set():
                        break
                    continue

    def event_consumer(self) -> None:
        counter: int = 0
        while True:
            if self.stop_event.is_set():
                return
            counter += 1
            message: str = f'("id": {counter})'
            self.message_queue.put(message)
            time.sleep(0.1)

    def signal_handler(self, sig, frame):
        print('Stopping connector')
        self.stop_event.set()

    def start(self):
        self.forwarder.start()
        self.consumer.start()


if __name__ == '__main__':
    connector: BinanceConnector = BinanceConnector()
    connector.start()

