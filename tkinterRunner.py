import tkinter as tk

items = []
root = tk.Tk()

def returnItems():
    return items

def main():
    stockName = tk.StringVar()
    stockPrice = tk.StringVar()
    stockBS = tk.StringVar()

    stockNameLabel = tk.Label(root, text = "Stock Ticker:")
    stockNameEntry = tk.Entry(root, textvariable = stockName)

    stockPriceLabel = tk.Label(root, text = "Stock Price:")
    stockPriceEntry = tk.Entry(root, textvariable = stockPrice)

    choices = ["Bought", "Sold"]
    stockBS.set("Null")
    choiceMenu = tk.OptionMenu(root, stockBS, *choices)

    def submit(e):
        global items
        name = stockName.get(); stockName.set("")
        price = stockPrice.get(); stockPrice.set("")
        bs = stockBS.get();
        items = [name, price, bs]
        root.quit()

    root.bind("<Return>", submit)

    stockNameLabel.grid(row = 0, column = 0)
    stockNameEntry.grid(row = 0, column = 1)
    stockPriceLabel.grid(row = 1, column = 0)
    stockPriceEntry.grid(row = 1, column = 1)
    choiceMenu.grid(row = 0, column = 2)

    tk.mainloop()
