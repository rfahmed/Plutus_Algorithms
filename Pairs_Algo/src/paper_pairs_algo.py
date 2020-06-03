import Analysis_TDA as analysis
import pandas as pd
import time
import datetime
import sched
import AlpacaApiSetup as alpaca


# set up websocket to constantly import data
# set up constant graph of z score

S1='GIS'
S2='KHC'
# TODO: repeat buys need to be eliminated
last_zscore = None
import threading
def timer():
  t = threading.Timer(60, timer)
  t.start()
  run_every_halfhour(t)


def run_every_halfhour(t):
    market_open = alpaca.is_market_open()
    if market_open==True:
        clk_id1 = time.CLOCK_REALTIME
        epoch_time = time.clock_gettime(clk_id1)
        human_time = datetime.datetime.fromtimestamp(epoch_time).strftime('%c')
        if int(human_time[14: 16]) == (30):
            print('EXECUTED AT: ', human_time)
            zscores(S1, S2)
        elif int(human_time[14: 16]) == (00):
            print('EXECUTED AT: ', human_time)
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
    zscore = zscore["Price"].tolist()
    current_zscore = zscore[len(zscore)-1]
    # global last_zscore
    # if current_zscore >1.0 and last_zscore >1.0:
    #     print('Passed over to prevent double buying')
    #     pass
    # if current_zscore<-1.0 and last_zscore<-1.0:
    #     print('Passed over to prevent double buying')
    #     pass
    # if current_zscore<0.5 and current_zscore>-0.5:
    #     print('Passed over to prevent double buying')
    #     pass
    # last_zscore=current_zscore
    print(current_zscore)
    if current_zscore>1.0:
        # we sell the ratio here:
        print('EXECUTING: Selling the ratio...')
        # When selling the ratio, sell S1 and buy S2
        # buy S2:
        alpaca.buy(S2, qty= 10)
        # sell S1:
        open_pos = alpaca.get_open_positions()
        for i in open_pos:
            if i==S2:
                alpaca.close_a_position(S1)
        alpaca.sell(S1, qty=10)
    if current_zscore<-1.0:
        # we buy the ratio here:
        print('EXECUTING: Buying the ratio...')
        # When buying the ratio, buy S1 and sell S2
        # buy S1:
        alpaca.buy(S1, qty= 10)
        # sell S2:
        open_pos = alpaca.get_open_positions()
        for i in open_pos:
            if i==S1:
                alpaca.close_a_position(S2)
        alpaca.sell(S2, qty=10)
    if (current_zscore > -0.5 and current_zscore <0.5):
        # here we liquidate
        print('liquidating')
        alpaca.close_all_positions()
# first we must buy an initial amount of each:

# now we can do the 30 min intervals:
timer()
