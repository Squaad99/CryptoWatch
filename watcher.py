import datetime
import time

from binance_api.api import BinanceApi
from binance_api.order_handler import OrderHandler
from database.database_connector import DatabaseConnector


class Watcher:

    def __init__(self, strategy, minute_interval, strategy_id, run_id, production=False):
        self.strategy = strategy
        self.minute_interval = minute_interval
        self.strategy_id = strategy_id
        self.run_id = run_id
        self.binance_api = BinanceApi()
        self.database_connector = DatabaseConnector()
        self.production = production
        self.strategy.setup(self.binance_api)
        self.order_handler = OrderHandler(self.strategy.main_currency, self.strategy.second_currency, strategy_id,
                                          run_id, self.production, self.binance_api, self.database_connector)

    def start(self):
        print("Starting watcher for:", self.strategy.main_currency, self.strategy.second_currency,
              datetime.datetime.now().replace(microsecond=0))
        self.strategy.set_data()
        while True:
            self.strategy.set_data()
            result = self.strategy.evaluate_criterias()

            if result:
                self.order_handler.buy(self.production)
            elif result:
                self.order_handler.sell(self.production)

            time.sleep(self.minute_interval * 60)
