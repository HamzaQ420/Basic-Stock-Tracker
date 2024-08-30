import yfinance as yf; from datetime import datetime; import time; import robin_stocks as robin; import os

f = open(os.getcwd() + "/data.txt", "r"); temp = f.readlines(); tickers = []
for x in temp: tickers.append(x.replace("\n", ""))

while True:
    time.sleep(5)
    for y in tickers:
        priceInfo = str(yf.Ticker(y).info).split(","); price = ""
        symbolInfo = str(yf.Ticker(y).info).split(","); symbol = ""
        for x in priceInfo:
            if "currentPrice" in x:
                if temp == x: priceUpdate = False
                else:
                    priceUpdate = True
                    temp = x; price = x;
                    price = str(round(float(price[price.index(":") + 2:]), 2))
                    if len(price[price.index("."):]) < 3:
                        price += "0"
                for x in symbolInfo:
                    if "symbol" in x:
                        symbol = x
                        symbol = symbol[symbol.index(":") + 2:]
                if len(price) < 6:
                    price += (" " * (6 - len(price)))
                if len(symbol) < 6: symbol += (" " * (6 - len(symbol)))
                if priceUpdate: print(symbol, " : ", price, datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    print()
