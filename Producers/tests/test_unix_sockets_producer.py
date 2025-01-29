import json
import socket
import time

import requests

from requests import Response
from http import HTTPStatus
from typing import Dict, List
from Binance.api.api_keys import get_api_key
from Binance.api.common import HTTPHeader

socket_path: str = "/tmp/unix_socket"
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

    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
        client.connect(socket_path)
        client.sendall(payload)


def connection_test():
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
        client.connect(socket_path)
        time.sleep(10)


def connection_and_send():
    # message = '0123456789' * 1024 * 10 + "1234"
    message = "1234"
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
        client.connect(socket_path)
        for i in range(3):
            client.sendall(message.encode())
            time.sleep(1)

    time.sleep(0.05)


if __name__ == '__main__':
    # connection_test()
    connection_and_send()
