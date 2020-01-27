import datetime

class Stock(object):
    def __init__(self, ticker=None, closingPrice=None):
        self.ticker=ticker
        self.closingPrice=closingPrice
        self.smaWeek={}
        self.smaDay={}
        self.smaMinute={}

    def SetMAMinute(self,intra=None):
        self.smaMinute = intra

    def SetMADay(self,intra=None):
        self.smaDay = intra

    def SetMAWeek(self,intra=None):
        self.smaWeek = intra
    
    def IsDownTrend(self):
        if bool(self.smaWeek):
            today = datetime.date.today()
            friday = today + datetime.timedelta((4-today.weekday())%7)
            key1 = friday-datetime.timedelta(7*2)
            key2 = friday-datetime.timedelta(7*5)
            key3 = friday-datetime.timedelta(7*3)
            key4 = friday-datetime.timedelta(7*6)
            if float(self.smaWeek[key1.strftime('%Y-%m-%d')]['SMA']) < float(self.smaWeek[key2.strftime('%Y-%m-%d')]['SMA']) and float(self.smaWeek[key3.strftime('%Y-%m-%d')]['SMA']) < float(self.smaWeek[key4.strftime('%Y-%m-%d')]['SMA']):
                return True
        return False

    def Debug(self):
        pass