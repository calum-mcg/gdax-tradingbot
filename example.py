import time
from model.TimedThread import *

#Custom settings
LOOP_DURATION = 58.5 # 58.5 minute - computing time
MAX_LOOP_TIME = 8 * 60 * 60 #seconds
QUOTE_CURRENCY = "BTC"
BASE_CURRENCY = "EUR"
CSV_PRICE = 'price.csv'
CSV_TRANSACTIONS = 'transactions.csv'

#Start thread
stopFlag = Event()
thread = TimedThread(stopFlag, LOOP_DURATION, QUOTE_CURRENCY, BASE_CURRENCY, CSV_PRICE, CSV_TRANSACTIONS)
thread.start()

#Set max time to run
time.sleep(MAX_LOOP_TIME)
stopFlag.set()