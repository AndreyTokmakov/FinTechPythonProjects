import requests
from typing import Dict

host: str = "https://api.gateio.ws"
prefix: str = "/api/v4"
headers: Dict = {'Accept': 'application/json', 'Content-Type': 'application/json'}


def get_currencies():
    url = '/spot/currencies'
    r = requests.request('GET', host + prefix + url, headers=headers)
    print(r.json())


def specific_currency_pair():
    url = '/spot/currency_pairs/ETH_BTC'
    r = requests.request('GET', host + prefix + url, headers=headers)
    print(r.json())


# TODO: https://www.gate.io/docs/developers/apiv4/#get-details-of-a-specifc-currency-pair

if __name__ == '__main__':
    get_currencies()
    specific_currency_pair()
