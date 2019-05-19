from binance.client import Client


class BinanceApi:

    def __init__(self):
        self.api_key = ""
        self.secret_key = ""
        self.client = Client(self.api_key, self.secret_key)

    def get_24h_1h_candle(self, pair):
        return self.client.get_historical_klines(pair, Client.KLINE_INTERVAL_1HOUR, "1 day ago UTC")
