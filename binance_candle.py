import datetime


class BinanceCandle:

    def __init__(self, open_time, open_price, high_price, low_price, close_price,
                 volume_price, close_time, asset_volume, trades):
        self.open_time = datetime.datetime.fromtimestamp(int(open_time)/1000)
        self.open_price = open_price
        self.high_price = high_price
        self.low_price = low_price
        self.close_price = close_price
        self.volume_price = volume_price
        self.close_time = datetime.datetime.fromtimestamp((int(close_time) + 1)/1000)
        self.asset_volume = asset_volume
        self.trades = trades

    def is_positive(self):
        if self.open_price < self.close_price:
            return True
        return False