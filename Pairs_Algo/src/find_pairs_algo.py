import time
import numpy as np
import AlpacaApiSetup as settings
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import coint
import Analysis_TDA as tda
# note:
# this algorithm is soley for finding pairs not for trading if you want to go to the trading algo please visit
# pairs_algo.py

# algo starts here:
def compareSymbols(symb1,symb2):
    df1 = tda.histdata(Symbol='{}'.format(symb1),
                       periodType='day',
                       frequencyType='minute',
                       frequency='1',
                       period='2',
                       needExtendedHoursData='true')
    df2 = tda.histdata(Symbol='{}'.format(symb2),
                       periodType='day',
                       frequencyType='minute',
                       frequency='1',
                       period='2',
                       needExtendedHoursData='true')
    df1.plot()
    df2.plot()
    plt.title('{} vs {}'.format(symb1, symb2))
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend([symb1, symb2])
    plt.show()

    # graph their relationship+mean
    (df1 / df2).plot(figsize=(15, 7))
    plt.axhline((df1 / df2).mean(), color='red', linestyle='--')
    plt.xlabel('Time')
    plt.legend(['Price Ratio', 'Mean'])
    plt.show()
    print('the mean value is: {}'.format((df1 / df2).mean()))
    # compute the p-value of the cointegration test
    # will inform us as to whether the ratio between the 2 timeseries is stationary
    # around its mean
    score, pvalue, _ = coint(df1, df2)
    print('the p value is: {}'.format(pvalue))


def find_cointegrated_pairs(data):
    # compute the integration of the pair
    n = data.shape[1]
    score_matrix = np.zeros((n, n))
    pvalue_matrix = np.ones((n, n))
    keys = data.keys()
    pairs = []
    pvalueperpair = []
    counter = 0
    for i in range(n):
        #Commented out percent loading bar bc its broken rn
        #counter+=1
        #if(counter%5==0):
            #print("We are {}% done!".format(counter))
        for j in range(i + 1, n):
            S1 = data[keys[i]]
            S2 = data[keys[j]]
            result = coint(S1, S2)
            score = result[0]
            pvalue = result[1]
            score_matrix[i, j] = score
            pvalue_matrix[i, j] = pvalue
            if pvalue < 0.02:
                pairs.append((keys[i], keys[j]))
                pvalueperpair.append(pvalue)
    return score_matrix, pvalue_matrix, pairs, pvalueperpair
def closedata (symb):
    df = tda.histdata(Symbol='{}'.format(symb), periodType='year', frequencyType='daily', frequency='1',
                          endDate='1577854800000', startDate='1274328000000', needExtendedHoursData='false')
    return df
def corrolationValsandHeatmap(instrumentIds):
    # create the data set for cointegration calculations
    print(instrumentIds)
    pricearr = []
    for i in instrumentIds:
        print(i)
        time.sleep(0.3) #we do this so that we don't throw an error with the api call limit
        dftemp = closedata(i)
        pricearr.append(dftemp)
    print(tda.toremove)
    dsfinal = pd.concat(pricearr, axis=1)
    dsfinal.set_axis(instrumentIds, axis=1, inplace=True)
    data = dsfinal
    find_cointegrated_pairs(data)
    # Heatmap to show the p-values of the cointegration test
    # between each pair of stocks
    scores, pvalues, pairs, pvalueinpair = find_cointegrated_pairs(data)
    import seaborn
    m = [0, 0.2, 0.4, 0.6, 0.8, 1]
    seaborn.heatmap(pvalues, xticklabels=instrumentIds, yticklabels=instrumentIds, cmap='RdYlGn_r', mask=(pvalues >= 0.98))
    plt.show()
    #print p vals of returned pair matches
    pvalueinpairindex = np.argsort(pvalueinpair)[:20]
    for i in pvalueinpairindex:
        print('the pair is: {}'.format(pairs[i]))
        print('the p value for the above pair is: {}'.format(pvalueinpair[i]))


def readCSVdata(path):
    # read in csv file to create symbol data
    #path should be a directory to the csv file
    csvdata = pd.DataFrame(pd.read_csv(path, engine='python'))
    csvdata = csvdata.iloc[:,0]
    corrolationValsandHeatmap(instrumentIds=csvdata)

