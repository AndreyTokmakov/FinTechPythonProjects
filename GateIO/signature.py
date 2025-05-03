import json
import time
import hashlib
import hmac
import six
from typing import Dict
from GateIO.credentials import Credentials, read_credentials, read_credentials_testnet

creds: Credentials = read_credentials()
test_net_creds: Credentials = read_credentials_testnet()


def __get_sing__(credentials: Credentials, method, url, query_string=None, payload_string=None):
    timestamp = time.time()

    m = hashlib.sha512()
    if payload_string is not None:
        if not isinstance(payload_string, six.string_types):
            body = json.dumps(payload_string)
        m.update(body.encode('utf-8'))
    hashed_payload = m.hexdigest()

    s = '%s\n%s\n%s\n%s\n%s' % (method, url, query_string or "", hashed_payload, timestamp)
    print(s)
    print(s.encode('utf-8'))
    signature = hmac.new(credentials.api_secret.encode('utf-8'), s.encode('utf-8'), hashlib.sha512).hexdigest()
    headers =  {
        'KEY': credentials.api_key,
        'Timestamp': str(timestamp),
        'SIGN': signature
    }

    print(headers)
    return headers

def __generate_signature__(credentials: Credentials,
                           method: str,
                           url: str,
                           query_string,
                           payload_string) -> Dict[str, str]:
    payload: str = payload_string or ""
    timestamp: time = time.time()

    hash = hashlib.sha512()
    hash.update(payload.encode('utf-8'))
    hashed_payload: str = hash.hexdigest()

    query_string = f'sub_uid={query_string.get("sub_uid")}'

    msg: bytes = f'{method}\n{url}\n{query_string or ""}\n{hashed_payload}\n{timestamp}'.encode('utf-8')
    print(msg)
    signature: str = hmac.new(credentials.api_secret.encode('utf-8'), msg, hashlib.sha512).hexdigest()

    print(credentials.api_key)
    print(credentials.api_secret)

    hash = hashlib.sha512()
    hash.update(payload.encode('utf-8'))

    return {
        'KEY': credentials.api_key,
        'Timestamp': str(timestamp),
        'SIGN': signature
    }

def generate_signature(method: str,
                       url: str,
                       query_string=None,
                       payload_string=None) -> Dict[str, str]:
    return __generate_signature__(credentials=creds,
                                  method=method,
                                  url=url,
                                  query_string=query_string,
                                  payload_string=payload_string)

def generate_signature_testnet(method: str,
                               url: str,
                               query_string=None,
                               payload_string=None) -> Dict[str, str]:
    return __generate_signature__(credentials=test_net_creds,
                                  method=method,
                                  url=url,
                                  query_string=query_string,
                                  payload_string=payload_string)