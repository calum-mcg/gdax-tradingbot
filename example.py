import time
from model.TimedThread import *

#Custom settings
LOOP_DURATION = 10 #1 58.5 minute - computing time
MAX_LOOP_TIME = 8 * 60 * 60 #seconds
QUOTE_CURRENCY = "BTC"
BASE_CURRENCY = "EUR"

#Start thread
stopFlag = Event()
thread = TimedThread(stopFlag, LOOP_DURATION, QUOTE_CURRENCY, BASE_CURRENCY)
thread.start()

#Set max time to run
time.sleep(MAX_LOOP_TIME)
stopFlag.set()