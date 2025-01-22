import json
import socket
import textwrap
import sys
from typing import Dict, List

host, port = '0.0.0.0', 52525


def send_simple_json():
    payload: bytes = json.dumps({
        'id': 1, 'side': 'BUY', 'quantity': 10, 'action': 'NEW'
    }).encode('utf-8')

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        #  sock.bind(('127.0.0.1', 10000))
        bytes_send: int = sock.sendto(payload, (host, port))

        print(f'{bytes_send} bytes_send')


def send_depth():
    with open('/home/andtokm/DiskS/ProjectsUbuntu/FinTechPythonProjects/Producers/tests/data/depth.json') as file:
        data: str = file.read()

    max_size: int = 1024
    chunks: List[str] = textwrap.wrap(data, max_size)
    parts: int = len(chunks)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        for block in chunks:
            parts -= 1
            payload: bytes = json.dumps({'p': parts, 't': 1, 'd': block}).encode('utf-8')
            bytes_send: int = sock.sendto(payload, (host, port))
            print(f'{bytes_send} bytes_send of {len(payload)}')


def send_depth_update():
    with open('/home/andtokm/DiskS/ProjectsUbuntu/FinTechPythonProjects/Producers/tests/data/depth_change.json') as file:
        data: str = file.read()

    max_size: int = 1024
    chunks: List[str] = textwrap.wrap(data, max_size)
    parts: int = len(chunks)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        for block in chunks:
            parts -= 1
            payload: bytes = json.dumps({'p': parts, 't': 2, 'd': block}).encode('utf-8')
            bytes_send: int = sock.sendto(payload, (host, port))
            print(f'{bytes_send} bytes_send of {len(payload)}')


if __name__ == '__main__':
    # send_simple_json()
    send_depth()
    # send_depth_update()
