from sklearn.ensemble import RandomForestRegressor

class StockModel:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100)

    def train(self, df):
        X = df.drop("target", axis=1)
        y = df["target"]
        self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)
