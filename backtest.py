import numpy as np
from features import StockFeatures
from model import StockModel

def evaluate(df, model):
    df["prediction"] = model.predict(df.drop("target", axis=1))
    df["strategy"] = np.sign(df["prediction"])
    df["returns"] = df["strategy"] * df["ret_1"]
    print("Strategy Returns:", df["returns"].sum())
    print("Buy & Hold Returns:", df["ret_1"].sum())

if __name__ == "__main__":
    sf = StockFeatures()
    df = sf.build_features()

    model = StockModel()
    train_df = df[:-252]
    model.train(train_df)

    test_df = df[-252:]
    evaluate(test_df, model)
