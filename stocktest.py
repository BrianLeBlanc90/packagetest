import pandas as pd
import urllib
import datetime as dt
import matplotlib.pyplot as plt

def yahoo_intraday(ticker = 'USDGBP', date_range = '15d', currency = True, freq = 'Default'):
    # freq = '5m', '10m', '15m', '30m'
    if currency == True:
        tick = ticker+'%3DX'
    url1 = 'http://chartapi.finance.yahoo.com/instrument/1/'+tick
    url2 = '/chartdata;type=quote;range='+date_range+'/csv/'
    url = url1 + url2
    response = urllib.request.urlopen(url)
    data =  response.read().decode().split('\n')
    labels = ['Close', 'High', 'Low', 'Open', 'Volume','Ticker']
    x = 0
    for x in range(len(data)):
        if data[x].split(':')[0] == 'volume':
            index = x
        else:
            x += 1
    ts = [dt.datetime.fromtimestamp(float(data[x].split(',')[0])) for x in range(index+1,len(data)-1)]
    Close = [data[x].split(',')[1] for x in range(index+1,len(data)-1)]
    High = [data[x].split(',')[2] for x in range(index+1,len(data)-1)]
    Low = [data[x].split(',')[3] for x in range(index+1,len(data)-1)]
    Open = [data[x].split(',')[4] for x in range(index+1,len(data)-1)]
    Volume = [data[x].split(',')[5] for x in range(index+1,len(data)-1)]
    values = [Close,High,Low,Open,Volume,ticker]
    df = pd.DataFrame({labels[x]:values[x] for x in range(len(values))}, index = ts)
    if freq == 'Default':
        return df
    else:
        frequency = freq.split('m')[0] + 'T'
        df = df.asfreq(frequency, method = 'ffill')
        return df
        
# %%

USDGBP = yahoo_intraday(ticker = 'USDGBP', date_range = '15d', currency = True, freq = 'Default')

USDGBP['Close'].plot()