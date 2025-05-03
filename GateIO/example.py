
from __future__ import print_function

import gate_api
from gate_api import ApiClient, EarnUniApi
from gate_api.exceptions import ApiException, GateApiException


'''
Live trading                                    : https://api.gateio.ws/api/v4
Futures TestNet trading                         : https://fx-api-testnet.gateio.ws/api/v4
Futures live trading alternative (futures only) : https://fx-api.gateio.ws/api/v4
'''



# Defining the host is optional and defaults to https://api.gateio.ws/api/v4
# See configuration.py for a list of all supported configuration parameters.
configuration = gate_api.Configuration(
    # host = "https://api.gateio.ws/api/v4"
    host = "https://fx-api-testnet.gateio.ws/api/v4"
)

api_client: ApiClient = gate_api.ApiClient(configuration)

# Create an instance of the API class
api_instance: EarnUniApi = gate_api.EarnUniApi(api_client)

def list_uni_currencies(api: EarnUniApi) -> None:
    try:
        # List currencies for lending
        api_response = api.list_uni_currencies()
        print(api_response)
    except GateApiException as ex:
        print("Gate api exception, label: %s, message: %s\n" % (ex.label, ex.message))
    except ApiException as e:
        print("Exception when calling EarnUniApi->list_uni_currencies: %s\n" % e)


# TODO: https://github.com/gateio/gateapi-python
# TODO: Exampl : https://github.com/gateio/gateapi-python/tree/master/example

if __name__ == '__main__':
    list_uni_currencies(api_instance)
    # list_uni_currencies(api_instance)

