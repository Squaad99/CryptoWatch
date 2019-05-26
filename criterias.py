import datetime

from binance_24h_1h_candles import Binance24h1hHandler
from binance_api import BinanceApi


class Criterias:

    def __init__(self, main_currency, second_currency):
        self.main_currency = main_currency
        self.second_currency = second_currency
        self.binance_api = BinanceApi()
        self.candles_24h_1h = []
        self.binance_24h_1h_handler = Binance24h1hHandler()
        self.time_now = datetime.datetime.now()

    def set_data(self):
        pair = self.main_currency + self.second_currency
        print(pair)
        self.candles_24h_1h = self.binance_api.get_24h_1h_candle(pair)
        self.binance_24h_1h_handler.set_data(self.candles_24h_1h)
        if not self.binance_24h_1h_handler.verify_data():
            print("Data not valid for: " + pair)
            return
        self.time_now = datetime.datetime.now()
        print("Data set: " + pair)

    def criteria_1_1(self):
        # Last candle is positive +2/-2 or +1/-1 for first half hour
        if self.binance_24h_1h_handler.last_candle_positive:
            if self.time_now.minute > 29:
                return 2
            return 1
        else:
            if self.time_now.minute > 29:
                return -2
            return -1

    def criteria_1_2(self):
        # Last CLOSED candle is positive +2/-2
        if self.binance_24h_1h_handler.last_close_candle_positive:
            return 2
        else:
            return -2

    def criteria_2(self):
        # Low High index 0-10 4, 10-40 3 40-70 2, 70-100 1
        index = self.binance_24h_1h_handler.low_high_index
        if 0 <= index <= 20:
            return 2
        elif 20 <= index <= 50:
            return 1
        elif 50 <= index <= 80:
            return -1
        elif 80 <= index <= 100:
            return -2

    def criteria_3(self):
        # 24h period change +2/-2
        if self.binance_24h_1h_handler.get_period_change() > 0:
            return 2
        else:
            return -2

    def criteria_4_1(self):
        # Trade average +2/-2
        average_divided = self.binance_24h_1h_handler.average_trades * self.binance_24h_1h_handler.last_candle_length
        if self.binance_24h_1h_handler.last_candle_trades > average_divided:
            return 2
        return -2

    def criteria_4_2(self):
        # Change average +2/-2
        if self.binance_24h_1h_handler.last_candle_change > self.binance_24h_1h_handler.average_change:
            return 2
        return -2

