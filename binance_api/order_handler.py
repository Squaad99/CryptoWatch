import datetime


class OrderHandler:

    def __init__(self, main_currency, second_currency, strategy_id, run_id, production, binance_api, database_connector):
        self.main_currency = main_currency
        self.second_currency = second_currency
        self.strategy_id = strategy_id
        self.run_id = run_id
        self.production = production
        self.binance_api = binance_api
        self.database_connector = database_connector
        self.last_trade_time = datetime.datetime.now()
        self.own_main = False

    def buy(self):
        current_trade = datetime.datetime.now()
        if current_trade > self.last_trade_time:
            if not self.own_main:
                print("Buying", self.main_currency, "Strategy:", self.strategy_id)
                self.last_trade_time = datetime.datetime.now() + datetime.timedelta(hours=1)
                if self.production:
                    print("Buy real")
                else:
                    self.own_main = True
                    self.database_connector.insert_order(self.strategy_id, self.run_id, "BUY", self.main_currency,
                                                         self.second_currency,
                                                         self.binance_api.get_latest_price(
                                                             self.main_currency + self.second_currency),
                                                         datetime.datetime.now().replace(microsecond=0), self.production)

    def sell(self):
        current_trade = datetime.datetime.now()
        if current_trade > self.last_trade_time:
            if self.own_main:
                print("Selling", self.main_currency, "for", self.second_currency, "Strategy:", self.strategy_id)
                self.last_trade_time = datetime.datetime.now() + datetime.timedelta(hours=1)
                if self.production:
                    print("Sell real")
                else:
                    self.own_main = False
                    self.database_connector.insert_order(self.strategy_id, self.run_id, "SELL", self.main_currency,
                                                         self.second_currency,
                                                         self.binance_api.get_latest_price(
                                                             self.main_currency + self.second_currency),
                                                         datetime.datetime.now().replace(microsecond=0), self.production)
