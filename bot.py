import config
from binance.client import Client
from binance.enums import *
import time
import numpy as np


client = Client(config.API_KEY, config.API_SECRET, tld='com')

symbolTicker = 'BNBBTC'
quantity = 1
prev_symbolPrice = 0

list_of_tickers = client.get_all_tickers()
for tick_2 in list_of_tickers:
    if tick_2["symbol"] == symbolTicker:
        prev_symbolPrice = float(tick_2["price"])

buyOrder = client.create_order(
    symbol = symbolTicker,
    side = 'BUY',
    type = 'STOP_LOSS_LIMIT',
    quantity = quantity,
    price = round(prev_symbolPrice*1.001,7),
    stopPrice = round(prev_symbolPrice*1.002,7),
    timeInForce = 'GTC'
)

while 1:
    time.sleep(5)

    list_of_tickers = client.get_all_tickers()
    for tick_2 in list_of_tickers:
        if tick_2["symbol"] == symbolTicker:
            current_symbolPrice = float(tick_2["price"])

    print("    Prev Price = " + str(prev_symbolPrice))
    print(" Current Price = " + str(current_symbolPrice))

    if ( prev_symbolPrice > current_symbolPrice):

        result = client.cancel_order(
            symbol = symbolTicker,
            orderId = buyOrder.get('orderId')
        )

        buyOrder = client.create_order(
            symbol = symbolTicker,
            side = 'BUY',
            type = 'STOP_LOSS_LIMIT',
            quantity = quantity,
            price = round(current_symbolPrice*1.001,7),
            stopPrice = round(current_symbolPrice*1.002,7),
            timeInForce = 'GTC'
        )

        prev_symbolPrice = current_symbolPrice


