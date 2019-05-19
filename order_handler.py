import datetime


class OrderHandler:

    def __init__(self, main_currency, second_currency, binance_api):
        self.main_currency = main_currency
        self.second_currency = second_currency
        self.binance_api = binance_api
        self.last_trade_timeout = datetime.datetime.now()

    def buy(self):
        current_trade = datetime.datetime.now()
        if current_trade > self.last_trade_timeout:
            print("Buying", self.main_currency)
            self.last_trade_timeout = datetime.datetime.now() + datetime.timedelta(hours=1)

    def sell(self):
        current_trade = datetime.datetime.now()
        if current_trade > self.last_trade_timeout:
            print("Selling", self.main_currency, "for", self.second_currency)
            self.last_trade_timeout = datetime.datetime.now() + datetime.timedelta(hours=1)

    def own_main(self):
        return True
