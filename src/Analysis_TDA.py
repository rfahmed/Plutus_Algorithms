# some functions to convert TDA data to a usable format for algo design

import urllib
import requests
import dateutil.parser
from datetime import datetime
import datetime
from selenium import webdriver
import config
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.chrome.options import Options
import json
from websocket import create_connection

toremove = []


def histdata(Symbol, periodType, frequencyType, frequency, endDate, startDate, needExtendedHoursData):
    # define our endpoint
    endpoint = r"https://api.tdameritrade.com/v1/marketdata/{}/pricehistory".format(Symbol)

    # define our payload
    payload = {'apikey': config.client_id,
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


def marketOpen(Market):
    endpoint = r"https://api.tdameritrade.com/v1/marketdata/{}/hours".format(Market)
    headers = {'Authorization': 'Bearer {}'.format(accesstoken())}
    # define params for endpoint
    params = {'date': str(datetime.datetime.today()).split()[0]}
    # make a request
    time_info = requests.get(url=endpoint, params=params, headers=headers)
    time_to_json = time_info.json()
    return (time_to_json['equity']['equity']['isOpen'])


def histdatahourly(Symbol, periodType, frequencyType, frequency, period, needExtendedHoursData):
    endpoint = r"https://api.tdameritrade.com/v1/marketdata/{}/pricehistory".format(Symbol)
    # define our payload
    payload = {'apikey': config.client_id,
               'periodType': periodType,
               'frequencyType': frequencyType,
               'frequency': frequency,
               'period': period,
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
    print(df)
    return df


def hourlyhistoricals(symbol):
    return histdata(Symbol=symbol, periodType='day', frequencyType='minute', frequency='30', endDate='1590586200000',
                    startDate='1588339800000', needExtendedHoursData='false')


# paper trading with pairs algo

# Authentication Step (to get access token):
def accesstoken():
    # going to tda website and logging in:
    ans = None
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(
        'https://auth.tdameritrade.com/auth?response_type=code&redirect_uri=http://localhost&client_id={}%40AMER.OAUTHAP'.format(
            config.client_id))  # throwing third party error
    payload = {'username': 'irshadahmed2', 'password': config.tdpass}
    driver.find_element_by_id('username').send_keys(payload['username'])
    driver.find_element_by_id('password').send_keys(payload['password'])
    driver.find_element_by_id('accept').click()
    # print('Logged in successfully...')
    driver.find_element_by_xpath('//*[@id="authform"]/main/details/summary').send_keys('\ue006')
    driver.find_element_by_name('init_secretquestion').send_keys(Keys.RETURN)
    secq = driver.find_element_by_xpath('//*[@id="authform"]/main/div[2]/p[2]').text
    if secq == 'Question: In what city was your high school? (Enter full name of city only.)':
        ans = config.tda_hs
    if secq == 'Question: In what city was your mother born? (Enter full name of city only.)':
        ans = config.tda_MomCity
    if secq == 'Question: In what city were you married? (Enter full name of city only.)':
        ans = config.tda_Married
    if secq == 'Question: What was the name of the town your grandmother lived in? (Enter full name of town only.)':
        ans = config.tda_Grandma
    driver.find_element_by_name('su_secretquestion').send_keys(ans)
    driver.find_element_by_id('accept').send_keys(Keys.RETURN)
    # print('Answered security question...')
    driver.find_element_by_id('accept').send_keys(Keys.RETURN)
    url = driver.current_url
    parsed_url = urllib.parse.unquote(url.split('code=')[1])
    driver.quit()
    # print('Got access token...')
    url_auth = r"https://api.tdameritrade.com/v1/oauth2/token"
    headers = {'Content-Type': "application/x-www-form-urlencoded"}
    payload = {'grant_type': 'authorization_code',
               'access_type': 'offline',
               'code': parsed_url,
               'client_id': config.client_id,
               'redirect_uri': 'http://localhost'}
    auth_reply = requests.post(url_auth, headers=headers, data=payload)
    decoded = auth_reply.json()
    token = decoded['access_token']
    # print('Successfully formatted access token...')
    # print('Transferring to relevant endpoint now...')
    return token


# #tried to make access tokens last longer
# access_token = 'nothing here'
# counter = 0
# def refreshtoken():
#     global access_token
#     global counter
#     counter += 1
#     if counter %5==0:
#         access_token = accesstoken()
#         print(access_token)
#     else:
#         print(counter)
#         print(access_token)
#         pass


# Quote Endpoint:
def quote(symbol):
    token = accesstoken()
    quote_url = "https://api.tdameritrade.com/v1/marketdata/{}/quotes".format(symbol)
    headers = {'Authorization': 'Bearer {}'.format(accesstoken())}
    payload = {'apikey': config.client_id}
    quote_reply = requests.get(quote_url, headers=headers, data=payload)
    quotes = quote_reply.json()
    quote_json = json.dumps(quotes)
    pandas_json_quote = pd.read_json(quote_json)
    pandas_current_quote = pd.DataFrame(pandas_json_quote)
    lastprice = pandas_current_quote.loc['lastPrice']
    lastprice = lastprice.iloc[0]
    print('the most recent quote for {} is: '.format(symbol), lastprice)
    return lastprice


# next two are for websocket attempt (ended up not needing it though)
def unix_time_millis(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000.0


def getlogininfo():
    # need to access user info and preferances > get user principles endpoint
    access_token = accesstoken()
    # define our endpoint
    endpoint = 'https://api.tdameritrade.com/v1/userprincipals'
    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    # define params for endpoint
    params = {'fields': 'streamerSubscriptionKeys,streamerConnectionInfo'}
    # make a request
    stream_info = requests.get(url=endpoint, params=params, headers=headers)
    stream_info_response = stream_info.json()
    # define info we need
    tokenTimeStamp = stream_info_response['streamerInfo']['tokenTimestamp']
    date = dateutil.parser.parse(tokenTimeStamp, ignoretz=True)
    tokenTimeStampAsMs = unix_time_millis(date)
    credentials = {'userid': stream_info_response['accounts'][0]['accountId'],
                   'token': stream_info_response['streamerInfo']['token'],
                   'company': stream_info_response['accounts'][0]['company'],
                   'segments': stream_info_response['accounts'][0]['segment'],
                   'cddomain': stream_info_response['accounts'][0]['accountCdDomainId'],
                   'usergroup': stream_info_response['streamerInfo']['userGroup'],
                   'accesslevel': stream_info_response['streamerInfo']['accessLevel'],
                   'authorized': "Y",
                   'timestamp': int(tokenTimeStampAsMs),
                   'appid': stream_info_response['streamerInfo']['appId'],
                   'acl': stream_info_response['streamerInfo']['acl']}
    from urllib.parse import urlparse
    login_request = {"requests": [{
        "service": "ADMIN",
        "requestid": "1",
        "command": "LOGIN",
        "account": stream_info_response['accounts'][0]['accountId'],
        "source": stream_info_response['streamerInfo']['appId'],
        "parameters": {"token": stream_info_response['streamerInfo']['token'],
                       "version": "1.0",
                       "credential": urllib.parse.urlencode(credentials)}}]}
    data_request = {"requests": [{
        "service": "QUOTE",
        "requestid": "1",
        "command": "SUBS",
        "account": stream_info_response['accounts'][0]['accountId'],
        "source": access_token,
        "parameters": {
            "keys": "AAPL,MSFT",
            "fields": "0,1,2,3,4,5,6,7,8"
        }}]}
    login_encoded = json.dumps(login_request)
    data_encoded = json.dumps(data_request)
    uri = "wss://" + stream_info_response['streamerInfo']['streamerSocketUrl'] + "/ws"
    ws = create_connection(uri)
    ws.send(login_encoded)
    ws.send(data_encoded)
    result = ws.recv()
    print(result)
    ws.close()
