import sys
import os
import time
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
if sys.platform[:3] == 'win':
    from msvcrt import getch
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plot

from wallet.wallet import Wallet
from stock.stock import Stock

period = 60
#data, meta = ts.get_intraday(
#    symbol='APHA.TO', interval='1min', outputsize='full')
#ti = TechIndicators(key=os.environ['AlphaKey'], output_format='pandas')
#dataTi, metaTi = ti.get_sma(
#    symbol='APHA.TO', interval='1min', time_period=period, series_type='close')
#df1 = dataTi
#df2 = data['4. close'].iloc[period-1::]
#df = pd.concat([df1, df2], axis=1)
#df.plot()
#plot.show()

key = 0
#while key != 27:
    #key = ord(getch())

def ParseSite(numberOfStocks=None,maximumStockPrice=0, minimumStockPrice=0):
    site = 'https://ca.finance.yahoo.com/most-active?offset=0&count=100'
    stocks = []
    tickers = []
    client = urlopen(site)
    html = client.read()
    client.close()
    soup = bs(html,'html.parser')
    stonks = soup.findAll('tr',{'class':'simpTblRow'})
    for stonk in stonks:
        if(numberOfStocks and len(stocks) >= numberOfStocks):
            break
        ticker = stonk.td.a.text.strip()
        price = float(stonk.find('td',{'aria-label':'Price (Intraday)'}).span.text)
        if(price > minimumStockPrice and price < maximumStockPrice and not ticker in tickers):
            stock = Stock(ticker,price)
            stocks.append(stock)
            tickers.append(ticker)
    return stocks

def Sell():
    pass

def Buy():
    pass

def UpdateSymbols():
    pass

def GetMAHour(ticker=None):
    if ticker:
        pass
    return None

def GetMADay(ticker=None):
    if ticker:
        ti = TechIndicators(key=os.environ['AlphaKey'], output_format='json')
        data, meta = ti.get_sma(symbol=ticker, interval='daily', time_period=480, series_type='close')
        return data
    return None

def GetMAWeek(ticker=None):
    if ticker:
        ti = TechIndicators(key=os.environ['AlphaKey'], output_format='json')
        try:
            data, meta = ti.get_sma(symbol=ticker, interval='weekly', time_period=480, series_type='close')
            return data
        except Exception as e:
            print(e)
            return {}
    return None

def IsOkToDrop(stock=None,wallet=None):
    if stock and wallet:
        if stock.IsDownTrend() and not wallet.HasStock(stock.ticker):
            print('Ok To Drop Stock: ', stock.ticker)
            return True
    return False

if __name__ == '__main__':
    wallet = Wallet(funds=1000,multiplier=0.25,stopLoss=0.8)
    wallet.Debug()
    stockList = None
    stocks = []
    run = True
    buy = True
    stocksChecked = False
    stocksRefreshed = False
    openTime = 9
    closeTime = 16
    ts = TimeSeries(key=os.environ['AlphaKey'], output_format='pandas')
    ti = TechIndicators(key=os.environ['AlphaKey'], output_format='pandas')
    while run:
        #check if market is open
        if ((time.localtime()[3] >= openTime and time.localtime()[3] <= closeTime) and time.localtime()[6]<5 and stocksChecked):
            print('...Monitoring Stocks...')
            #pull stock intraday for each stock
            for stock in stocks:
                dataI, metaI = ts.get_intraday(symbol=stock.ticker, interval='1min', outputsize='full')
                dataIp = dataI['4. close'].iloc[period-1::]
                dataT, metaT = ti.get_sma(symbol=stock.ticker, interval='1min', time_period=60, series_type='close')
                df = pd.concat([dataIp, dataT], axis=1)
                df.plot()
            plot.show()
        #Market closed, collect daily and weekly intra
        if(stocksChecked == False):
            print('...Collecting Weekly SMA...')
            #Check stocks for bad movers
            for stock in stocks:
                print('...Collecting ',stock.ticker,'...')
                stock.SetMAWeek(GetMAWeek(stock.ticker))
            
            #Remove bad movers
            print('...Removing bad movers...')
            tempList = [stock for stock in stocks if not IsOkToDrop(stock, wallet)]
            stocks = tempList
            
            #Fill stock list up to 5
            if len(stocks) < 5:
                print('...Repopulating stock list...')
                if not stocksRefreshed:
                    print('...Refreshing stock options...')
                    stockList = ParseSite(maximumStockPrice=wallet.maximumStockPrice,minimumStockPrice=0.5)
                    stocksRefreshed = True
                needed = 5 - len(stocks)
                tempList = stockList[:needed]
                stockList = stockList[needed:]
                print('Number Of Stock Options Left: ',len(stockList))
                stocks = stocks + tempList
            else:
                stocksChecked = True
                    

        #Clear checks
        if((time.localtime()[3] == 23)):
            print('...Time to check stocks...')
            stocksChecked = False
            stocksRefreshed = False
        
        #sleep a minute
        print('...Wait 60s...')
        time.sleep(60)