import datetime

import mysql.connector


class DatabaseConnector:

    def __init__(self):
        self.database = mysql.connector.connect(
            host='35.228.9.187',
            database='crypto_watch_db',
            user='henrik',
            password='1234')
        self.cursor = self.database.cursor()

    def insert_order(self, strategy_id, run_id, order_type, main_currency, second_currency, price, date, prod=False):
        sql = "INSERT INTO crypto_order (trade_strategy, run_id, production, order_type, main_currency, second_currency, price, date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (strategy_id, run_id, prod, order_type, main_currency, second_currency, price, date)
        self.cursor.execute(sql, val)
        self.database.commit()

    def insert_run(self, id, type):
        sql = "INSERT INTO runs (id, type, date) VALUES (%s, %s, %s)"
        val = (id, type, datetime.datetime.now().replace(microsecond=0))
        self.cursor.execute(sql, val)
        self.database.commit()

    def setup_tables(self):
        self.cursor.execute(
            "CREATE TABLE crypto_order ("
            "id int AUTO_INCREMENT PRIMARY KEY,"
            "trade_strategy int, "  # Strategy Id
            "run_id int, "  # Run Id
            "production varchar(255), "  # True / False
            "order_type varchar(255), "  # Sell / Buy
            "main_currency varchar(255), "
            "second_currency varchar(255), "
            "price varchar(255), "
            "date varchar(255))"
        )

    def setup_run_table(self):
        self.cursor.execute(
            "CREATE TABLE runs ("
            "id int,"
            "type varchar(255), "
            "date varchar(255))"
        )

    def get_last_run(self):
        sql = "select *from runs ORDER BY Id DESC LIMIT 1"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_all_runs(self):
        sql = "select * from runs"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_order_history(self):
        sql = "select * from crypto_order"
        self.cursor.execute(sql)
        return self.cursor.fetchall()
