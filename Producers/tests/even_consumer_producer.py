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


def even_forwarder(queue: multiprocessing.Queue, event: Event):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        while True:
            try:
                event: str = queue.get(timeout=0.25)
                payload: bytes = event.encode('utf-8')
                bytes_send: int = sock.sendto(payload, (host, port))
                print(f'{bytes_send} bytes send')
            except Empty:
                if event.is_set():
                    break
                continue


def event_consumer(queue: multiprocessing.Queue,
                   event: Event) -> None:
    counter: int = 0
    while True:
        if event.is_set():
            return
        counter += 1
        message: str = f'("id": {counter})'
        queue.put(message)
        time.sleep(0.1)


if __name__ == '__main__':
    message_queue: Queue = Queue()
    stop_event: Event = Event()


    def signal_handler(sig, frame):
        print('Stopping connector')
        stop_event.set()

    print_process: Process = Process(target=even_forwarder, args=(message_queue, stop_event,))
    print_process.start()

    print_process: Process = Process(target=event_consumer, args=(message_queue, stop_event,))
    print_process.start()
