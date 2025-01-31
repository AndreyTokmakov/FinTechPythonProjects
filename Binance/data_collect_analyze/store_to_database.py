import json
import os
import sqlite3
from typing import Dict, List

from Binance.data_collect_analyze.BookTick import BookTick
from Binance.data_collect_analyze.Tick import Tick
from Binance.data_collect_analyze.Trade import Trade

data_store_folder: str = f'{os.getcwd()}/../streams/data'
db_storage_folder: str = f'{os.getcwd()}/../storage'


def create_trades_table(connection: sqlite3.Connection):
    cursor = connection.cursor()
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
    cursor.close()


def create_ticks_table(connection: sqlite3.Connection):
    cursor = connection.cursor()
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
    cursor.close()


def create_book_ticks_table(connection: sqlite3.Connection):
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS book_ticks (
            update_id INT NOT NULL,
            symbol TEXT NOT NULL,
            best_bid_price TEXT NOT NULL,
            best_bid_quantity TEXT NOT NULL,
            best_ask_price TEXT NOT NULL,
            best_ask_quantity TEXT NOT NULL,
            timestamp TEXT NOT NULL
            );''')
    cursor.close()


def insert_trade(connection: sqlite3.Connection, trade: Trade):
    statement: str = (f"INSERT INTO trades (time,symbol,trade_id,price,quantity,trade_time,is_buyer,timestamp)"
                      f" VALUES ({trade.time},'{trade.symbol}',{trade.trade_id},'{trade.price}',"
                      f"'{trade.quantity}','{trade.trade_time}','{trade.is_buyer}','{trade.timestamp}');")
    cursor = connection.cursor()
    cursor.execute(statement)
    connection.commit()
    cursor.close()


def process_trades_data(connection: sqlite3.Connection):
    trades: List[Trade] = []
    with open(f'{data_store_folder}/btcusdt_trade') as trades_file:
        for trade_str in trades_file:
            trades.append(Trade(json.loads(trade_str.replace('\n', ''))))

    for trade in trades:
        insert_trade(connection=connection, trade=trade)


def insert_tick(connection: sqlite3.Connection, tick: Tick):
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
    cursor = connection.cursor()
    cursor.execute(statement)
    connection.commit()
    cursor.close()


def process_ticker_data(connection: sqlite3.Connection):
    ticks: List[Tick] = []
    with open(f'{data_store_folder}/btcusdt_ticker') as ticker_file:
        for ticker_str in ticker_file:
            ticks.append(Tick(json.loads(ticker_str.replace('\n', ''))))

    for tick in ticks:
        insert_tick(connection=connection, tick=tick)


def insert_book_tick(connection: sqlite3.Connection, book_tick: BookTick):
    statement: str = (f"INSERT INTO book_ticks (update_id,symbol,best_bid_price,best_bid_quantity,"
                      f"best_ask_price,best_ask_quantity,timestamp)"
                      f" VALUES ('{book_tick.update_id}','{book_tick.symbol}','{book_tick.best_bid_price}',"
                      f"'{book_tick.best_bid_quantity}','{book_tick.best_ask_price}',"
                      f"'{book_tick.best_ask_quantity}','{book_tick.timestamp}');")
    cursor = connection.cursor()
    cursor.execute(statement)
    connection.commit()
    cursor.close()


def process_book_ticker_data(connection: sqlite3.Connection):
    book_ticks: List[BookTick] = []
    with open(f'{data_store_folder}/btcusdt_bookTicker') as book_ticker_file:
        for book_ticker_str in book_ticker_file:
            book_ticks.append(BookTick(json.loads(book_ticker_str.replace('\n', ''))))

    for book_ticker in book_ticks:
        insert_book_tick(connection=connection, book_tick=book_ticker)


if __name__ == '__main__':
    # process_trades_data()

    '''
    with sqlite3.connect(f'{db_storage_folder}/binance_data.db') as session:
        create_trades_table(connection=session)
        process_trades_data(connection=session)
    '''
    '''
    with sqlite3.connect(f'{db_storage_folder}/binance_data.db') as session:
        create_ticks_table(connection=session)
        process_ticker_data(connection=session)
    '''

    with sqlite3.connect(f'{db_storage_folder}/binance_data.db') as session:
        create_book_ticks_table(connection=session)
        process_book_ticker_data(connection=session)


