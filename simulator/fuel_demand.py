import pandas as pd
from sklearn.linear_model import LinearRegression

def calibrate_elasticity(data_path):
    df = pd.read_csv(data_path)

    df["price_pct_change"] = df["avg_fuel_price"].pct_change() * 100
    df["demand_pct_change"] = -0.3 * df["price_pct_change"]  # proxy

    df = df.dropna()

    X = df[["price_pct_change"]]
    y = df["demand_pct_change"]

    model = LinearRegression()
    model.fit(X, y)

    return model.coef_[0]


def calculate_fuel_demand_change(price_increase_pct, elasticity):
    return elasticity * price_increase_pct
