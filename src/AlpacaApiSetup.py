import alpaca_trade_api as tradeapi
from config import alpaca_key, alpaca_secret, alpaca_base_url
# authentication and connection details
api_key = alpaca_key
api_secret = alpaca_secret
base_url = alpaca_base_url
# instantiate REST API
api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')
# obtain account information
account = api.get_account()
