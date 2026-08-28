import numpy as np
from features import StockFeatures
from model import StockModel

def evaluate(df, model, cost=0.001):
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

if __name__ == "__main__":
    sf = StockFeatures()
    df = sf.build_features()

    model = StockModel()
    train_df = df[:-252]
    model.train(train_df)

    test_df = df[-252:]
    evaluate(test_df, model)
