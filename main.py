import yfinance as yf; from datetime import datetime; import time; import os; import pygame as pg; import tkinter as tk; import tkinterRunner

pg.init()
# Setting up the pygame window for the UI, technically just a viewing screen right now though.
#       Later you should set up a connection to Robinhood or various other trading platforms so that you can buy and sell with just a click.
class window:
    dimensions = (800, 400)
    screen = pg.display.set_mode(dimensions)
    clock = pg.time.Clock()

    # Setting the window name.
    pg.display.set_caption("Stock Analyzer")

    # Font Setup
    font = pg.font.Font(os.getcwd() + "/ocr.ttf", 25)
    text = font.render("Hello", True, "black")

    # Background and buy/sell text setup.
    bg = pg.Surface(dimensions); bg.fill("black")
    textDimensions = (72, 20)
    textBG = pg.Surface(textDimensions); textBG.fill("white")

# Taking information from the tkinter input window, parsing it, then writing it to our data.txt file.
def writeToFile():
    flag = False
    info = tkinterRunner.returnItems()
    ticker = info[0].upper(); price = float(info[1]); bs = "S" if info[2] == "Sold" else "B"
    stockInfo = ticker + ":" + bs + "," + str(price)

    f = open(os.getcwd() + "/data.txt", "r"); lines = f.readlines(); f.close()
    string = ""
    for x in lines:
        if ticker in x:
          string += stockInfo + "\n"
          flag = True
        else: string += x
    f = open(os.getcwd() + "/data.txt", "w");
    f.write(string + "\n") if flag else f.write(string + "\n" + stockInfo)

# Setting up tkinter for the entry message boxes.
run = True
# Main loop
while run:
    # Pygame event loop to make the screen show up.
    for event in pg.event.get():
        if event.type == pg.quit:
            pg.quit(); exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit(); exit()
            if event.key == pg.K_TAB:
                tkinterRunner.main()
                writeToFile()

    # Getting the information from the data.txt file and parsing it into 3 lists. Tickers, last bought/sold, prices at which bought/sold.
    f = open(os.getcwd() + "/data.txt", "r"); temp = f.readlines(); tickers = []; bs = []; prices = [];
    # Initializing variables for the while loop to use.
    previousPrice = 0; priceChange = 0; txtLST = []; color = ""

    # Parsing the information in the text file into the 3 lists.
    for x in temp:
        if x == "\n": continue
        x = x.split(":"); tickers.append(x[0])
        x = x[1].split(","); bs.append(x[0]); prices.append(float(x[1].replace("\n", "")))

    # Below is a delay function in case you don't want the code running every second.
    #time.sleep(5)
    # Loop to get the individual ticker information.
    for y in tickers:
        # Right now, we are just retrieving the ticker infor from yahoo finance as it updates.
        priceInfo = str(yf.Ticker(y).info).split(","); price = ""
        symbolInfo = str(yf.Ticker(y).info).split(","); symbol = ""

        # Parsing the ticker info from yahoo finance to get the price and symbol.
        # This loop could DEFINITELY be optimized, consider rewriting entirely.
        for x in priceInfo:
            if "currentPrice" in x:
                price = x
                price = str(round(float(price[price.index(":") + 2:]), 2))
                if len(price[price.index("."):]) < 3: price += "0"
                for x in symbolInfo:
                    if "symbol" in x:
                        symbol = x
                        symbol = symbol[symbol.index(":") + 2:]
                if len(price) < 6: price += (" " * (6 - len(price)))
                if len(symbol) < 6: symbol += (" " * (6 - len(symbol)))
                previousPrice = float(prices[tickers.index(y)]);
                priceChange = round(-((previousPrice - float(price)) / float(price)) * 100, 3)
                if priceChange > 0: priceChange = "+" + str(priceChange)
                # Printing the ticker info for each ticker in the tickers list to the terminal.
                print(symbol, " : ", price, datetime.now().strftime("%d/%m/%Y %H:%M:%S"), priceChange)

        # Formatting specific tickers. Ignore this, to be optimized later but for now it is hard-coded for Lucid and AMD.
        if len(price) < 6: price += (" " * (6 - len(price)))
        if len(price[price.index("."):]) < 3: price += "0"
        if len(symbol.replace("'", "").replace(" ", "")) == 3: symbol += " "

        # Checking the text file to see if a stock was recently bought or sold, then using that to figure out if the stock should be sold
        # if the price goes above 7% or bought if it dips below -7%. If neither, the option is to keep the stock.
        if bs[tickers.index(symbol.replace("'", "").replace(" ", ""))] == "B" and float(priceChange) > 7: val = "Sell"
        elif bs[tickers.index(symbol.replace("'", "").replace(" ", ""))] == "S" and float(priceChange) < -7: val = "Buy"
        else: val = "Keep"

        # Formatting the ticker information to print to the screen.
        text = str(symbol + " : " + price)

        # Adding all the information to be printed to the screen to a list so they are all in one place to be referenced.
        txtLST.append([text, str(priceChange), val, price, yf.Ticker(y).info["fiftyTwoWeekHigh"], yf.Ticker(y).info["fiftyTwoWeekLow"]])

    # Rendering Work
    window.screen.blit(window.bg, (0, 0))

    window.text = window.font.render(datetime.now().strftime("%m/%d/%Y %H:%M:%S"), True, "White")
    window.screen.blit(window.text, (260, 5)); vshift = 40

    # Rendering work.
    for n in txtLST:
        # Rendering the ticker information.
        window.text = window.font.render(n[0], True, "white")
        window.screen.blit(window.text, (2, txtLST.index(n) * 24 + vshift))

        # Rendering the price change percentage (priceChange).
        if float(n[1]) == 0: color = "yellow"
        elif "+" in n[1]: color = "green"
        else: color = "red"
        window.text = window.font.render(n[1], True, color)
        window.screen.blit(window.text, (222, txtLST.index(n) * 24 + vshift))

        # Rendering whether to buy, keep, or sell the stock.
        if n[2] == "Keep": color = "yellow"
        elif n[2] == "Sell": color = "green"
        else: color = "red"
        window.text = window.font.render(str(n[2]), True, "black")
        window.textBG.fill(color)
        window.screen.blit(window.textBG, (337, txtLST.index(n) * 24 + 5 + vshift))
        window.screen.blit(window.text, (342, txtLST.index(n) * 24 + vshift))

        # Rendering the weekly highest stock price.
        window.text = window.font.render("52 High: " + str(n[4]), True, "light green")
        window.screen.blit(window.text, (417, txtLST.index(n) * 24 + vshift))

        # Rendering the weekly low stock price.
        window.text = window.font.render("Low: " + str(n[5]), True, "#FF474C")
        window.screen.blit(window.text, (632, txtLST.index(n) * 24 + vshift))

    pg.display.update()
    window.clock.tick(60)
    txtLST = []
    print()
