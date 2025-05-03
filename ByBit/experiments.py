import hashlib
import hmac
import time

import requests
from requests import Response
from typing import Dict

from Credentials.credentials import ByBitConfiguration, Credentials

api_endpoint: str = "https://api-testnet.bybit.com/v5"
credentials: Credentials = ByBitConfiguration.read_credentials()


def get_timestamp() -> int:
    return int(time.time_ns() / 1_000_000)


def generate_signature(params: Dict,
                       recv_window: int = 20000,
                       timestamp: int = 0) -> str:
    # # timestamp+api_key+recv_window+queryString
    data: str = f'{timestamp}{credentials.api_key}{recv_window}' + '&'.join([f'{k}={v}' for k, v in params.items()])
    print(data)

    byte_key: bytes = credentials.api_secret.encode("UTF-8")
    message: bytes = data.encode()
    return hmac.new(byte_key, message, hashlib.sha256).hexdigest()


def get_balance():
    url: str = f'{api_endpoint}/account/wallet-balance'
    timestamp: int = get_timestamp()
    window: int = 20_000
    params: Dict = {
        'accountType': 'UNIFIED',
        'coin': 'BTC'
    }

    signature: str = generate_signature(params=params, timestamp=timestamp, recv_window=window)
    headers: Dict = {
        'X-BAPI-API-KEY': credentials.api_key,
        'X-BAPI-SIGN': signature,
        'X-BAPI-TIMESTAMP': f'{timestamp}',
        'X-BAPI-RECV-WINDOW': f'{window}'
    }

    response: Response = requests.get(url=url, headers=headers, params=params)
    print(response.text)


def get_account_info():
    url: str = f'{api_endpoint}/account/info'
    timestamp: int = get_timestamp()
    window: int = 20_000
    params: Dict = {}
    signature: str = generate_signature(params=params, timestamp=timestamp, recv_window=window)
    headers: Dict = {
        'X-BAPI-API-KEY': credentials.api_key,
        'X-BAPI-SIGN': signature,
        'X-BAPI-TIMESTAMP': f'{timestamp}',
        'X-BAPI-RECV-WINDOW': f'{window}'
    }

    response: Response = requests.get(url=url, headers=headers, params=params)
    print(response.text)


if __name__ == '__main__':
    # get_balance()
    get_account_info()

