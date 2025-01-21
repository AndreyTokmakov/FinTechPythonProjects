import base64
import time
from typing import Dict

from cryptography.hazmat.primitives.serialization import load_pem_private_key

# Set up authentication
API_KEY: str = '9FmOZl0CCPVkzipOv0kXMx0gaL1BSeCuUhzG0CKilr0yjS6mxf037UvqM2nhAuXf'
PRIVATE_KEY_PATH: str = '/home/andtokm/Documents/Binance/ssh_Key/ed25519.pem'


def get_api_key() -> str:
    return API_KEY


def get_private_key(path: str = PRIVATE_KEY_PATH):
    with open(file=path, mode='rb') as file:
        return load_pem_private_key(data=file.read(), password=None)


def get_timestamp() -> int:
    return int(time.time() * 1000)  # UNIX timestamp in milliseconds


def get_params_with_signature(request_params: Dict) -> Dict:
    private_key = get_private_key()
    request_params['timestamp'] = get_timestamp()
    payload: str = '&'.join([f'{param}={value}' for param, value in request_params.items()])
    signature: bytes = base64.b64encode(private_key.sign(payload.encode('ASCII')))
    request_params['signature'] = signature
    return request_params

# https://binance-docs.github.io/apidocs/spot/en/#data-sources
#   Endpoint security type


