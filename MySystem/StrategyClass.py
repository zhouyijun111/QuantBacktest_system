# --- NDayReversalStrategy Class ---
import backtrader as bt 

class NDayReversalStrategy(bt.Strategy):
    params = (('n', 5), ('threshold', 0.05),)

    def __init__(self):
        self.order = None
        self.cum_return = bt.indicators.PercentChange(self.data.close, period=self.params.n)

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.data.datetime.date(0)
        print(f'{dt.isoformat()} {txt}')  # Print date and log message

    def next(self):
        if self.order:
            return

        if not self.position:
            if self.cum_return[0] < -self.params.threshold:
                self.order = self.buy()
        else:
            if self.cum_return[0] > self.params.threshold:
                self.order = self.sell()
        if self.cum_return[0] < -self.params.threshold:
            if not self.position:  # Check if we are in the market
                self.buy()
                self.log('BUY CREATE, %.2f' % self.data.close[0])

        elif self.cum_return[0] > self.params.threshold:
            if self.position:  # Check if we are in the market
                self.sell()
                self.log('SELL CREATE, %.2f' % self.data.close[0])