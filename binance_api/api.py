from binance.client import Client


class BinanceApi:

    def __init__(self):
        self.api_key = ""
        self.secret_key = ""
        self.client = Client(self.api_key, self.secret_key)

    def get_24h_1h_candle(self, pair):
        return self.client.get_historical_klines(pair, Client.KLINE_INTERVAL_1HOUR, '1 day ago UTC')

    def get_latest_price(self, pair):
        ticker = self.client.get_ticker(symbol=pair)
        round_up_currencies = ['BTCUSDT']
        if pair in round_up_currencies:
            return round(float(ticker['lastPrice']), 3)
        return ticker['lastPrice']

    def get_market_depth(self, pair):
        return self.client.get_order_book(symbol=pair)

