import alpaca_trade_api as tradeapi
import pandas as pd
from config import alpaca_key, alpaca_secret, alpaca_base_url

# authentication and connection details
api_key = alpaca_key
api_secret = alpaca_secret
base_url = alpaca_base_url
# instantiate REST API
api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')
# obtain account information
account = api.get_account()

# buy
def buy(symbol, qty):
    api.submit_order(
        symbol=symbol,
        qty=qty,
        side='buy',
        type='market',
        time_in_force='day'
    )


# sell
def sell(symbol, qty):
    api.submit_order(
        symbol=symbol,
        qty=qty,
        side='sell',
        type='market',
        time_in_force='day'
    )


# check if market is open
def is_market_open():
    clock = api.get_clock()
    return clock.is_open
    # TODO: return boolean based on if it is open on the hour.


# get position info (symbol, quantity, market value, side, change today)
def display_position_info():
    portfolio = api.list_positions()
    sym = []
    qty = []
    mv = []
    side = []
    change = []
    for position in portfolio:
        sym.append(position.symbol)
        qty.append(position.qty)
        mv.append(position.market_value)
        side.append(position.side)
        change.append(position.change_today)
    data = {'Symbol': sym,
            'Quantity': qty,
            'Market Value': mv,
            'Side': side,
            '∆ Today': change}
    df = pd.DataFrame(data)
    print(df)


# get open positions
def get_open_positions():
    return api.list_positions()


# cancel all orders:
def cancel_all_orders():
    # list = api.list_orders()
    # print(' '.join(list))
    api.cancel_all_orders()

# close a position
def close_a_position(Symbol):
    api.close_position(symbol=Symbol)


# close all positions
def close_all_positions():
    # list = api.list_positions()
    # print(' '.join(list))
    api.close_all_positions()

cancel_all_orders()