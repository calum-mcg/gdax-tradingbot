import time
from threading import Event, Thread
from exchange.CoinBase import *
from model.Functions import *
from config import *

class TimedThread(Thread):
    def __init__(self, event, wait_time, quote_currency, base_currency):
        Thread.__init__(self)
        self.stopped = event
        self.wait_time = wait_time
        self.quote_currency = quote_currency
        self.base_currency = base_currency
        #Authenticate details
        self.CoinBase = CoinbaseExchange(API_KEY, API_SECRET, API_PASS, API_URL)
		#Create model
        self.model = Model()
		#Choose Product
        self.product_id = self.CoinBase.getProductId(self.quote_currency, self.base_currency)
        #Specify timeout duration
        self.order_timeout = 180

    def run(self):
        while not self.stopped.wait(self.wait_time):
        	self.EMACrossover()

    def order(self, type):	
    	if (type == "sell"):
    		#Sell product
			#Get all open orders and cancel
    		open_orders = self.CoinBase.getOrders()
    		if(len(open_orders) > 0):
    			for order in open_orders:
    				self.CoinBase.cancelOrder(order['id'])

    		current_balance = float(self.CoinBase.getBalance(self.quote_currency))
    		if current_balance > 0:
				#Sell current position
	    		order = self.model.sell(self.product_id, self.CoinBase, self.quote_currency)
	    		order_time = order['created_at']
	    		order_id = order['id']
	    		price = order['price']
	    		print("Time: {}, Order: Sell, Price:{}, Status: {}".format(order_time, price, order['status']))
	    		timer_count = 0

	    		while True:
	    			if timer_count > self.order_timeout:
	    				self.CoinBase.cancelOrder(order_id)
	    				print("Time limit exceeded, order cancelled")
	    				break
	    			order_status = self.CoinBase.getOrderStatus(order_id)
	    			if order_status == "done":
	    				print("Sell fulfilled at {}".format(order['price']))
	    				break
	    			time.sleep(1)
	    			timer_count = timer_count + 1
    		else:
    			order_time = self.CoinBase.getTime()
    			print("Time: {}, Order: Sell, No currency available.".format(order_time))
    		
    	elif (type == "buy"):
    		current_balance = float(self.CoinBase.getBalance(self.base_currency))
    		if current_balance > 0:
	    		#Buy product
	    		order = self.model.buy(self.product_id, self.CoinBase, self.base_currency)
	    		order_time = order['created_at']
	    		order_id = order['id']
	    		print("Time: {}, Order: Buy, Status: {}".format(order_time, order['status']))
	    		timer_count = 0
	    		while True:
	    			if timer_count > self.order_timeout:
	    				self.CoinBase.cancelOrder(order_id)
	    				print("Time limit exceeded, order cancelled")
	    				break
	    			order_status = self.CoinBase.getOrderStatus(order_id)
	    			if order_status == "done":
	    				print("Buy fulfilled at {}".format(order['price']))
	    				upper_order = self.model.sellUpper(self.product_id, self.CoinBase, self.quote_currency)
	    				order_time = upper_order['created_at']
	    				order_price = upper_order['price']
	    				print("Time:{}, Order: SellUpper, Price:{}, Status: {}".format(order_time, order_price, order['status']))
	    				break
	    			time.sleep(1)
	    			timer_count = timer_count + 1
	    			return
	    	else:
    			order_time = self.CoinBase.getTime()
    			print("Time: {}, Order: Buy, No currency available.".format(order_time))

    def EMACrossover(self):
	    self.model.calculateEma(self.CoinBase, self.product_id)
	    signal = self.model.calculateCrossover()
	    if signal is not None:
	        if signal["value"] == "buy":
	            order_thread = Thread(target=self.order, args=('buy',))
	            order_thread.start()
	        elif signal["value"] == "sell":
	            order_thread = Thread(target=self.order, args=('sell',))
	            order_thread.start()