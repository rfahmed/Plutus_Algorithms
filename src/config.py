import os
#config for tda
client_id = os.environ.get('TD_CLIENT_ID')
tdpass = os.environ.get('TD_PASS')
tdaccountnum = os.environ.get('TD_ACCOUNT_NUM')
tda_hs = os.environ.get('TD_Q_HS_CITY')
tda_MomCity = os.environ.get('TD_Q_MOM_CITY')
tda_Married = os.environ.get('TD_Q_MARRIED_CITY')
tda_Grandma = os.environ.get('TD_Q_GRANDMA_CITY')

#config for alpaca
alpaca_key = os.environ.get('ALPACA_KEY')
alpaca_secret = os.environ.get('ALPACA_SECRET')
alpaca_base_url = os.environ.get('ALPACA_URL')
