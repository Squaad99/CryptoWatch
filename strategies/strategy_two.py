import datetime

from binance_24h_1h_candles import Binance24h1hHandler
from criterias import Criterias


class StrategyTwo:

    def __init__(self, main_currency, second_currency, binance_api):
        self.main_currency = main_currency
        self.second_currency = second_currency
        self.binance_api = binance_api
        self.candles_24h_1h = []
        self.binance_24h_1h_handler = Binance24h1hHandler()
        self.time_now = datetime.datetime.now()
        self.criterias = Criterias(self.main_currency, self.second_currency)

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

    def evaluate_criterias(self):
        points = []
        points.append(self.criterias.criteria_1_1())
        points.append(self.criterias.criteria_1_2())
        points.append(self.criterias.criteria_2())
        return sum(points)
