import Analysis_TDA as analysis
import pandas as pd
import time
import datetime
import sched
import AlpacaApiSetup as alpaca


# set up websocket to constantly import data
# set up constant graph of z score

S1='MSFT'
S2='TSLA'
# TODO: repeat buys need to be eliminated
# TODO:
import threading
def timer():
  t = threading.Timer(60, timer)
  t.start()
  run_every_halfhour(t)


def run_every_halfhour(t):
    market_open = analysis.marketOpen('EQUITY')
    if market_open==True:
    clk_id1 = time.CLOCK_REALTIME
    epoch_time = time.clock_gettime(clk_id1)
    human_time = datetime.datetime.fromtimestamp(epoch_time).strftime('%c')
    if int(human_time[14: 16]) == (30):
        zscores(S1, S2)
    elif int(human_time[14: 16]) == (00):
        zscores(S1, S2)

def zscores(S1, S2):
    S1list = analysis.hourlyhistoricals(S1)
    S2list = analysis.hourlyhistoricals(S2)
    minofboth = (min(len(S1list), len(S2list)))
    ratios = []
    for i in range(minofboth):
        ratios.append(S1list[i] / S2list[i])
    S1current = analysis.quote(S1)
    S2current = analysis.quote(S2)
    CurrentRatio = S1current / S2current
    ratios.append(CurrentRatio)
    ratios = pd.DataFrame(ratios, columns=['Price'])
    ma1 = ratios.rolling(window=5,
                         center=False).mean()
    ma2 = ratios.rolling(window=60,
                         center=False).mean()
    std = ratios.rolling(window=60,
                         center=False).std()
    zscore = (ma1 - ma2) / std
    checkbuysell(zscore)
    return zscore
def checkbuysell (zscore):
    print('updated z score chart')
    print(zscore.iloc[len(zscore)-1])

timer()
#run_every_halfhour()
# buy sell signals
