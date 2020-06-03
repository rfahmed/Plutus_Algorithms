# some functions to convert alpha vantage data to a usable format for algo design
import pandas as pd
import AlpacaApiSetup as settings
import matplotlib.pyplot as plt

def data (Symbol, interval):
    df = pd.DataFrame(settings.api.alpha_vantage.historic_quotes(Symbol,
                                                                 adjusted=True,
                                                                 output_format='pandas',
                                                                 cadence=interval))
    return df
def formatforanalysis (df, type, length, Symbol):
    dfformat = df.iloc[0:length, type]
    dfformat.columns=[Symbol]
    return dfformat
def graph(Symbol, interval, time, type):
    print('***IMPORTANT - this graphs historical quotes up until the most recent interval. If you want to see '
          'interday quotes use that function instead***')

    df = pd.DataFrame(settings.api.alpha_vantage.historic_quotes(Symbol,
                                                                 adjusted=True,
                                                                 output_format='pandas',
                                                                 cadence=interval))
    titleconvert = ''
    if interval: 'daily'
    titleconvert = 'days'
    if interval: 'weekly'
    titleconvert= 'weeks'
    if interval: 'monthly'
    titleconvert= 'monthly'

    if type== 'open':
        graphedval = df['1. open']
        graphedval = graphedval.head(time)
        plt.plot(graphedval)
        plt.title('The Open Prices of {} over {} {}'.format(Symbol, time, titleconvert))
        plt.show()
    if type== 'high':
        graphedval = df['2. high']
        graphedval = graphedval.head(time)
        plt.plot(graphedval)
        plt.title('The High Prices of {} over {} {}'.format(Symbol, time, titleconvert))
        plt.show()
        pass
    if type== 'low':
        graphedval = df['3. low']
        graphedval = graphedval.head(time)
        plt.plot(graphedval)
        plt.title('The low Prices of {} over {} {}'.format(Symbol, time, titleconvert))
        plt.show()
        pass
    if type== 'close':
        graphedval = df['4. close']
        graphedval = graphedval.head(time)
        plt.plot(graphedval)
        plt.title('The close Prices of {} over {} {}'.format(Symbol, time, titleconvert))
        plt.show()
        pass
    if type== 'adjustedclose':
        graphedval = df['5.adjusted close']
        graphedval = graphedval.head(time)
        plt.plot(graphedval)
        plt.title('The Open Prices of {} over {} {}'.format(Symbol, time, titleconvert))
        plt.show()
        pass
    if type== 'volume':
        graphedval = df['6. volume']
        graphedval = graphedval.head(time)
        plt.plot(graphedval)
        plt.title('The High Prices of {} over {} {}'.format(Symbol, time, titleconvert))
        plt.show()
        pass
    if type== 'dividendamount':
        graphedval = df['7. dividend amount']
        graphedval = graphedval.head(time)
        plt.plot(graphedval)
        plt.title('The Open Prices of {} over {} {}'.format(Symbol, time, titleconvert))
        plt.show()
        pass
