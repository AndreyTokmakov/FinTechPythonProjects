
import requests
from typing import Dict
from Binance.api.api_keys import get_params_with_signature, get_api_key

TESTNET_API_HOST: str = 'https://testnet.binance.vision/api'
TESTNET_WS_HOST: str = 'wss://testnet.binance.vision/ws'


if __name__ == '__main__':

    api_key: str = get_api_key()

    # https://testnet.binance.vision/api/v3/klines?symbol=BTCUSDT&limit=1&interval=1m
    # [[1727494920000,"66050.01000000","66051.98000000","66027.41000000","66027.41000000","0.19485000",
    # 1727494979999,"12866.89971470",51,"0.08725000","5761.73242340","0"]]

    # Set up the request parameters
    params: Dict = {
        'symbol': 'BTCUSDT',
        'side': 'BUY',
        'type': 'LIMIT',
        'timeInForce': 'GTC',
        'quantity': '0.0100000',
        'price': '65165.9',
    }

    params = get_params_with_signature(params)

    headers: Dict = {
        'X-MBX-APIKEY': api_key,
    }
    response = requests.post(url=f'{TESTNET_API_HOST}/v3/order',
                             headers=headers,
                             data=params)
    print(response.json())
