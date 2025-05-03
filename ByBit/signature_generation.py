import hashlib
import hmac
import time
from typing import Dict


def get_timestamp() -> int:
    return int(time.time_ns() / 1_000_000)


def generate_signature(params: Dict,
                       recv_window: int = 20000,
                       timestamp: int = 0) -> None:
    api_key: str = 'NPy3UB5UVTv7rT8eZe'
    secret: str = 'Ow0IRCNjUMPHkcTwWdFaGO31cUANYtZr9KAx'

    # timestamp+api_key+recv_window+queryString
    data: str = f'{timestamp}{api_key}{recv_window}{timestamp}' + \
        '&'.join([f'{key}={value}' for key, value in params.items()])
    print(data)

    byte_key: bytes = secret.encode("UTF-8")
    message: bytes = data.encode()
    msg_hashed: str = hmac.new(byte_key, message, hashlib.sha256).hexdigest()

    print(msg_hashed)

if __name__ == '__main__':
    params: Dict = {
        'accountType': 'UNIFIED',
        'coin': 'BTC'
    }

    generate_signature(params=params, timestamp=get_timestamp())
