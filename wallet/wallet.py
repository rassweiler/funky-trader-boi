class Wallet(object):
    def __init__(self, funds=0,multiplier=0.25,stopLoss=0.8):
        self.funds=funds
        self.multiplier=multiplier
        self.stopLoss=stopLoss
        self.availableTradingFunds = funds*multiplier
        self.maximumStockPrice = int(self.availableTradingFunds*0.015)
        self.heldStocks = []

    def BuyStock(self):
        pass

    def SellStock(self):
        pass

    def HasStock(self,ticker):
        if ticker and ticker in self.heldStocks:
            return True
        return False

    def Debug(self):
        print('Cash Funds: ',self.funds)
        print('Trading Funds: ',self.availableTradingFunds)
        print('Max Stock Price: ',self.maximumStockPrice)
        print('Held Stocks: ',self.heldStocks)