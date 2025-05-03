from __future__ import print_function
import gate_api
from gate_api.exceptions import ApiException, GateApiException

from GateIO.signature import creds

# Defining the host is optional and defaults to https://api.gateio.ws/api/v4
# See configuration.py for a list of all supported configuration parameters.
# The client must configure the authentication and authorization parameters in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that satisfies your auth use case.

# Configure APIv4 key authorization
configuration = gate_api.Configuration(
    host = "https://api.gateio.ws/api/v4",
    key = creds.api_key,
    secret = creds.api_secret
)


def list_spot_accounts():
    api_client = gate_api.ApiClient(configuration)
    # Create an instance of the API class

    api_instance = gate_api.SpotApi(api_client)
    currency = 'BTC'  # str | Retrieve data of the specified currency (optional)

    try:
        # List spot accounts
        api_response = api_instance.list_spot_accounts(currency=currency)
        print(api_response)
    except GateApiException as ex:
        print("Gate api exception, label: %s, message: %s\n" % (ex.label, ex.message))
    except ApiException as e:
        print("Exception when calling SpotApi->list_spot_accounts: %s\n" % e)


def list_sub_account_balances():

    api_client = gate_api.ApiClient(configuration)
    # Create an instance of the API class
    api_instance = gate_api.WalletApi(api_client)
    sub_uid = '10003,10004'  # str | User ID of sub-account, you can query multiple records separated by `,`.
                     # If not specified, it will return the records of all sub accounts (optional)

    try:
        # Retrieve sub account balances
        api_response = api_instance.list_sub_account_balances(sub_uid=sub_uid)
        print(api_response)
    except GateApiException as ex:
        print("Gate api exception, label: %s, message: %s\n" % (ex.label, ex.message))
    except ApiException as e:
        print("Exception when calling WalletApi->list_sub_account_balances: %s\n" % e)




# https://github.com/gateio/gateapi-python/blob/master/docs/SpotApi.md#list_spot_accounts

'''
# https://www.gate.io/docs/developers/apiv4/#retrieve-user-s-total-balances


Retrieve user's total balances
This endpoint returns an approximate sum of exchanged amount from all currencies to input currency for each account.
The exchange rate and account balance could have been cached for at most 1 minute.
It is not recommended to use its result for any trading calculation.
For trading calculation, use the corresponding account query endpoint for each account type. For example:

    GET /spot/accounts to query spot account balance
    GET /margin/accounts to query margin account balance
    GET /futures/{settle}/accounts to query futures account balance
'''

if __name__ == '__main__':

    # list_spot_accounts()
    list_sub_account_balances()
