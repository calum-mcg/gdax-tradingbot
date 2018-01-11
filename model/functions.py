import logging
import pandas as pd
import matplotlib.pyplot as plt
from exchange import *

logging.basicConfig(level=logging.INFO)

class Model(object):
    def __init__(self):
        self.ema_dataframe = pd.DataFrame(data={'datetime': [],'price': [], 'EMA4': [], 'EMA18': [], 'signal': []})
        self.transaction_dataframe = pd.DataFrame(data={'GDAX_id' : [], 'product_id' : [], 'datetime': [], 'buy/sell': [], 'price': [], 'quantity': [], 'status': []})
        self.csv_price = 'price.csv'
        self.csv_transactions = 'transactions.csv'

    def calculateEma(self, CoinBase, product_id):
        #Get current price and time
        price = CoinBase.getPrice(product_id)
        datetime = CoinBase.getTime()

        self.ema_dataframe = self.ema_dataframe.append(pd.DataFrame({'datetime': datetime, 'price': price}, index=[0]), ignore_index=True)
        length = self.ema_dataframe.shape[0]
        if length>4:
            self.ema_dataframe['EMA4'] = self.ema_dataframe['price'].dropna().shift().fillna(self.ema_dataframe['EMA4']).ewm(com=4).mean()
        if length>18:
            self.ema_dataframe['EMA18'] = self.ema_dataframe['price'].dropna().shift().fillna(self.ema_dataframe['EMA18']).ewm(com=18).mean()

    def calculateCrossover(self):
        length = self.ema_dataframe.shape[0]
        if length>4:
            EMA4 = self.ema_dataframe['EMA4'].tail(2).reset_index(drop=True)
            EMA18 = self.ema_dataframe['EMA18'].tail(2).reset_index(drop=True)
            if (EMA4[1] <= EMA18[1]) & (EMA4[0] >= EMA18[0]):
                signal = {"signal": True, "value": "sell"}
            elif (EMA4[1] >= EMA18[1]) & (EMA4[0] <= EMA18[0]):
                signal = {"signal": True, "value": "buy"}
            else:
                signal = {"signal": False, "value": None}
            self.ema_dataframe.loc[self.ema_dataframe.index[length-1], 'signal'] = signal['value']
            print(self.ema_dataframe)
            return signal

    def buy(self, product_id, CoinBase, base_currency):
        time = CoinBase.getTime()
        buy_price = CoinBase.determinePrice(product_id, "buy")
        balance = CoinBase.getBalance(base_currency)
        balance = float(balance) * 0.1
        quantity = float(balance)/float(buy_price)
        order = CoinBase.buy(product_id, quantity, buy_price)
        if 'id' in order:
            id = order['id']
            status = order['status']
            self.transaction_dataframe.loc[self.transaction_dataframe.shape[0]] =  [id, product_id, time, 'buy', buy_price, quantity, status]
            self.logTransactions(True)
            return order
        else:
            print(order)
            return -1 

    def sell(self, product_id, CoinBase, quote_currency):
        time = CoinBase.getTime()
        sell_price = CoinBase.determinePrice(product_id, "sell")
        quantity = CoinBase.getAccounts(quote_currency)
        order = CoinBase.sell(product_id, quantity, sell_price)
        if 'id' in order:
            id = order['id']
            status = order['status']
            self.transaction_dataframe.loc[self.transaction_dataframe.shape[0]] =  [id, product_id, time, 'sell', sell_price, quantity, status]
            self.logTransactions(True)
            return order
        else:
            print(order)
            return -1 

    def plotGraph(self):
        self.ema_dataframe['price'] = self.ema_dataframe['price'].astype(float)
        self.ema_dataframe['EMA4'] = self.ema_dataframe['EMA4'].astype(float)
        self.ema_dataframe['EMA18'] = self.ema_dataframe['EMA18'].astype(float)
        pl = self.ema_dataframe[['datetime', 'price']].plot(label='Price')
        self.ema_dataframe[['datetime', 'EMA4']].plot(label='EMA4', ax=pl)
        self.ema_dataframe[['datetime', 'EMA18']].plot(label='EMA18', ax=pl)
        plt.xlabel('Datetime')
        plt.ylabel('Price')
        plt.legend()
        plt.show()

    def logPrice(self, append):
        if (append):
            self.ema_dataframe.to_csv(self.csv_price, encoding='utf-8', mode='a', index=False)
        else:
            self.ema_dataframe.to_csv(self.csv_price, encoding='utf-8', index=False)          

    def logTransactions(self, append):
        if (append):
            self.transaction_dataframe.to_csv(self.csv_transactions, encoding='utf-8', mode='a', index=False)
        else:
            self.transaction_dataframe.to_csv(self.csv_transactions, encoding='utf-8', index=False)  