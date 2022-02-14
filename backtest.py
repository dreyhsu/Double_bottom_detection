# data feeds
import datetime
import backtrader as bt
import backtrader.feeds as btfeeds
import math
import pandas as pd

class PandasData(bt.feed.DataBase):
    '''
    The ``dataname`` parameter inherited from ``feed.DataBase`` is the pandas
    DataFrame
    '''
    params = (
        # Possible values for datetime (must always be present)
        #  None : datetime is the "index" in the Pandas Dataframe
        #  -1 : autodetect position or case-wise equal name
        #  >= 0 : numeric index to the colum in the pandas dataframe
        #  string : column name (as index) in the pandas dataframe
        ('datetime', None),

        # Possible values below:
        #  None : column not present
        #  -1 : autodetect position or case-wise equal name
        #  >= 0 : numeric index to the colum in the pandas dataframe
        #  string : column name (as index) in the pandas dataframe
        ('open', -1),
        ('high', -1),
        ('low', -1),
        ('close', -1),
        ('volume', -1),
        ('openinterest', -1),
    )

# Create a Stratey
class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.dataopen = self.datas[0].open
        self.openinterest = self.datas[0].openinterest

    def next(self):
         # 帳戶沒有部位
        if not self.position:
            # 5ma往上穿越20ma
            if self.openinterest[0] > 0.5:
                # 印出買賣日期與價位
                self.log('BUY ' + ', Price: ' + str(self.dataopen[0]))
                # 使用開盤價買入標的
                self.buy(price=self.dataopen[0])
        # 5ma往下穿越20ma
        elif self.openinterest[0] < 0.25:
            # 印出買賣日期與價位
            self.log('SELL ' + ', Price: ' + str(self.dataopen[0]))
            # 使用開盤價賣出標的
            self.close(price=self.dataopen[0])

if __name__ == '__main__':
    dataframe = pd.read_csv('test.csv', delimiter=",", index_col="datetime", parse_dates= True)
    data = bt.feeds.PandasData(dataname=dataframe)
    # 初始化cerebro
    cerebro = bt.Cerebro()
    # feed data
    cerebro.adddata(data)
    # add strategy
    cerebro.addstrategy(TestStrategy)
    # run backtest
    cerebro.run()
    # plot diagram
    cerebro.plot()