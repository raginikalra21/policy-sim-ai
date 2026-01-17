import pandas as pd
import numpy as np
from scipy.optimize import curve_fit

def logistic(x, L, k, x0):
    return L / (1 + np.exp(-k * (x - x0)))

def train_ev_adoption_model(data_path):
    df = pd.read_csv(data_path)

    X = df["year"].values
    y = df["ev_sales"].values

    # Interpretable initial guesses
    p0 = [1_500_000, 0.4, 2022]

    params, _ = curve_fit(
        logistic, X, y, p0=p0, maxfev=10000
    )
    return params

def project_ev_sales(years, params):
    L, k, x0 = params
    return [logistic(y, L, k, x0) for y in years]
