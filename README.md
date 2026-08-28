# stock-prexp

A simple pipeline to predict next day returns for PAXG using a Random Forest model.

## Files

- `config.py`: sets the data directory and ticker symbol.
- `dataclass.py`: downloads price history with yfinance and saves it to a CSV.
- `features.py`: builds features like returns, moving averages, and RSI from the CSV.
- `model.py`: trains a Random Forest to predict next day return.
- `backtest.py`: runs the model on a holdout period and compares strategy returns to buy and hold.
- `main.py`: runs the full pipeline, download, features, train, backtest.

## Setup

1. Install dependencies:
```
pip install -r requirements.txt
```

2. Edit `config.py`:
- Set `DATA_DIR` to a real folder on your machine.
- Set `TICKER` to `PAXG-USD` so yfinance can find the data.

## Run

```
python main.py
```

This downloads the data, builds features, trains the model, and prints strategy returns versus buy and hold for the last 252 trading days.

## Status

This is an early skeleton, not a finished trading system. Known gaps are tracked in commit history and should be fixed before relying on any output.
