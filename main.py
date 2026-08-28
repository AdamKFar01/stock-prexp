from dataclass import StockData
from features import StockFeatures
from model import StockModel
from backtest import evaluate

if __name__ == "__main__":
    # Download data
    sd = StockData()
    sd.download()

    # Build features
    sf = StockFeatures()
    df = sf.build_features()

    # Train model
    model = StockModel()
    train_df = df[:-252]
    model.train(train_df)

    # Backtest
    test_df = df[-252:]
    evaluate(test_df, model)
