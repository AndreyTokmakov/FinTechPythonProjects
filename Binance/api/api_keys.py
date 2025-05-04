import base64
import time
from typing import Dict
from credentials.credentials import Credentials, BinanceConfiguration
from cryptography.hazmat.primitives.serialization import load_pem_private_key

creds: Credentials = BinanceConfiguration.read_credentials()


def get_api_key() -> str:
    return creds.api_key


def get_private_key(path: str = creds.private_key_path):
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


