import datetime
import time
from http import HTTPStatus

import requests
from typing import Dict, List

from requests import Response

from Binance.api.api_keys import get_api_key, get_params_with_signature
from Binance.api.common import HTTPHeader

TESTNET_API_HOST: str = 'https://testnet.binance.vision/api'
TESTNET_WS_HOST: str = 'wss://testnet.binance.vision/ws'
TESTNET_WS_STREAM_HOST: str = 'wss://testnet.binance.vision/stream'

api_key: str = get_api_key()

default_headers: Dict = {'X-MBX-APIKEY': api_key}


# params: Dict = get_params_with_signature({})


#  https://binance-docs.github.io/apidocs/spot/en/#test-connectivity

def print_response(response: Response):
    if HTTPStatus.OK == response.status_code:  # HTTP_OK
        content_type: str = response.headers.get(HTTPHeader.ContentType)
        if content_type and 'application/json' in content_type:
            print(response.json())
        else:
            print(response.text)
    else:
        print(f"Error {response.status_code}")


def send_get_request(endpoint: str,
                     headers: Dict = None,
                     params: Dict = None):
    if not headers:
        headers = default_headers
    if not params:
        params = {}
    response: Response = requests.get(url=f'{TESTNET_API_HOST}/{endpoint}',
                                      headers=headers,
                                      params=params)
    print_response(response)


def ping():
    send_get_request('v3/ping')


def get_time():
    send_get_request('v3/time')


def exchange_info():
    send_get_request('v3/exchangeInfo')


# Order book
def get_depth(symbol: str = 'BTCUSDT',
              limit: int = 5000):
    send_get_request(endpoint='v3/depth', params={'symbol': symbol, 'limit': limit})


# Recent trades list
def get_trades(symbol: str = 'BTCUSDT',
               limit: int = 1000):
    send_get_request(endpoint='v3/trades', params={'symbol': symbol, 'limit': limit})


# Current average price for a symbol.
def get_average_price(symbol: str = 'BTCUSDT'):
    send_get_request(endpoint='v3/avgPrice', params={'symbol': symbol})


def get_ticker_24_hour(symbol: str = 'BTCUSDT'):
    """ 24 hour rolling window price change statistics. Careful when accessing this with no symbol."""
    send_get_request(endpoint='v3/ticker/24hr', params={'symbol': symbol})


def get_ticker_trading_day(symbol: str = 'BTCUSDT'):
    """
        Price change statistics for a trading day.
        https://developers.binance.com/docs/binance-spot-api-docs/testnet/rest-api/market-data-endpoints#trading-day-ticker
    """
    send_get_request(endpoint='v3/ticker/tradingDay', params={'symbol': symbol})


def get_ticker_symbol_price(symbol: str = 'BTCUSDT'):
    """
        Latest price for a symbol or symbols.
        https://developers.binance.com/docs/binance-spot-api-docs/testnet/rest-api/market-data-endpoints#symbol-price-ticker
    """
    send_get_request(endpoint='v3/ticker/price', params={'symbol': symbol})


def get_ticker_best_book(symbol: str = 'BTCUSDT'):
    """
    Best price/qty on the order book for a symbol or symbols.
    https://developers.binance.com/docs/binance-spot-api-docs/testnet/rest-api/market-data-endpoints#symbol-order-book-ticker
    """
    send_get_request(endpoint='v3/ticker/bookTicker', params={'symbol': symbol})


def get_open_orders(timestamp: int,
                    symbol: str = 'BTCUSDT'):
    """
    Get all open orders on a symbol. Careful when accessing this with no symbol.
    https://developers.binance.com/docs/binance-spot-api-docs/testnet/rest-api/trading-endpoints#current-open-orders-user_data
    """
    send_get_request(endpoint='v3/openOrders', params={'symbol': symbol, 'timestamp': timestamp, 'recvWindow': 50000})


if __name__ == '__main__':
    # ping()
    # get_time()
    # exchange_info()
    get_depth()
    # get_trades()
    # get_average_price()
    # get_ticker_24_hour()
    # get_ticker_trading_day()
    # get_ticker_symbol_price()
    # get_ticker_best_book()

    # get_open_orders(timestamp=int(time.time_ns() / 1000))

