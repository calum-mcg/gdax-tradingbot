import logging
import pandas as pd
import matplotlib.pyplot as plt
from exchange import *

logging.basicConfig(level=logging.INFO)

class Model(object):
    def __init__(self):
        self.ema_dataframe = pd.DataFrame(data={'datetime': [],'price': [], 'EMA4': [], 'EMA20': [], 'signal': []})
        self.transaction_dataframe = pd.DataFrame(data={'product_id' : [], 'datetime': [], 'buy/sell': [], 'price': [],   'quantity': []})

    def calculateEma(self, CoinBase, product_id):
        #Get current price and time
        price = CoinBase.getPrice(product_id)
        datetime = CoinBase.getTime()

        self.ema_dataframe = self.ema_dataframe.append(pd.DataFrame({'datetime': datetime, 'price': price}, index=[0]), ignore_index=True)
        length = self.ema_dataframe.shape[0]
        if length>4:
            self.ema_dataframe['EMA4'] = self.ema_dataframe['price'].dropna().shift().fillna(self.ema_dataframe['EMA4']).ewm(com=4).mean()
        if length>20:
            self.ema_dataframe['EMA20'] = self.ema_dataframe['price'].dropna().shift().fillna(self.ema_dataframe['EMA20']).ewm(com=20).mean()

    def calculateCrossover(self):
        length = self.ema_dataframe.shape[0]
        if length>4:
            EMA4 = self.ema_dataframe['EMA4'].tail(2).reset_index(drop=True)
            EMA20 = self.ema_dataframe['EMA20'].tail(2).reset_index(drop=True)
            if (EMA4[1] <= EMA20[1]) & (EMA4[0] >= EMA20[0]):
                signal = {"signal": True, "value": "sell"}
            elif (EMA4[1] >= EMA20[1]) & (EMA4[0] <= EMA20[0]):
                signal = {"signal": True, "value": "buy"}
            else:
                signal = {"signal": False, "value": None}
            self.ema_dataframe.loc[self.ema_dataframe.index[length-1], 'signal'] = signal['value']
            print(self.ema_dataframe)
            return signal

    def buy(self, product_id, CoinBase, base_currency):
        print("Buy signal. Logging..")
        price = CoinBase.getPrice(product_id)
        #TODO: calculate best price for market making
        time = CoinBase.getTime()
        # balance = CoinBase.getBalance(base_currency)
        balance = 1000.00
        quantity = balance/float(price)
        self.transaction_dataframe.loc[self.transaction_dataframe.shape[0]] =  [product_id, time, 'buy', price, quantity]

    def sell(self, product_id, CoinBase, quote_currency):
        print("Sell signal. Logging..")
        price = CoinBase.getPrice(product_id)
        #TODO: calculate best price for market making
        time = CoinBase.getTime()
        #position = CoinBase.getPosition(quote_currency)
        position = 1.05
        self.transaction_dataframe.loc[self.transaction_dataframe.shape[0]] =  [product_id, time, 'sell', price, position]

    def plotGraph(self):
        self.ema_dataframe['price'] = self.ema_dataframe['price'].astype(float)
        self.ema_dataframe['EMA4'] = self.ema_dataframe['EMA4'].astype(float)
        self.ema_dataframe['EMA20'] = self.ema_dataframe['EMA20'].astype(float)
        pl = self.ema_dataframe[['datetime', 'price']].plot(label='Price')
        self.ema_dataframe[['datetime', 'EMA4']].plot(label='EMA4', ax=pl)
        self.ema_dataframe[['datetime', 'EMA20']].plot(label='EMA20', ax=pl)
        plt.xlabel('Datetime')
        plt.ylabel('Price')
        plt.legend()
        plt.show()

    def logPrice(self, csvname):
        self.ema_dataframe.to_csv(csvname, encoding='utf-8', index=False)

    def logTransactions(self, csvname):
        self.transaction_dataframe.to_csv(csvname, encoding='utf-8', index=False)