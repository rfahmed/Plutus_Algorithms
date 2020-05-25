import time
import urllib
import requests
from selenium import webdriver
from config import client_id, tdpass, tdaccountnum
from selenium.webdriver.common.keys import Keys
# paper trading with pairs algo
method='GET'
url='https://auth.tdameritrade.com/auth?'
client_code = client_id +'@AMER.OAUTHAP'
driver = webdriver.Chrome()
driver.get('https://auth.tdameritrade.com/auth?response_type=code&redirect_uri=http://localhost&client_id={}%40AMER.OAUTHAP'.format(client_id))
payload = {'username':'irshadahmed2', 'password':tdpass}
driver.find_element_by_id('username').send_keys(payload['username'])
driver.find_element_by_id('password').send_keys(payload['password'])
driver.find_element_by_id('accept').click()
time.sleep(0.5)
findsec = driver.find_element_by_xpath('//*[@id="authform"]/main/details/summary').send_keys('\ue006')
driver.find_element_by_name('init_secretquestion').send_keys(Keys.RETURN)
time.sleep((0.5))
secq = driver.find_element_by_xpath('//*[@id="authform"]/main/div[2]/p[2]').text
if (secq == 'Question: In what city was your high school? (Enter full name of city only.)'):
    ans = 'hyderabad'
if (secq == 'Question: In what city was your mother born? (Enter full name of city only.)'):
    ans = 'varanasi'
if (secq == 'Question: In what city were you married? (Enter full name of city only.)'):
    ans = 'mahwah'
if (secq == 'Question: What was the name of the town your grandmother lived in? (Enter full name of town only.)'):
    ans = 'varanasi'
driver.find_element_by_name('su_secretquestion').send_keys(ans)
driver.find_element_by_id('accept').send_keys(Keys.RETURN)
time.sleep(0.5)
driver.find_element_by_id('accept').send_keys(Keys.RETURN)
time.sleep(0.5)
url = driver.current_url
parsed_url = urllib.parse.unquote(url.split('code=')[1])
driver.quit()

url_auth = r"https://api.tdameritrade.com/v1/oauth2/token"
headers = {'Content-Type':"application/x-www-form-urlencoded"}
payload = {'grant_type':'authorization_code',
           'access_type':'offline',
           'code': parsed_url,
           'client_id': client_id,
           'redirect_uri':'http://localhost'}
auth_reply = requests.post(url_auth, headers=headers, data=payload)
decoded=auth_reply.json()
token=decoded['access_token']
quote_url = "https://api.tdameritrade.com/v1/marketdata/{}/quotes".format('TSLA')
payload = {'apikey':client_id,
           'Authorization': token}
quote_reply = requests.get(quote_url, params=payload)
print(quote_reply.json())
