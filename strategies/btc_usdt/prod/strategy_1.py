from binance_api.candle_24h_1h_handler import Candle24h1hHandler
from criterias.candles_24h_1h import Criterias24h1hCandles


class StrategyOneProd:

    def __init__(self, main_currency, second_currency):
        self.main_currency = main_currency
        self.second_currency = second_currency
        self.pair = self.main_currency + self.second_currency
        self.buy_target = 0
        self.sell_target = 0

    def setup(self, binance_api, order_handler):
        self.binance_api = binance_api
        self.handler = Candle24h1hHandler(self.binance_api)
        self.criterias = Criterias24h1hCandles(self.main_currency, self.second_currency, self.handler)
        self.order_handler = order_handler

    def set_data(self):
        self.handler.set_data(self.binance_api.get_24h_1h_candle(self.pair), self.binance_api.get_market_depth(self.pair))
        if not self.handler.verify_data():
            print("Data not valid for: " + self.pair)
            return

    def evaluate_criterias(self):
        # Return True(Buy) / False(Sell) / None Skip
        return None
