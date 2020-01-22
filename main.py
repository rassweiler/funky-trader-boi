import os
from msvcrt import getch
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import matplotlib.pyplot as plot

cashFunds = 1000
tradingMultiplier = 0.25
availableTradingFunds = cashFunds*tradingMultiplier
maximumStockPrice = int(availableTradingFunds/10)
print(availableTradingFunds)
print(maximumStockPrice)
period = 60
symbols = ['APHA.TO']
heldStocks = []
ts = TimeSeries(key=os.environ['AlphaKey'], output_format='pandas')
data, meta = ts.get_intraday(
    symbol='APHA.TO', interval='1min', outputsize='full')
ti = TechIndicators(key='EJPG3NQK4F3B67RR', output_format='pandas')
dataTi, metaTi = ti.get_sma(
    symbol='APHA.TO', interval='1min', time_period=period, series_type='close')
df1 = dataTi
df2 = data['4. close'].iloc[period-1::]
df = pd.concat([df1, df2], axis=1)
df.plot()
plot.show()

key = 0
print('Press escape to quit...')
while key != 27:
    key = ord(getch())


def Sell():
    pass


def UpdateSymbols():
    pass
