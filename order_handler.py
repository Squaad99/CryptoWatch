import datetime

from database_connector import DatabaseConnector


class OrderHandler:

    def __init__(self, main_currency, second_currency, binance_api, strategy_id, run_id):
        self.main_currency = main_currency
        self.second_currency = second_currency
        self.binance_api = binance_api
        self.last_trade_timeout = datetime.datetime.now()
        self.database_connector = DatabaseConnector()
        self.strategy_id = strategy_id
        self.run_id = run_id
        self.own_main = True
        self.database_connector.insert_order(self.strategy_id, self.run_id, "BUY", self.main_currency,
                                                         self.second_currency,
                                                         self.binance_api.get_latest_price(
                                                             self.main_currency + self.second_currency),
                                                         datetime.datetime.now().replace(microsecond=0), False)

    def buy(self, production):
        current_trade = datetime.datetime.now()
        if current_trade > self.last_trade_timeout:
            if not self.own_main:
                print("Buying", self.main_currency, "Strategy:", self.strategy_id)
                self.last_trade_timeout = datetime.datetime.now() + datetime.timedelta(hours=1)
                if production:
                    print("Buy real")
                else:
                    self.database_connector.insert_order(self.strategy_id, self.run_id, "BUY", self.main_currency,
                                                         self.second_currency,
                                                         self.binance_api.get_latest_price(
                                                             self.main_currency + self.second_currency),
                                                         datetime.datetime.now().replace(microsecond=0), production)

    def sell(self, production):
        current_trade = datetime.datetime.now()
        if current_trade > self.last_trade_timeout:
            if self.own_main:
                print("Selling", self.main_currency, "for", self.second_currency, "Strategy:", self.strategy_id)
                self.last_trade_timeout = datetime.datetime.now() + datetime.timedelta(hours=1)
                if production:
                    print("Sell real")
                else:
                    self.database_connector.insert_order(self.strategy_id, self.run_id, "SELL", self.main_currency,
                                                         self.second_currency,
                                                         self.binance_api.get_latest_price(
                                                             self.main_currency + self.second_currency),
                                                         datetime.datetime.now().replace(microsecond=0), production)

