
from pybit.unified_trading import HTTP




if __name__ == '__main__':
    session: HTTP = HTTP(testnet=True,
                         api_key="XXXXX",
                         api_secret="XXXXX")
    print(session.get_wallet_balance( accountType="SPOT",coin="BTC", ))
