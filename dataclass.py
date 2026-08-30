import os
import requests
import pandas as pd

from config import DATA_DIR, OUTPUT_CSV, COINGECKO_COIN_ID, ALPHAVANTAGE_SYMBOL

COINGECKO_URL = f"https://api.coingecko.com/api/v3/coins/{COINGECKO_COIN_ID}/market_chart"
ALPHAVANTAGE_URL = "https://www.alphavantage.co/query"


class DataSourceError(Exception):
    pass


class StockData:
    def download(self):
        try:
            df = self._fetch_coingecko()
            source = "CoinGecko"
        except (DataSourceError, requests.RequestException) as e:
            print(f"CoinGecko failed ({e}), falling back to Alpha Vantage")
            df = self._fetch_alphavantage()
            source = "Alpha Vantage"

        os.makedirs(DATA_DIR, exist_ok=True)
        out_path = f"{DATA_DIR}/{OUTPUT_CSV}"
        df.to_csv(out_path)

        print(f"Data source used: {source}")
        print(f"Rows saved: {len(df)}")
        print(f"Saved to {out_path}")
        return df

    def _fetch_coingecko(self):
        # Free-tier CoinGecko caps history at 365 days. Only /market_chart
        # gives real daily granularity (one sample per day); the dedicated
        # /ohlc endpoint collapses to 4-day candles beyond 30 days on the
        # free tier, too coarse for this pipeline. So Open/High/Low aren't
        # available from this source, only Close and Volume.
        params = {"vs_currency": "usd", "days": 365}
        resp = requests.get(COINGECKO_URL, params=params, timeout=15)
        if resp.status_code != 200:
            raise DataSourceError(f"HTTP {resp.status_code}: {resp.text[:200]}")

        payload = resp.json()
        prices = payload.get("prices")
        if not prices:
            raise DataSourceError(f"unexpected/empty response: {str(payload)[:200]}")

        volumes = dict(payload.get("total_volumes", []))

        rows = []
        for ts, price in prices:
            date = pd.to_datetime(ts, unit="ms").normalize()
            rows.append({"Date": date, "Close": price, "Volume": volumes.get(ts)})

        df = pd.DataFrame(rows).set_index("Date")
        df = df[~df.index.duplicated(keep="last")]
        df.sort_index(inplace=True)
        return df

    def _fetch_alphavantage(self):
        api_key = os.environ.get("ALPHAVANTAGE_API_KEY")
        if not api_key:
            raise DataSourceError("ALPHAVANTAGE_API_KEY environment variable is not set")

        params = {
            "function": "DIGITAL_CURRENCY_DAILY",
            "symbol": ALPHAVANTAGE_SYMBOL,
            "market": "USD",
            "apikey": api_key,
        }
        resp = requests.get(ALPHAVANTAGE_URL, params=params, timeout=15)
        if resp.status_code != 200:
            raise DataSourceError(f"HTTP {resp.status_code}: {resp.text[:200]}")

        payload = resp.json()
        series = payload.get("Time Series (Digital Currency Daily)")
        if not series:
            raise DataSourceError(f"unexpected/empty response: {str(payload)[:300]}")

        def pick(values, *keys):
            for k in keys:
                if k in values:
                    return float(values[k])
            raise DataSourceError(f"missing expected field among {keys} in {values}")

        rows = []
        for date_str, values in series.items():
            rows.append({
                "Date": pd.to_datetime(date_str),
                "Open": pick(values, "1. open", "1a. open (USD)"),
                "High": pick(values, "2. high", "2a. high (USD)"),
                "Low": pick(values, "3. low", "3a. low (USD)"),
                "Close": pick(values, "4. close", "4a. close (USD)"),
                "Volume": pick(values, "5. volume"),
            })

        df = pd.DataFrame(rows).set_index("Date")
        df.sort_index(inplace=True)
        return df
