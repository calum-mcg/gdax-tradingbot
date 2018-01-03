import time
from threading import Event
from exchange.CoinBase import *
from model.functions import *
from model.loop import *
from config import *

#Custom settings
PRICECSVNAME = "price.csv"
TRANSACTIONSCSVNAME = "transactions.csv"
LOOP_DURATION = 59 #seconds
MAX_LOOP_TIME = 8 * 60 * 60 #seconds
QUOTE_CURRENCY = 'BTC'
BASE_CURRENCY = 'EUR'

#Authenticate details
CoinBase = CoinbaseExchange(API_KEY, API_SECRET, API_PASS, API_URL)

#Create model
model = Model()

#Choose Product
product_id = CoinBase.getProductId(QUOTE_CURRENCY, BASE_CURRENCY)

order = model.sell(product_id, CoinBase, QUOTE_CURRENCY)
print(order)
