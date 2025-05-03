import datetime
import hmac
import hashlib
import base64
from inspect import signature
from typing import Tuple

talos_sandbox_url: str = 'tal-1.sandbox.talostrading.com'
talos_prod_url: str = 'tal-1.prod.talostrading.com'

# talos_sandbox_url: str = 'wss://tal-1.sandbox.talostrading.com/ws/v1'
api_key, api_secret = '<apikey>', '<apisecret>'


def get_signature(host: str = talos_sandbox_url,
                  path: str = '/ws/v1',
                  secret: str = api_secret,
                  delimiter: str = '\n') -> Tuple[str, str]:
    utc_datetime: str = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000000Z")
    params: str = delimiter.join(["GET", utc_datetime, host, path, ])
    hash_obj: hmac.HMAC = hmac.new(secret.encode('ascii'), params.encode('ascii'), hashlib.sha256)
    hash_obj.hexdigest()

    return base64.urlsafe_b64encode(hash_obj.digest()).decode(), utc_datetime


if __name__ == "__main__":
    signature, timestamp = get_signature(host=talos_sandbox_url, path='/ws/v1', secret=api_secret)
    header = {
        "TALOS-KEY": api_key,
        "TALOS-SIGN": signature,
        "TALOS-TS": timestamp,
    }

    print(header)

    '''
    ws = create_connection("wss://" + host + path, header=header)
    while True:
        print(ws.recv())
    '''
