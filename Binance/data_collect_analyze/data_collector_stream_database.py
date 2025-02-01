import datetime
import json
import os
import signal
import sys
from enum import Enum
from sqlite3 import Cursor

import websocket
import sqlite3

from multiprocessing import Process, Queue, Event
from queue import Empty
from typing import Any, Dict
from websocket import WebSocket

from Binance.common.BookTick import BookTick
from Binance.common.Tick import Tick
from Binance.common.AvgPrice import AvgPrice
from Binance.common.Trade import Trade


class StreamType(Enum):
    Unknown = 0
    Tick = 1
    MiniTicker = 2
    BookTick = 3
    Trade = 4
    AggTrade = 5
    Kline = 6
    AvgPrice = 7
    Depth = 8


def get_stream_type(stream_str_raw: str) -> StreamType:
    start: int = stream_str_raw.find('@')
    if -1 == start:
        return StreamType.Unknown
    stream_type: str = stream_str_raw[start + 1:]

    if 'ticker' == stream_type:
        return StreamType.Tick
    elif 'miniTicker' == stream_type:
        return StreamType.MiniTicker
    elif 'bookTicker' == stream_type:
        return StreamType.BookTick
    elif 'trade' == stream_type:
        return StreamType.Trade
    elif 'aggTrade' == stream_type:
        return StreamType.AggTrade
    elif 'kline' == stream_type:
        return StreamType.Kline
    elif 'depth' == stream_type:
        return StreamType.Depth
    elif 'avgPrice' == stream_type:
        return StreamType.AvgPrice


class CursorContext(object):

    def __init__(self,
                 connection: sqlite3.Connection,
                 commit: bool = False) -> None:
        self.connection: sqlite3.Connection = connection
        self.cursor: Cursor = self.connection.cursor()
        self.commit: bool = commit

    def __enter__(self) -> Cursor:
        return self.cursor

    def __exit__(self,
                 exc_type,
                 exc_val,
                 exc_tb) -> None:
        if self.commit:
            self.connection.commit()
        self.cursor.close()


class DatabaseWorker(object):

    @staticmethod
    def create_trades_table(connection: sqlite3.Connection):
        with CursorContext(connection) as cursor:
            cursor.execute('''CREATE TABLE IF NOT EXISTS trades (
                    time INT NOT NULL,
                    symbol TEXT NOT NULL,
                    trade_id INT NOT NULL,
                    price TEXT NOT NULL,
                    quantity TEXT NOT NULL,
                    trade_time TEXT NOT NULL,
                    is_buyer TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                    );''')

    @staticmethod
    def create_ticks_table(connection: sqlite3.Connection):
        with CursorContext(connection) as cursor:
            cursor.execute('''CREATE TABLE IF NOT EXISTS ticks (
                    event_type TEXT NOT NULL,
                    time INT NOT NULL,
                    symbol TEXT NOT NULL,
                    price_change TEXT NOT NULL,
                    price_change_percent TEXT NOT NULL,
                    weighted_average_price TEXT NOT NULL,
                    first_trade_price TEXT NOT NULL,
                    last_price TEXT NOT NULL,
                    last_quantity TEXT NOT NULL,
                    best_bid_price TEXT NOT NULL,
                    best_bid_quantity TEXT NOT NULL,
                    best_ask_price TEXT NOT NULL,
                    best_ask_quantity TEXT NOT NULL,
                    open_price TEXT NOT NULL,
                    high_price TEXT NOT NULL,
                    low_price TEXT NOT NULL,
                    total_traded_volume TEXT NOT NULL,
                    total_traded_quote_volume TEXT NOT NULL,
                    statistics_open_time TEXT NOT NULL,
                    statistics_close_time TEXT NOT NULL,
                    first_trade_id TEXT NOT NULL,
                    last_trade_id TEXT NOT NULL,
                    number_of_trades TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                    );''')

    @staticmethod
    def create_book_ticks_table(connection: sqlite3.Connection):
        with CursorContext(connection) as cursor:
            cursor.execute('''CREATE TABLE IF NOT EXISTS book_ticks (
                    update_id INT NOT NULL,
                    symbol TEXT NOT NULL,
                    best_bid_price TEXT NOT NULL,
                    best_bid_quantity TEXT NOT NULL,
                    best_ask_price TEXT NOT NULL,
                    best_ask_quantity TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                    );''')

    @staticmethod
    def insert_trade(connection: sqlite3.Connection,
                     trade: Trade):
        statement: str = (f"INSERT INTO trades (time,symbol,trade_id,price,quantity,trade_time,is_buyer,timestamp)"
                          f" VALUES ({trade.time},'{trade.symbol}',{trade.trade_id},'{trade.price}',"
                          f"'{trade.quantity}','{trade.trade_time}','{trade.is_buyer}','{trade.timestamp}');")
        with CursorContext(connection=connection, commit=True) as cursor:
            cursor.execute(statement)

    @staticmethod
    def insert_tick(connection: sqlite3.Connection,
                    tick: Tick):
        statement: str = (f"INSERT INTO ticks (event_type,time,symbol,price_change,price_change_percent,weighted_average_price,"
                          f"first_trade_price,last_price,last_quantity,best_bid_price,best_bid_quantity,best_ask_price,"
                          f"best_ask_quantity,open_price,high_price,low_price,total_traded_volume,total_traded_quote_volume,"
                          f"statistics_open_time,statistics_close_time,first_trade_id,last_trade_id,number_of_trades,timestamp)"
                          f" VALUES ('{tick.event_type}','{tick.time}','{tick.symbol}','{tick.price_change}','{tick.price_change_percent}',"
                          f"'{tick.weighted_average_price}','{tick.first_trade_price}','{tick.last_price}','{tick.last_quantity}',"
                          f"'{tick.best_bid_price}','{tick.best_bid_quantity}','{tick.best_ask_price}','{tick.best_ask_quantity}',"
                          f"'{tick.open_price}','{tick.high_price}','{tick.low_price}','{tick.total_traded_volume}',"
                          f"'{tick.total_traded_quote_volume}','{tick.statistics_open_time}','{tick.statistics_close_time}',"
                          f"'{tick.first_trade_id}','{tick.last_trade_id}','{tick.number_of_trades}','{tick.timestamp}');")
        with CursorContext(connection=connection, commit=True) as cursor:
            cursor.execute(statement)

    @staticmethod
    def insert_book_tick(connection: sqlite3.Connection,
                         book_tick: BookTick):
        statement: str = (f"INSERT INTO book_ticks (update_id,symbol,best_bid_price,best_bid_quantity,"
                          f"best_ask_price,best_ask_quantity,timestamp)"
                          f" VALUES ('{book_tick.update_id}','{book_tick.symbol}','{book_tick.best_bid_price}',"
                          f"'{book_tick.best_bid_quantity}','{book_tick.best_ask_price}',"
                          f"'{book_tick.best_ask_quantity}','{book_tick.timestamp}');")
        with CursorContext(connection=connection, commit=True) as cursor:
            cursor.execute(statement)


