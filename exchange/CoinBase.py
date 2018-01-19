import json, requests, datetime
from exchange.CoinBaseAuthenticate import CoinbaseExchangeAuth

class CoinbaseExchange(object):
    def __init__(self, api_key, secret_key, passphrase, api_url):
        self.api_url = api_url
        self.auth = CoinbaseExchangeAuth(api_key, secret_key, passphrase, api_url)

    def getTime(self):
        request = requests.get(self.api_url + 'time')
        time = (request.json())['epoch']
        time_dt = datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')
       # print("Server datetime: %s" % TIMESTAMP_DT)
        return time_dt

    def getAccounts(self, quote_currency):
        request = requests.get(self.api_url + 'accounts', auth=self.auth)
        accounts = request.json()
        #Find index corresponding to pair
        index = next(index for (index, d) in enumerate(accounts) if ((d["currency"] == quote_currency)))
        balance = accounts[index]['balance']
        return balance

    def getOrderStatus(self, order_id):
        request = requests.get(self.api_url + 'orders/' + order_id , auth=self.auth)
        if request.status_code == 404:
            # A 404 was issued - order doesnt exist
            print('Order ID does not exist')
            return False
        else:
            order = request.json()
            status = order['status']
            return status

    def getBalance(self, currency):
        request = requests.get(self.api_url + 'accounts', auth=self.auth)
        accounts = request.json()
        #Find index corresponding to currency
        index = next(index for (index, d) in enumerate(accounts) if d["currency"] == currency)
        balance = accounts[index]['balance']
        return balance

    def getProductId(self, base_currency, quote_currency):
        #SandBox price list is inaccurate
        self.api_url = 'https://api.gdax.com/'
        request = requests.get(self.api_url + 'products', auth=self.auth)
        products = request.json()
        #Find index corresponding to pair
        index = next(index for (index, d) in enumerate(products) if ((d["base_currency"] == base_currency) and (d["quote_currency"] == quote_currency)))
        product_id = products[index]['id']
        return product_id

    def getPrice(self, product_id):
        #SandBox price list is inaccurate
        request = requests.get('https://api.gdax.com/' + 'products/' + product_id + '/ticker', auth=self.auth)
        product = request.json()
        price = product['price']
        return price

    def determinePrice(self, product_id, option):
        parameters = {
            'level': '1'
        }
        request = requests.get('https://api.gdax.com/' + 'products/' + product_id + '/book', data = json.dumps(parameters), auth=self.auth, timeout=30)
        book = request.json()
        if option == "buy":
            buy_price = float(book['bids'][0][0]) - 0.01
            return buy_price
        if option == "sell":
            sell_price = float(book['asks'][0][0]) + 0.01
            return sell_price

    def buy(self, product_id, quantity, price):
        time_to_cancel = "hour"
        #Rounded down to 11dp
        quantity = (quantity // 0.00000001) / 100000000
        parameters = {
            'type': 'limit',
            'size': quantity,
            'price': price,
            'side': 'buy',
            'product_id': product_id,
            'time_in_force': 'GTT',
            'cancel_after': time_to_cancel,
            'post_only': True
        }
        request = requests.post(self.api_url + 'orders', data = json.dumps(parameters), auth=self.auth, timeout=30)
        buy_order = request.json()
        return buy_order

    def sell(self, product_id, quantity, price, upper):
        #Round price to 2DP
        price = round(float(price), 2)       
        if upper is True:
            parameters = {
                'type': 'limit',
                'size': quantity,
                'price': price,
                'side': 'sell',
                'product_id': product_id,
                'time_in_force': 'GTC',
                'post_only': True
            }            
        else:
            time_to_cancel = "hour"
            parameters = {
                'type': 'limit',
                'size': quantity,
                'price': price,
                'side': 'sell',
                'product_id': product_id,
                'time_in_force': 'GTT',
                'cancel_after': time_to_cancel,
                'post_only': True
            }            
        request = requests.post(self.api_url + 'orders', data = json.dumps(parameters), auth=self.auth, timeout=30)
        sell_order = request.json()
        return sell_order

    def cancelOrder(self, order_id):
        request = requests.delete(self.api_url + 'orders/' + order_id , auth=self.auth)
        result = request.json()
        if 'message' in result:
            print(result['message'])
            return False
        else:
            return True

    def getOrders(self):
        request = requests.get(self.api_url + 'orders', auth=self.auth)
        orders = request.json()
        return orders