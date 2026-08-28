import numpy as np
import pandas as pd
from config import DATA_DIR, TICKER

class StockFeatures:
    def __init__(self):
        self.data = pd.read_csv(f"{DATA_DIR}/{TICKER}.csv", index_col="Date", parse_dates=True)

    def build_features(self, window=20):
        df = self.data.copy()
        # Raw Open/High/Low/Volume columns are kept as features intentionally
        df["ret_1"] = df["Close"].pct_change()
        df["ret_5"] = df["Close"].pct_change(5)
        df["ret_20"] = df["Close"].pct_change(20)
        df["sma_20"] = df["Close"].rolling(window).mean()
        df["sma_50"] = df["Close"].rolling(window*2).mean()
        df["rsi_14"] = self.rsi(df["Close"], 14)
        df["target"] = df["Close"].shift(-1) / df["Close"] - 1
        df.dropna(inplace=True)
        return df

    @staticmethod
    def rsi(series, window):
        diff = series.diff()
        gains = diff.where(diff > 0, 0)
        losses = -diff.where(diff < 0, 0)
        avg_gains = gains.rolling(window).mean()
        avg_losses = losses.rolling(window).mean()
        rs = avg_gains / np.maximum(avg_losses, 1e-10)  # avoid division by zero
        rsi = 100 - (100 / (1 + rs))
        return rsi
