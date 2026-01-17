import pandas as pd
from sklearn.linear_model import LinearRegression

def train_emissions_model(data_path):
    df = pd.read_csv(data_path)

    X = df[["year"]]
    y = df["transport_emissions_mt"]

    model = LinearRegression()
    model.fit(X, y)

    return model

def project_emissions(model, years):
    return model.predict([[y] for y in years])
