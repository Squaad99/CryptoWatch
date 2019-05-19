import datetime
import time

from order_handler import OrderHandler
from strategies.strategy_one import StrategyOne


class Watcher:

    def __init__(self, main_currency, second_currency, minute_interval, binance_api, strategy_id):
        self.main_currency = main_currency
        self.second_currency = second_currency
        self.minute_interval = minute_interval
        self.binance_api = binance_api
        self.strategy_id = strategy_id
        self.order_handler = OrderHandler(self.main_currency, self.second_currency, binance_api)
        self.strategy = StrategyOne(self.main_currency, self.second_currency)

    def start(self):
        print("Starting watcher for:", self.main_currency, self.second_currency, datetime.datetime.now().replace(microsecond=0))
        while True:
            self.strategy.set_data()
            result = self.strategy.evaluate_criterias()
            if result > 0:
                self.order_handler.buy()
            elif result < 0:
                self.order_handler.sell()
            print("Points", result)
            print(datetime.datetime.now().replace(microsecond=0))
            time.sleep(self.minute_interval * 60)



