# GDAX Tradingbot
An automated GDAX trading bot built in Python.

The bot uses a simple exponential moving average (EMA) crossover strategy to attempt to profit from short-term upwards trends in cryptocurrency. A buy/sell signal is triggered when the 5-period EMA and the 20-period EMA intercept. The bot uses the GDAX platform to buy/sell cryptocurrency, accessed via the official API.

This project uses Threads to perform separate functions:
*  Grab live price, calculate EMAs and identify if a crossover has occurred
*  Perform a trading action - buy/sell depending on crossover

As the bot runs, all prices and transactions are logged into separate CSV files.

_Use at your own risk._

## Getting Started

These instructions allow you to get running and customise the project.

### Prerequisites

You will need a GDAX account and an API key. Create a config file (config.py) in the root directory with the following format:

```
API_KEY = ""
API_SECRET = ""
API_PASS = ""
API_URL = "https://api.gdax.com/" #Sandbox: https://api-public.sandbox.gdax.com
```

The project was built and tested with Python 3.6.4. The project requires the following packages:

```
pandas
matplotlib.pyplot
threading
hmac
hashlib
requests
base64
json
requests
datetime
```
### Customisation

To customise the project you can edit the following variables, as shown in example.py:

```
LOOP_DURATION = 58.5 # Time period (in seconds)
MAX_LOOP_TIME = 8 * 60 * 60 # Max duration to run (in seconds)
QUOTE_CURRENCY = "BTC" # Cryptocurrency of choice
BASE_CURRENCY = "EUR" # Fiat currency of choice
CSV_PRICE = 'price.csv' # Price CSV name
CSV_TRANSACTIONS = 'transactions.csv' # Transaction CSV name
```

## Authors

* **Calum McGuicken**


## License

This project is licensed under the MIT License

## Acknowledgments

* [GDAX Official API Documentation](https://docs.gdax.com/)
* [20-day/5-day EMA with Forex](http://www.theforexchronicles.com/the-ema-5-and-ema-20-crossover-trading-strategy/)
