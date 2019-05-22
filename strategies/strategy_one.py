import datetime

from binance_24h_1h_candles import Binance24h1hHandler
from binance_api import BinanceApi


class StrategyOne:

    def __init__(self, main_currency, second_currency):
        self.main_currency = main_currency
        self.second_currency = second_currency
        self.binance_api = BinanceApi()
        self.candles_24h_1h = []
        self.binance_24h_1h_handler = Binance24h1hHandler()
        self.start_value = 2
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

    def criteria_one(self):
        # Last candle is positive +2/-2 or +1/-1 for first half hour
        if self.binance_24h_1h_handler.last_candle_positive:
            if self.time_now.minute > 29:
                return 2
            return 1
        else:
            if self.time_now.minute > 29:
                return -2
            return -1

    def criteria_two(self):
        # Last CLOSED candle is positive +2/-2
        if self.binance_24h_1h_handler.last_close_candle_positive:
            return 2
        else:
            return -2

    def criteria_three(self):
        # Low High index 0-10 4, 10-40 3 40-70 2, 70-100 1
        index = self.binance_24h_1h_handler.low_high_index
        if 0 <= index <= 10:
            return 4
        elif 10 <= index <= 40:
            return 3
        elif 40 <= index <= 70:
            return 2
        elif 70 <= index <= 100:
            return 1

    def criteria_four(self):
        # 24h period change +2/-2
        change = self.binance_24h_1h_handler.get_period_change()
        if change > 0:
            return 2
        return -2

    def criteria_five(self):
        # Trade average +2/-2
        average_divided = self.binance_24h_1h_handler.average_trades * self.binance_24h_1h_handler.last_candle_length
        if self.binance_24h_1h_handler.last_candle_trades > average_divided:
            return 2
        return -2

    def criteria_six(self):
        # Change average +2/-2
        if self.binance_24h_1h_handler.last_candle_change > self.binance_24h_1h_handler.average_change:
            return 2
        return -2

    def evaluate_criterias(self):
        points = []
        points.append(self.criteria_one())
        points.append(self.criteria_two())
        points.append(self.criteria_three())
        points.append(self.criteria_four())
        points.append(self.criteria_five())
        points.append(self.criteria_six())
        return sum(points)
