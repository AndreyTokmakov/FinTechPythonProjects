
import requests
import json
from copy import copy
from requests import Response
from typing import Dict
from GateIO.signature import generate_signature, generate_signature_testnet
from common.HTTPHeader import HTTPHeader

prefix: str = "/api/v4"

host: str = "https://api.gateio.ws"
gen_generate_signature_func = generate_signature

# host: str = 'https://fx-api-testnet.gateio.ws'
# en_generate_signature_func = generate_signature_testnet


base_headers: Dict[str, str] = {
    HTTPHeader.Accept.value: 'application/json',
    HTTPHeader.ContentType.value: 'application/json'
}


def get_account_info():
    url: str = '/account/detail'
    query_param = ''
    sign_headers: Dict[str, str] = gen_generate_signature_func('GET', prefix + url, query_param)
    headers: Dict[str, str] = copy(base_headers)
    headers.update(sign_headers)

    response: Response = requests.request('GET', host + prefix + url, headers=headers)
    print(host + prefix + url)
    print(response.text)
    print(response.json())


def get_sub_account_futures_balances():
    url: str = '/wallet/sub_account_futures_balances'
    query_param = ''
    sign_headers: Dict[str, str] = gen_generate_signature_func('GET', prefix + url, query_param)
    headers: Dict[str, str] = copy(base_headers)
    headers.update(sign_headers)

    response: Response = requests.get(host + prefix + url, headers=headers)
    print(response.json())


def get_wallet_total_balance():
    url: str = '/wallet/total_balance'
    params: Dict = {"currency": "USDT"}
    query_param = '&'.join([f'{k}={v}' for k, v in params.items()])
    sign_headers: Dict[str, str] = gen_generate_signature_func('GET', prefix + url, query_param)
    headers: Dict[str, str] = copy(base_headers)
    headers.update(sign_headers)

    print(f'GET {host + prefix + url}')
    response: Response = requests.get(host + prefix + url, headers=headers, params=params)
    print(response.json())

def get_wallet_sub_account_balances():
    url: str = '/wallet/sub_account_balances'
    query_param = {
        'sub_uid': ''
    }
    sign_headers: Dict[str, str] = gen_generate_signature_func('GET', prefix + url, query_param)
    headers: Dict[str, str] = copy(base_headers)
    headers.update(sign_headers)

    response: Response = requests.get(host + prefix + url, headers=headers, params=query_param)
    print(response.json())


# https://www.gate.io/docs/developers/apiv4/#retrieve-sub-account-balances
def get_spot_accounts():
    url: str = '/spot/accounts'
    query_param = ''
    sign_headers: Dict[str, str] = gen_generate_signature_func('GET', prefix + url, query_param)
    headers: Dict[str, str] = copy(base_headers)
    headers.update(sign_headers)

    response: Response = requests.get(host + prefix + url, headers=headers)
    print(response.json())

def get_margin_accounts():
    url: str = '/margin/accounts'
    query_param = ''
    sign_headers: Dict[str, str] = gen_generate_signature_func('GET', prefix + url, query_param)
    headers: Dict[str, str] = copy(base_headers)
    headers.update(sign_headers)

    response: Response = requests.get(host + prefix + url, headers=headers)
    print(response.json())

if __name__ == '__main__':
    # get_account_info()

    # get_wallet_total_balance()
    get_wallet_sub_account_balances()

    # get_spot_accounts()
    # get_margin_accounts()
    # get_sub_account_futures_balances()