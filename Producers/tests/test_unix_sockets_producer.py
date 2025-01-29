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


if __name__ == '__main__':
    print(1)
