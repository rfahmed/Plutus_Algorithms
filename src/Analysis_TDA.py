# some functions to convert TDA data to a usable format for algo design
import requests
import os
import pandas as pd
from config import client_id
import json
toremove = []
def histdata(Symbol, periodType, frequencyType, frequency, endDate, startDate, needExtendedHoursData):
    # define our endpoint
    endpoint = r"https://api.tdameritrade.com/v1/marketdata/{}/pricehistory".format(Symbol)

    # define our payload
    payload = {'apikey': client_id,
               'periodType': periodType,
               'frequencyType': frequencyType,
               'frequency': frequency,
               'endDate': endDate,
               'startDate': startDate,
               'needExtendedHoursData': needExtendedHoursData}
    # make a request
    content = requests.get(url=endpoint, params=payload)
    data = content.json()
    df = pd.DataFrame(data['candles'])
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)

    # print('Symbol is: {}'.format(Symbol))
    df = df.iloc[0:, 3]
    if len(df.index) < 251:
        toremove.append(Symbol)
    return df
