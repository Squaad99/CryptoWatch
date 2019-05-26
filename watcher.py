import datetime
import time

from order_handler import OrderHandler
from strategies.strategy_one import StrategyOne


class Watcher:

    def __init__(self, main_currency, second_currency, minute_interval, binance_api, database_connector, strategy_id, run_id,
                 strategy, production=False):
        self.main_currency = main_currency
        self.second_currency = second_currency
        self.minute_interval = minute_interval
        self.binance_api = binance_api
        self.database_connector = database_connector
        self.strategy_id = strategy_id
        self.run_id = run_id
        self.order_handler = OrderHandler(self.main_currency, self.second_currency, binance_api, strategy_id, run_id)
        self.strategy = strategy
        self.production = production

    def start(self):
        print(self.production)
        print("Starting watcher for:", self.main_currency, self.second_currency, datetime.datetime.now().replace(microsecond=0))
        while True:
            self.strategy.set_data()
            result = self.strategy.evaluate_criterias()
            if result > 0:
                self.order_handler.buy(self.production)
            elif result < 0:
                self.order_handler.sell(self.production)
            print("Points", result)
            print(datetime.datetime.now().replace(microsecond=0))
            time.sleep(self.minute_interval * 60)