class BinanceDataCollector(object):
    MAX_PAYLOAD_SIZE: int = 1024
    BINANCE_TESTNET_HOST: str = 'wss://testnet.binance.vision'

    def __init__(self):
        self.symbol: str = 'BTCUSDT'
        self.db_storage_folder: str = f'{os.getcwd()}/../storage'

        self.message_queue: Queue = Queue()
        self.stop_event: Event = Event()
        self.even_processor: Process = Process(target=self.even_dumper)

        self.db_session: sqlite3.Connection = sqlite3.connect(f'{self.db_storage_folder}/binance_data_1.db')

        DatabaseWorker.create_trades_table(connection=self.db_session)
        DatabaseWorker.create_ticks_table(connection=self.db_session)
        DatabaseWorker.create_book_ticks_table(connection=self.db_session)

        self.web_socket = websocket.WebSocketApp(f'{self.BINANCE_TESTNET_HOST}/stream',
                                                 on_message=self.on_message,
                                                 on_error=self.on_error,
                                                 on_close=self.on_close,
                                                 on_open=self.on_open,
                                                 on_ping=self.on_ping)

        signal.signal(signal.SIGINT, self.signal_handler)

    # TODO: Implement
    def store_avg_price(self, event: Dict):
        avg_price: AvgPrice = AvgPrice(event)

    def store_trade(self, event: Dict):
        DatabaseWorker.insert_trade(connection=self.db_session,
                                    trade=Trade(event))

    def store_tick(self, event: Dict):
        DatabaseWorker.insert_tick(connection=self.db_session,
                                   tick=Tick(event))

    def store_book_tick(self, event: Dict):
        DatabaseWorker.insert_book_tick(connection=self.db_session,
                                        book_tick=BookTick(event))

    def store_event(self,
                    event: Dict):
        try:
            stream_name, data = event.get('stream'), event.get('data')
            if not stream_name or not data:
                return
            data['timestamp'] = str(datetime.datetime.now())
            stream_type: StreamType = get_stream_type(stream_name)
            if StreamType.Trade == stream_type:
                self.store_trade(data)
            elif StreamType.Tick == stream_type:
                self.store_tick(data)
            elif StreamType.BookTick == stream_type:
                self.store_book_tick(data)

        except Exception as exc:
            sys.stderr.write(str(exc))

    def even_dumper(self):
        while not self.stop_event.is_set():
            try:
                event: Dict = self.message_queue.get(timeout=0.25)
                self.store_event(event)
            except Empty:
                if self.stop_event.is_set():
                    break
                continue

    def on_message(self,
                   ws_socket: WebSocket,
                   message: Any):
        self.message_queue.put(json.loads(message))

    @staticmethod
    def on_error(ws_socket: WebSocket,
                 error: Any):
        sys.stderr.write(f"Error: {error}")

    @staticmethod
    def on_close(ws_socket: WebSocket,
                 close_status_code: Any,
                 close_msg: Any):
        print(f"WebSocket connection closed: {close_status_code} - {close_msg}")

    def on_open(self,
                ws_socket: WebSocket):
        subscribe_message: Dict = {
            "method": "SUBSCRIBE",
            "params": [
                # f"{self.symbol.lower()}@depth"
                # f"{self.symbol.lower()}@avgPrice"
                # f"{self.symbol.lower()}@miniTicker",
                f"{self.symbol.lower()}@bookTicker",
                f"{self.symbol.lower()}@ticker",
                # f"{self.symbol.lower()}@aggTrade",
                f"{self.symbol.lower()}@trade",
                # f"{self.symbol.lower()}@kline_1000ms",
            ],
            "id": 1
        }
        ws_socket.send(json.dumps(subscribe_message))

    @staticmethod
    def on_ping(ws_socket: WebSocket,
                message: Any):
        ws_socket.send(message, websocket.ABNF.OPCODE_PONG)

    def signal_handler(self, sig, frame):
        print('Stopping connector')
        self.stop_event.set()

    def start(self):
        self.even_processor.start()
        self.web_socket.run_forever()


if __name__ == '__main__':
    collector: BinanceDataCollector = BinanceDataCollector()
    collector.start()
