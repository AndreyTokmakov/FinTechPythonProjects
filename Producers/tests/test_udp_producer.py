import json
import socket
import textwrap
import sys
from http import HTTPStatus
from typing import Dict, List

import requests
from requests import Response

from Binance.api.api_keys import get_api_key
from Binance.api.common import HTTPHeader

host, port = '0.0.0.0', 52525
TESTNET_API_HOST: str = 'https://testnet.binance.vision/api'
api_key: str = get_api_key()

default_headers: Dict = {'X-MBX-APIKEY': api_key}


def send_get_request(endpoint: str,
                     headers: Dict = None,
                     params: Dict = None) -> Dict:
    if not headers:
        headers = default_headers
    if not params:
        params = {}
    response: Response = requests.get(url=f'{TESTNET_API_HOST}/{endpoint}',
                                      headers=headers,
                                      params=params)
    if HTTPStatus.OK == response.status_code:  # HTTP_OK
        content_type: str = response.headers.get(HTTPHeader.ContentType)
        if content_type and 'application/json' in content_type:
            return response.json()
        else:
            return {}
    else:
        return {}


def get_depth(symbol: str = 'BTCUSDT',
              limit: int = 5000) -> Dict:
    return send_get_request(endpoint='v3/depth', params={'symbol': symbol, 'limit': limit})


def send_simple_json():
    payload: bytes = json.dumps({
        'id': 1, 'side': 'BUY', 'quantity': 10, 'action': 'NEW'
    }).encode('utf-8')

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        #  sock.bind(('127.0.0.1', 10000))
        bytes_send: int = sock.sendto(payload, (host, port))

        print(f'{bytes_send} bytes_send')


def send_depth(symbol: str = 'BTCUSDT',
               limit: int = 10000):
    depth: Dict = get_depth(symbol=symbol, limit=limit)
    data: str = json.dumps({"data": depth, "s": symbol})

    max_size: int = 1024
    chunks: List[str] = textwrap.wrap(data, max_size)
    parts: int = len(chunks)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        for block in chunks:
            parts -= 1
            payload: bytes = json.dumps({'p': parts, 't': 1, 'd': block}).encode('utf-8')
            bytes_send: int = sock.sendto(payload, (host, port))
            # print(f'{bytes_send} bytes_send of {len(payload)}')
            # print(payload)


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
            # print(payload)


if __name__ == '__main__':
    # send_simple_json()
    # send_depth_update()

    send_depth(symbol='BTCUSDT')
    # send_depth(symbol='ETHUSDT')
