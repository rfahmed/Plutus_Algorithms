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
currentOrders = []  # this is to store current order IDs, when you buy, sell, close position, etc. update this list
# buy function:
    # should be easy to find in alpaca documentation under orders

# sell function:
    # should be easy to find in alpaca documentation under orders

# get position info function
    # should be easy to find in alpaca docs under positions

# cancel all orders function
    # this is under alpaca documentation under orders

# general liquidation function (close all positions)
    # exists in alpaca documentation under positions

# display all current positions function
    # also exists in positions portion of documentation
