import os
import numpy as np
import matplotlib.pyplot as plt
from features import StockFeatures
from model import StockModel

ASSETS_DIR = "assets"

def evaluate(df, model, cost=0.001):
    df = df.copy()
    df["prediction"] = model.predict(df.drop("target", axis=1))
    df["strategy"] = np.sign(df["prediction"])
    df["strategy_returns"] = df["strategy"].shift(1) * df["ret_1"]
    df["trades"] = df["strategy"].diff().fillna(0).abs()
    df["strategy_returns"] -= df["trades"] * cost
    df["cum_strategy_returns"] = (1 + df["strategy_returns"]).cumprod()
    df["cum_bh_returns"] = (1 + df["ret_1"]).cumprod()

    print(f"Strategy Returns: {df['cum_strategy_returns'].iloc[-1] - 1:.2%}")
    print(f"Buy & Hold Returns: {df['cum_bh_returns'].iloc[-1] - 1:.2%}")
    print(f"Sharpe Ratio: {df['strategy_returns'].mean() / df['strategy_returns'].std():.2f}")
    print(f"Max Drawdown: {(df['cum_strategy_returns'] / df['cum_strategy_returns'].cummax() - 1).min():.2%}")

    return df

def plot_results(df, out_path=f"{ASSETS_DIR}/backtest.png"):
    os.makedirs(ASSETS_DIR, exist_ok=True)

    plt.rcParams["font.family"] = "sans-serif"
    fig, ax = plt.subplots(figsize=(9, 5), dpi=150)

    ax.plot(df.index, df["cum_strategy_returns"], label="Strategy", color="#2a6f97", linewidth=1.8)
    ax.plot(df.index, df["cum_bh_returns"], label="Buy & Hold", color="#adb5bd", linewidth=1.8, linestyle="--")

    ax.set_title("Strategy vs Buy & Hold, Last 252 Trading Days", fontsize=13, weight="bold", pad=12)
    fig.text(0.01, 0.01, "Ticker: PAXG-USD", fontsize=8, color="#868e96")
    ax.set_ylabel("Growth of $1")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", color="#e9ecef", linewidth=0.8)
    ax.legend(frameon=False, loc="upper left")
    fig.tight_layout()

    fig.savefig(out_path)
    plt.close(fig)
    print(f"Saved chart to {out_path}")

if __name__ == "__main__":
    sf = StockFeatures()
    df = sf.build_features()

    model = StockModel()
    train_df = df[:-252]
    model.train(train_df)

    test_df = df[-252:]
    test_df = evaluate(test_df, model)
    plot_results(test_df)
