import Analysis_TDA as analysis
import pandas as pd
import AlpacaApiSetup as alpaca
#set up websocket to constantly import data
#set up constant graph of z score


def zscores (S1, S2):
    S1list = analysis.hourlyhistoricals(S1)
    S2list = analysis.hourlyhistoricals(S2)
    minofboth = (min(len(S1list), len(S2list)))
    ratios = []
    for i in range(minofboth):
        ratios.append(S1list[i]/S2list[i])
    S1current = analysis.quote(S1)
    S2current = analysis.quote(S2)
    CurrentRatio = S1current/S2current
    ratios.append(CurrentRatio)
    ratios = pd.DataFrame(ratios, columns=['Price'])
    ma1 = ratios.rolling(window=5,
                         center=False).mean()
    ma2 = ratios.rolling(window=60,
                         center=False).mean()
    std = ratios.rolling(window=60,
                         center=False).std()
    zscore = (ma1 - ma2) / std
    print('the list of z scores is: ', zscore)
zscores(S1='MSFT', S2='ADBE')
#buy sell signals
