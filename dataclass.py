import yfinance as yf
from config import DATA_DIR, TICKER

class StockData:
    def __init__(self):
        self.ticker = TICKER

    def download(self):
        data = yf.download(self.ticker)
        data.to_csv(f"{DATA_DIR}/{TICKER}.csv")
