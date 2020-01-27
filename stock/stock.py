import datetime

class Stock(object):
    def __init__(self, ticker=None, closingPrice=None):
        self.ticker=ticker
        self.closingPrice=closingPrice
        self.intraDay={}
        self.smaWeek={}
        self.smaDay={}
        self.smaHour={}

    def SetMAHour(self,intra=None):
        self.smaHour = intra

    def SetMADay(self,intra=None):
        self.smaDay = intra

    def SetMAWeek(self,intra=None):
        self.smaWeek = intra

    def SetIntraDay(self,intra=None):
        self.intraDay = intra
        print(self.intraDay)
    
    def IsDownTrend(self):
        if bool(self.smaWeek):
            today = datetime.date.today()
            friday = today + datetime.timedelta((4-today.weekday())%7)
            key1 = friday-datetime.timedelta(7*1)
            key2 = friday-datetime.timedelta(7*5)
            key3 = friday-datetime.timedelta(7*2)
            key4 = friday-datetime.timedelta(7*6)
            if float(self.smaWeek[key1.strftime('%Y-%m-%d')]['SMA']) < float(self.smaWeek[key2.strftime('%Y-%m-%d')]['SMA']) and float(self.smaWeek[key3.strftime('%Y-%m-%d')]['SMA']) < float(self.smaWeek[key4.strftime('%Y-%m-%d')]['SMA']):
                return True
        return False

    def Debug(self):
        pass