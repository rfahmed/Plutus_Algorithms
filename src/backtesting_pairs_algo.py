import find_pairs_algo as pairs
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def zscore(series):
    #calculates zscore to aid in creating map of data
    return (series - series.mean()) / np.std(series)

def checkPairsWithGraph(symb1, symb2):
    S1 = pairs.closedata(symb1)
    S2 = pairs.closedata(symb2)
    score, pvalue, _ = pairs.coint(S1, S2)
    print(pvalue)
    ratios = S1 / S2
    zscore(ratios).plot()
    plt.axhline(zscore(ratios).mean())
    plt.axhline(1.0, color='red',linestyle='--')
    plt.axhline(-1.0, color='green',linestyle='--')
    plt.title('Buying schema for {} vs {}'.format(symb1,symb2))
    plt.show()

def set_train_and_test(symb1,symb2):
    ratios = pairs.closedata(symb1)/pairs.closedata(symb2)
    lenbenchmark = int((len(ratios))/2)
    print(lenbenchmark)
    train = ratios[:lenbenchmark]
    test = ratios[lenbenchmark:]
    ratios_mavg5 = train.rolling(window=5,
                                 center=False).mean()
    ratios_mavg60 = train.rolling(window=60,
                                  center=False).mean()
    std_60 = train.rolling(window=60,
                           center=False).std()
    zscore_60_5 = (ratios_mavg5 - ratios_mavg60) / std_60
    plt.figure(figsize=(15, 7))
    plt.plot(train.index, train.values)
    plt.plot(ratios_mavg5.index, ratios_mavg5.values)
    plt.plot(ratios_mavg60.index, ratios_mavg60.values)
    plt.legend(['Ratio', '5d Ratio MA', '60d Ratio MA'])
    plt.ylabel('Ratio')
    plt.title('{} and {} ratio and 5, 60 day MA'.format(symb1,symb2))
    plt.show()
    plt.figure(figsize=(15, 7))
    zscore_60_5.plot()
    plt.axhline(0, color='black')
    plt.axhline(1.0, color='red', linestyle='--')
    plt.axhline(-1.0, color='green', linestyle='--')
    plt.legend(['Rolling Ratio z-Score', 'Mean', '+1', '-1'])
    plt.title('Rolling z score buying schema for {} and {}'.format(symb1,symb2))
    plt.show()
    # Plot the ratios and buy and sell signals from z score
    plt.figure(figsize=(15, 7))
    train[60:].plot()
    buy = train.copy()
    sell = train.copy()
    buy[zscore_60_5 > -1] = 0
    sell[zscore_60_5 < 1] = 0
    buy[60:].plot(color='green', linestyle ='None', marker ='^')
    sell[60:].plot(color='red', linestyle ='None', marker ='^')
    x1, x2, y1, y2 = plt.axis()
    plt.axis((x1, x2, ratios.min(), ratios.max()))
    plt.legend(['Ratio', 'Buy Signal', 'Sell Signal'])
    plt.title('Buying schema for {} vs {}'.format(symb1,symb2))
    plt.show()
    # Plot the prices and buy and sell signals from z score
    plt.figure(figsize=(18, 9))
    S1 = pairs.closedata(symb1).iloc[:lenbenchmark]
    S2 = pairs.closedata(symb2).iloc[:lenbenchmark]
    S1[60:].plot(color='b')
    S2[60:].plot(color='c')
    buyR = 0 * S1.copy()
    sellR = 0 * S1.copy()
    # When buying the ratio, buy S1 and sell S2
    buyR[buy != 0] = S1[buy != 0]
    sellR[buy != 0] = S2[buy != 0]
    # When selling the ratio, sell S1 and buy S2
    buyR[sell != 0] = S2[sell != 0]
    sellR[sell != 0] = S1[sell != 0]
    buyR[60:].plot(color='g', linestyle='None', marker='^')
    sellR[60:].plot(color='r', linestyle='None', marker='^')
    x1, x2, y1, y2 = plt.axis()
    plt.axis((x1, x2, min(S1.min(), S2.min()), max(S1.max(), S2.max())))
    plt.legend([symb1, symb2, 'Buy Signal', 'Sell Signal'])
    plt.title('Final schema on initial charts for {} and {}'.format(symb1,symb2))
    plt.show()


# Trade using a simple strategy
def trade(S1, S2, window1, window2):
    # If window length is 0, algorithm doesn't make sense, so exit
    if (window1 == 0) or (window2 == 0):
        return 0

    # Compute rolling mean and rolling standard deviation
    ratios = S1 / S2
    ma1 = ratios.rolling(window=window1,
                         center=False).mean()
    ma2 = ratios.rolling(window=window2,
                         center=False).mean()
    std = ratios.rolling(window=window2,
                         center=False).std()
    zscore = (ma1 - ma2) / std

    # Simulate trading
    # Start with no money and no positions
    money = 0
    initialmoney=money
    countS1 = 0
    countS2 = 0
    for i in range(len(ratios)):
        # Sell short if the z-score is > 1
        if zscore[i] > 1:
            money += S1[i] - S2[i] * ratios[i]
            countS1 -= 1
            countS2 += ratios[i]
            print('Selling Ratio %s %s %s %s' % (money, ratios[i], countS1, countS2))
        # Buy long if the z-score is < 1
        elif zscore[i] < -1:
            money -= S1[i] - S2[i] * ratios[i]
            countS1 += 1
            countS2 -= ratios[i]
            print('Buying Ratio %s %s %s %s' % (money, ratios[i], countS1, countS2))
        # Clear positions if the z-score between -.5 and .5
        elif abs(zscore[i]) < 0.5:
            money += S1[i] * countS1 + S2[i] * countS2
            countS1 = 0
            countS2 = 0
            print('Exit pos %s %s %s %s' % (money, ratios[i], countS1, countS2))
    print("Profit is: {}".format(money-initialmoney))
    return money

def runtest(symb1, symb2, length):
    set_train_and_test(symb1, symb2)
    trade(pairs.closedata(symb1).iloc[:length], pairs.closedata(symb2).iloc[:length], 5, 60)
runtest('MSFT', 'ADBE', 90)