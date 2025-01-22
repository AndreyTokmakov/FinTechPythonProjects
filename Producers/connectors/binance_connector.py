import json
import logging
import random
import signal
import socket
import string
import textwrap
import time
from enum import Enum, IntEnum

import requests
import multiprocessing.queues

from dataclasses import dataclass
from http import HTTPStatus
from multiprocessing import Process, Queue, Event
from queue import Empty
from typing import Any, List, Tuple
from requests import Response

host, port = '0.0.0.0', 52525


class EventType(IntEnum):
    DepthSnapshot = 1
    DepthUpdate = 2


class BinanceConnector(object):

    MAX_PAYLOAD_SIZE: int = 1024

    def __init__(self):
        self.message_queue: Queue = Queue()
        self.stop_event: Event = Event()

        self.forwarder: Process = Process(target=self.even_forwarder)
        self.consumer: Process = Process(target=self.event_consumer)

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
        # FIXME
        with open('/home/andtokm/DiskS/ProjectsUbuntu/FinTechPythonProjects/Producers/tests/data/depth_change.json') as file:
            data: str = file.read()
        while True:
            if self.stop_event.is_set():
                return
            message: str = data
            self.message_queue.put((EventType.DepthUpdate, message))
            time.sleep(0.1)

    def signal_handler(self, sig, frame):
        print('Stopping connector')
        self.stop_event.set()

    def start(self):
        self.forwarder.start()
        self.consumer.start()


# TODO: Redis instead UDP ?? https://opstree.com/blog/2019/04/16/redis-best-practices-and-performance-tuning/

if __name__ == '__main__':
    connector: BinanceConnector = BinanceConnector()
    connector.start()

