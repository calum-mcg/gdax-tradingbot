import time
from threading import Event
from exchange.CoinBase import *
from model.functions import *
from model.loop import *
from config import *

#Custom settings

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


order = model.buy(product_id, CoinBase, BASE_CURRENCY)
order_id = order['id']

while True:
	order_status = CoinBase.getOrderStatus(order_id)
	if order_status == "done":
		print("Buy fulfilled")
		break
	time.sleep(0.5)

order = model.sell(product_id, CoinBase, QUOTE_CURRENCY)
order_id = order['id']

while True:
	order_status = CoinBase.getOrderStatus(order_id)
	if order_status == "done":
		print("Sell fulfilled")
		break
	time.sleep(0.5)