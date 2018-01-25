import time
from model.TimedThread import *

#Custom settings
LOOP_DURATION = 58.5 # Time period (in seconds)
MAX_LOOP_TIME = 8 * 60 * 60 # Max duration to run (in seconds)
QUOTE_CURRENCY = "BTC" # Cryptocurrency of choice
BASE_CURRENCY = "EUR" # Fiat currency of choice
CSV_PRICE = "price.csv" # Price CSV name
CSV_TRANSACTIONS = "transactions.csv" # Transaction CSV name

#Start thread
stopFlag = Event()
thread = TimedThread(stopFlag, LOOP_DURATION, QUOTE_CURRENCY, BASE_CURRENCY, CSV_PRICE, CSV_TRANSACTIONS)
thread.start()

#Set max time to run
time.sleep(MAX_LOOP_TIME)
stopFlag.set()