import pandas as pd
from sklearn.linear_model import LinearRegression

def train_ev_adoption_model(data_path):
    df = pd.read_csv(data_path)

    X = df[["year"]]
    y = df["ev_sales"]

    model = LinearRegression()
    model.fit(X, y)

    return model


def estimate_ev_adoption(subsidy_amount, base_rate):
    subsidy_effect = subsidy_amount / 100000
    return min(base_rate + subsidy_effect, 1.0)
