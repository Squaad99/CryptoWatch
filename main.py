import time

from queue import Queue
import threading

from database.database_connector import DatabaseConnector
from strategies.strategy_template import StrategyTemplate
from watcher import Watcher

watcher_list = []
database_connector = DatabaseConnector()

last_run_dict = database_connector.get_last_run()
run_id = (last_run_dict[0][0] + 1)
database_connector.insert_run(run_id, "Start")


# Template
# watcher_list.append(Watcher(StrategyTemplate("BTC", "USDT"), 2, 3, run_id))
def setup_watchers():
    print("dd")


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
