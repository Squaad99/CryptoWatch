import mysql.connector


class DatabaseConnector:

    def __init__(self):
        self.database = mysql.connector.connect(
            host='localhost',
            database='crypto_watch_db',
            user='root',
            password='1234')
        self.cursor = self.database.cursor()

    def insert_order(self, strategy_id, order_type, main_currency, second_currency, price, date, prod=False):
        sql = "INSERT INTO crypto_order (trade_strategy, production, order_type, main_currency, second_currency, price, date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (strategy_id, prod, order_type, main_currency, second_currency, price, date)
        self.cursor.execute(sql, val)
        self.database.commit()

    def setup_tables(self):
        self.cursor.execute(
            "CREATE TABLE crypto_order ("
            "id int AUTO_INCREMENT PRIMARY KEY,"
            "trade_strategy int, "  # Strategy Id
            "production varchar(255), "  # True / False
            "order_type varchar(255), "  # Sell / Buy
            "main_currency varchar(255), "
            "second_currency varchar(255), "
            "price varchar(255), "
            "date varchar(255))"
        )


connector = DatabaseConnector()
connector.insert_order(1, "BUY", "BTC", "USDT", "8112.206", "2019", False)

