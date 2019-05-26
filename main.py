import time

from binance_api import BinanceApi
from database_connector import DatabaseConnector
from strategies.strategy_one import StrategyOne
from strategies.strategy_two import StrategyTwo
from watcher import Watcher
from queue import Queue
import threading

watcher_list = []
binance_api = BinanceApi()
database_connector = DatabaseConnector()

last_run_dict = database_connector.get_last_run()
run_id = (last_run_dict[0][0] + 1)
database_connector.insert_run(run_id, "Start")


def setup_watchers():
    watcher_list.append(Watcher("BTC", "USDT", 5, binance_api, database_connector, 1, run_id, StrategyOne("BTC", "USDT")))
    watcher_list.append(Watcher("BTC", "USDT", 3, binance_api, database_connector, 2, run_id, StrategyTwo("BTC", "USDT", binance_api)))


index = -1


def start_watchers():

    def watch_thread():
        global index
        index += 1
        while True:
            watcher_list[index].start()

    q = Queue()

    for x in range(len(watcher_list)):
        t = threading.Thread(target=watch_thread)
        t.daemon = True
        t.start()
        time.sleep(1)

    for worker in range(len(watcher_list)):
        q.put(worker)

    q.join()


def run():
    setup_watchers()
    start_watchers()


run()
