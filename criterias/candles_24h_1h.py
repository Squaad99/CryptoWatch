import datetime

from calculator import Calculator


class Criterias24h1hCandles:

    def __init__(self, main_currency, second_currency, handler):
        self.main_currency = main_currency
        self.second_currency = second_currency
        self.handler = handler
        self.candles_24h_1h = []
        self.binance_24h_1h_handler = handler
        self.time_now = datetime.datetime.now()
        self.calculator = Calculator()

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

    def criteria_5_1(self):
        # Market depth in BTC highest divided by 20 1-5
        bid_percentage, ask_percentage = self.calculator.percentage_of_two_values(self.binance_24h_1h_handler.total_bids, self.binance_24h_1h_handler.total_asks)
        # More seller
        if bid_percentage < ask_percentage:
            return -ask_percentage / 20
        # More buyers
        elif bid_percentage > ask_percentage:
            return bid_percentage / 20
