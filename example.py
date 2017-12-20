import time
from threading import Event
from exchange.CoinBase import *
from model.functions import *
from model.loop import *

#Sandbox settings
API_KEY = '6338bdfc20260afd7c4b8bb19201d7f2'
API_SECRET = 'OR/8eTQitl0UVnsn3Wa/SW1f2yFfPq5kWwetgQ/kdJeaUXY6IA7pd1Wn+wZ9WOCJBzyb2ZgZHBuPDgW4hukwtA=='
API_PASS = '8o98x0le6d7'
#API_URL = 'https://api-public.sandbox.gdax.com/'
API_URL = 'https://api.gdax.com/'

#Custom settings
PRICECSVNAME = "price.csv"
TRANSACTIONSCSVNAME = "transactions.csv"
LOOP_DURATION = 60 #seconds
MAX_LOOP_TIME = 10.5 * 60 * 60 #seconds
QUOTE_CURRENCY = 'BTC'
BASE_CURRENCY = 'USD'

#Authenticate details
CoinBase = CoinbaseExchange(API_KEY, API_SECRET, API_PASS, API_URL)

#Create model
model = Model()

#Choose Product
product_id = CoinBase.getProductId(QUOTE_CURRENCY, BASE_CURRENCY)

#Define list of functions to be performed in timed Thread
#TODO: Build failsafe: x number of failed trades and stop
#TODO: Build in integrated stop loss orders

def functions():
    model.calculateEma(CoinBase, product_id)
    signal = model.calculateCrossover()
    if signal is not None:
        if signal['value'] == "buy":
            model.buy(product_id, CoinBase, BASE_CURRENCY)
        elif signal['value'] == "sell":
            model.sell(product_id,  CoinBase, QUOTE_CURRENCY)

#Run timed Thread with custom Event to stop Thread
stopFlag = Event()
thread = TimedThread(stopFlag, LOOP_DURATION, functions)
thread.start()
time.sleep(MAX_LOOP_TIME)
stopFlag.set()

#Log price and transactions to CSV
model.logPrice(PRICECSVNAME)
model.logTransactions(TRANSACTIONSCSVNAME)

#Plot graph
model.plotGraph()