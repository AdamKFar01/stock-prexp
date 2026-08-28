import os
import pandas as pd
import yfinance as yf
from config import DATA_DIR, TICKER

class StockData:
    def __init__(self):
        self.ticker = TICKER

    def download(self):
        data = yf.download(self.ticker, period="5y")
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        os.makedirs(DATA_DIR, exist_ok=True)
        data.to_csv(f"{DATA_DIR}/{TICKER}.csv")
