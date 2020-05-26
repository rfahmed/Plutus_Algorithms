import json
import time
import urllib
import requests
from selenium import webdriver
import config
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.chrome.options import Options

# paper trading with pairs algo

# Authentication Step (to get access token):
def accesstoken():
    #going to tda website and logging in:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://auth.tdameritrade.com/auth?response_type=code&redirect_uri=http://localhost&client_id={}%40AMER.OAUTHAP'.format(config.client_id))
    payload = {'username':'irshadahmed2', 'password':config.tdpass}
    driver.find_element_by_id('username').send_keys(payload['username'])
    driver.find_element_by_id('password').send_keys(payload['password'])
    driver.find_element_by_id('accept').click()
    print('Logged in successfully...')
    findsec = driver.find_element_by_xpath('//*[@id="authform"]/main/details/summary').send_keys('\ue006')
    driver.find_element_by_name('init_secretquestion').send_keys(Keys.RETURN)
    secq = driver.find_element_by_xpath('//*[@id="authform"]/main/div[2]/p[2]').text
    if (secq == 'Question: In what city was your high school? (Enter full name of city only.)'):
        ans = config.tda_hs
    if (secq == 'Question: In what city was your mother born? (Enter full name of city only.)'):
        ans = config.tda_MomCity
    if (secq == 'Question: In what city were you married? (Enter full name of city only.)'):
        ans = config.tda_Married
    if (secq == 'Question: What was the name of the town your grandmother lived in? (Enter full name of town only.)'):
        ans = config.tda_Grandma
    driver.find_element_by_name('su_secretquestion').send_keys(ans)
    driver.find_element_by_id('accept').send_keys(Keys.RETURN)
    print('Answered security question...')
    driver.find_element_by_id('accept').send_keys(Keys.RETURN)
    url = driver.current_url
    parsed_url = urllib.parse.unquote(url.split('code=')[1])
    driver.quit()
    print('Got access token...')
    url_auth = r"https://api.tdameritrade.com/v1/oauth2/token"
    headers = {'Content-Type':"application/x-www-form-urlencoded"}
    payload = {'grant_type':'authorization_code',
               'access_type':'offline',
               'code': parsed_url,
               'client_id': config.client_id,
               'redirect_uri':'http://localhost'}
    auth_reply = requests.post(url_auth, headers=headers, data=payload)
    decoded=auth_reply.json()
    token=decoded['access_token']
    print('Successfully formatted access token...')
    print('Transferring to relevant endpoint now...')
    return token

# Quote Endpoint:
def quote (symbol):
    token = accesstoken()
    quote_url = "https://api.tdameritrade.com/v1/marketdata/{}/quotes".format(symbol)
    payload = {'apikey':config.client_id,
               'Authorization': token}
    quote_reply = requests.get(quote_url, params=payload)
    quotes = quote_reply.json()
    quote_json=json.dumps(quotes)
    pandas_json_quote = pd.read_json(quote_json)
    pandas_current_quote = pd.DataFrame(pandas_json_quote)
    lastprice = pandas_current_quote.loc['lastPrice']
    lastprice = lastprice.iloc[0]
    print('the most recent quote for {} is: '.format(symbol),lastprice)

quote('REGI')
