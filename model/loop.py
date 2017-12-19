from threading import Thread
from exchange.CoinBase import *
from model.functions import *

class TimedThread(Thread):
    def __init__(self, event, wait_time, tasks):
        Thread.__init__(self)
        self.stopped = event
        self.wait_time = wait_time
        self.tasks = tasks

    def run(self):
        while not self.stopped.wait(self.wait_time):
            #Run function every loop unless stopped
            self.tasks()
