import sys
import os
import time
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from wallet.wallet import Wallet
from stock.stock import Stock

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
        ti = TechIndicators(key=os.environ['AlphaKey'], output_format='json')
        data, meta = ti.get_sma(symbol=ticker, interval='1min', time_period=60, series_type='close')
        return data
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
    stocksWeeklyChecked = False
    stocksHourlyChecked = False
    stocksRefreshed = False
    openTime = 9
    closeTime = 16
    while run:
        #check if market is open
        if ((time.localtime()[3] >= openTime and time.localtime()[3] <= closeTime) and time.localtime()[6]<5 and stocksWeeklyChecked and stocksHourlyChecked):
            print('...Monitoring Stocks...')
            #pull stock intraday for each stock
            ts = TimeSeries(key=os.environ['AlphaKey'], output_format='json')
            for stock in stocks:
                dataI, metaI = ts.get_intraday(symbol=stock.ticker, interval='1min', outputsize='full')
                stock.SetIntraDay(dataI)
                #list(my_dict)[0] #Dic is now insertion order in 3.7+

        #Find Stocks, Collect Weekly SMA, remove downers, collect hourly SMA
        if(not stocksWeeklyChecked):
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
                stocksWeeklyChecked = True
        #Get Hourly SMA trend for stocks        
        elif(not stocksHourlyChecked):
            print('...Collecting Hourly SMA...')
            error = False
            #Check stocks for bad movers
            for stock in stocks:
                print('...Collecting',stock.ticker,'...')
                try:
                    stock.SetMAHour(GetMAHour(stock.ticker))
                except Exception as e:
                    errror = True
                    print('!!!Unable to collect hourly SMA for',stock.ticker,'\r\n',e)
            if(not error):
                stocksHourlyChecked = True
                    

        #Clear checks
        if((time.localtime()[3] == 23 and time.localtime()[4] == 59)):
            print('...Time to check stocks...')
            stocksWeeklyChecked = False
            stocksWeeklyChecked = False
            stocksRefreshed = False
        
        #Check hourly SMA
        if((time.localtime()[4] == 0)):
            print('...Time to check hourly SMA...')
            stocksHourlyChecked = False
        
        #sleep a minute
        print('...Wait 60s...')
        time.sleep(60)