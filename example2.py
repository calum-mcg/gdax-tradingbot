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

#Test buy, check status and sell
order = model.buy(product_id, CoinBase, BASE_CURRENCY)
order_id = order['id']
print("ID: {}, Order: Buy, Status: {}".format(order_id, order['status']))

while True:
	order_status = CoinBase.getOrderStatus(order_id)
	if order_status == "done":
		print("Buy fulfilled at {}".format(order['price']))
		break
	time.sleep(0.5)

order = model.sell(product_id, CoinBase, QUOTE_CURRENCY)
order_id = order['id']
print("ID: {}, Order: Sell, Status: {}".format(order_id, order['status']))

while True:
	order_status = CoinBase.getOrderStatus(order_id)
	if order_status == "done":
		print("Sell fulfilled at {}".format(order['price']))
		break
	time.sleep(0.5)