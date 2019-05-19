from binance_api import BinanceApi
from watcher import Watcher
from queue import Queue
import threading

watcher_list = []
binance_api = BinanceApi()


def setup_watchers():
    watcher_list.append(Watcher("BTC", "USDT", 5, binance_api, 1))


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

    for worker in range(len(watcher_list)):
        q.put(worker)

    q.join()


def run():
    setup_watchers()
    start_watchers()


run()
