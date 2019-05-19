import datetime

import numpy as np

from binance_candle import BinanceCandle


class Binance24h1hHandler:

    def __init__(self):
        self.candle_list = []
        self.low_price = 0
        self.high_price = 0
        self.last_price = 0
        self.low_high_index = 0
        self.last_candle_positive = False
        self.last_close_candle_positive = False
        self.average_change = 0
        self.average_trades = 0
        self.last_candle_length = 0
        self.last_candle_trades = 0
        self.last_candle_change = 0

    def set_data(self, candle_list):
        for candle in candle_list:
            self.candle_list.append(BinanceCandle(candle[0], candle[1], candle[2], candle[3], candle[4], candle[5],
                                                  candle[6], candle[7], candle[8]))
        self.low_price = self.get_low_price()
        self.high_price = self.get_high_price()
        self.last_price = self.get_last_price()
        self.low_high_index = self.get_LH24h()
        self.last_candle_positive = self.get_last_candle_positive()
        self.last_close_candle_positive = self.get_last_close_candle_positive()
        self.average_change = self.get_average_change()
        self.average_trades = self.get_average_trades()
        self.last_candle_length = round(datetime.datetime.now().minute / 60, 2)
        self.last_candle_trades = self.candle_list[len(self.candle_list) - 1].trades
        self.last_candle_change = self.get_last_candle_change()

    def verify_data(self):
        now = datetime.datetime.now()
        if now.hour < 10:
            hour_value = "0" + str(now.hour)
        else:
            hour_value = str(now.hour)
        if now.month < 10:
            month_value = "0" + str(now.month)
        else:
            month_value = str(now.month)
        if now.day < 10:
            day_value = "0" + str(now.day)
        else:
            day_value = str(now.day)
        start_time = str(now.year) + "-" + month_value + "-" + day_value + " " + hour_value + ":00:00"
        next_hour = datetime.datetime.now() + datetime.timedelta(hours=1)
        if next_hour.hour < 10:
            hour_value = "0" + str(next_hour.hour)
        else:
            hour_value = str(next_hour.hour)
        if next_hour.month < 10:
            month_value = "0" + str(next_hour.month)
        else:
            month_value = str(now.month)
        if next_hour.day < 10:
            day_value = "0" + str(next_hour.day)
        else:
            day_value = str(next_hour.day)
        end_time = str(next_hour.year) + "-" + month_value + "-" + day_value + " " + hour_value + ":00:00"
        if 12 >= len(self.candle_list):
            return False
        elif str(self.candle_list[len(self.candle_list) - 1].open_time) != start_time:
            return False
        elif str(self.candle_list[len(self.candle_list) - 1].close_time) != end_time:
            return False
        return True

    def get_average_change(self):
        change = []
        for candle in self.candle_list:
            change.append(round((float(candle.close_price) / float(candle.open_price) - 1) * 100, 2))
        return np.mean(change)

    def get_average_trades(self):
        trades_list = []
        for candle in self.candle_list:
            trades_list.append(candle.trades)
        return np.mean(trades_list)

    def get_low_price(self):
        low = self.candle_list[0].low_price
        for candle in self.candle_list:
            if candle.low_price < low:
                low = candle.low_price
        return low

    def get_high_price(self):
        high = self.candle_list[0].high_price
        for candle in self.candle_list:
            if candle.high_price > high:
                high = candle.high_price
        return high

    def get_last_price(self):
        return self.candle_list[len(self.candle_list) - 1].close_price

    def get_LH24h(self):
        low = float(self.get_low_price())
        high = float(self.get_high_price())
        latest = float(self.get_last_price())
        range_diff = high - low
        one_point = range_diff / 100
        bottom_range = latest - low
        lh_index = bottom_range / one_point
        return round(lh_index, 1)

    def get_last_candle_positive(self):
        return self.candle_list[len(self.candle_list) - 1].is_positive()

    def get_last_close_candle_positive(self):
        return self.candle_list[len(self.candle_list) - 2].is_positive()

    def get_period_change(self):
        return round((float(self.candle_list[len(self.candle_list) - 1].close_price) / float(
            self.candle_list[0].open_price) - 1) * 100, 2)

    def get_last_candle_change(self):
        last_candle = self.candle_list[len(self.candle_list)-1]
        return round((float(last_candle.close_price) / float(last_candle.open_price) - 1) * 100, 2)
