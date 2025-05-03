import json
import time

import requests
from http import HTTPStatus
from requests import Response
from TestNetworkServices.common.HTTPHeader import HTTPHeader

url: str = 'http://0.0.0.0:8080/'
endpoint: str = 'public'
rest_url: str = f'{url}/{endpoint}'


def print_response(response: Response):
    if HTTPStatus.OK == response.status_code:
        if 'application/json' == response.headers.get(HTTPHeader.ContentType):
            print(json.dumps(response.json(), indent=4))
        else:
            print(response.text)
    else:
        print(f"Error {response.status_code}")
        print(response.text)


def get_info():
    params = {'accountId': 123}
    response: Response = requests.get(url=f'{rest_url}/account_balance', params=params)
    print_response(response)


if __name__ == '__main__':
    get_info()
