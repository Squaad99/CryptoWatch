import time

from queue import Queue
import threading

from database.database_connector import DatabaseConnector
from strategies.btc_usdt.strategy_1 import StrategyOne
from strategies.btc_usdt.strategy_2 import StrategyTwo
from strategies.btc_usdt.strategy_3 import StrategyThree
from strategies.btc_usdt.strategy_4 import StrategyFour
from strategies.btc_usdt.strategy_5 import StrategyFive
from watcher import Watcher

watcher_list = []
database_connector = DatabaseConnector()

last_run_dict = database_connector.get_last_run()
run_id = (last_run_dict[0][0] + 1)
database_connector.insert_run(run_id, "Start")


# Template
# watcher_list.append(Watcher(StrategyTemplate("BTC", "USDT"), 2, 3, run_id))


def setup_watchers():
    watcher_list.append(Watcher(StrategyOne("BTC", "USDT"), 5, 1, run_id))
    watcher_list.append(Watcher(StrategyTwo("BTC", "USDT"), 5, 2, run_id))
    watcher_list.append(Watcher(StrategyThree("BTC", "USDT"), 5, 3, run_id))
    watcher_list.append(Watcher(StrategyFour("BTC", "USDT"), 5, 4, run_id))
    watcher_list.append(Watcher(StrategyFive("BTC", "USDT"), 5, 5, run_id))

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
