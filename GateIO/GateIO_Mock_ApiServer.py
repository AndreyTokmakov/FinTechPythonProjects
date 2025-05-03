
import uvicorn
from fastapi import FastAPI, APIRouter

from common.Utilities import Utilities


class APIServer(object):

    RESOURCES_FOLDER: str = '/home/andtokm/Projects/M2/M2TestTools/GateIO/resources'

    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route(path="/api/v4/auth", methods=["GET"],
                                  endpoint=self.authenticate)
        self.router.add_api_route(path="/api/v4/wallet/total_balance", methods=["GET"],
                                  endpoint=self.get_wallet_total_balance)
        self.router.add_api_route(path="/api/v4/wallet/sub_account_balances", methods=["GET"],
                                  endpoint=self.get_wallet_sub_account_balances)
        self.router.add_api_route(path="/api/v4/wallet/sub_account_futures_balances", methods=["GET"],
                                  endpoint=self.get_wallet_sub_account_futures_balances)
        self.router.add_api_route(path="/api/v4/wallet/sub_account_margin_balances", methods=["GET"],
                                  endpoint=self.get_wallet_sub_account_margin_balances)
        self.router.add_api_route(path="/api/v4/wallet/sub_account_cross_margin_balances", methods=["GET"],
                                  endpoint=self.get_wallet_sub_account_cross_margin_balances)
        self.router.add_api_route(path="/api/v4/spot/accounts", methods=["GET"],
                                  endpoint=self.get_spot_accounts)
        self.router.add_api_route(path="/api/v4/margin/accounts", methods=["GET"],
                                  endpoint=self.get_margin_accounts)

    def authenticate(self,
                   accountId: str):
        return { 'id': accountId, 'result': 'OK'}

    def get_wallet_total_balance(self,
                                 currency: str = None):
        return Utilities.read_json_file(f'{APIServer.RESOURCES_FOLDER}/wallet_total_balance.json')

    def get_wallet_sub_account_balances(self,
                                        sub_uid: str = None):
        return Utilities.read_json_file(f'{APIServer.RESOURCES_FOLDER}/wallet_sub_account_balances.json')

    def get_wallet_sub_account_margin_balances(self,
                                               sub_uid: str = None):
        return Utilities.read_json_file(f'{APIServer.RESOURCES_FOLDER}/wallet_sub_account_margin_balances.json')

    def get_wallet_sub_account_futures_balances(self,
                                                sub_uid: str = None,
                                                settle: str = None):
        return Utilities.read_json_file(f'{APIServer.RESOURCES_FOLDER}/wallet_sub_account_futures_balances.json')

    def get_wallet_sub_account_cross_margin_balances(self,
                                                     sub_uid: str = None):
        return Utilities.read_json_file(f'{APIServer.RESOURCES_FOLDER}/wallet_sub_account_cross_margin_balances.json')

    def get_spot_accounts(self,
                          currency: str = None):
        return Utilities.read_json_file(f'{APIServer.RESOURCES_FOLDER}/spot_accounts.json')

    def get_margin_accounts(self,
                            currency_pair: str = None):
        return Utilities.read_json_file(f'{APIServer.RESOURCES_FOLDER}/margin_accounts.json')


# GET /futures/{settle}/accounts  # https://www.gate.io/docs/developers/apiv4/#query-futures-account

if __name__ == '__main__':
    api: FastAPI = FastAPI()
    server = APIServer()
    api.include_router(server.router)
    uvicorn.run(api, host="0.0.0.0", port=50002, log_level="debug")

    # INFO:  Swagger | http://0.0.0.0:50002/docs
