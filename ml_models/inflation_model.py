def predict_inflation_risk(fuel_price_increase):
    if fuel_price_increase < 3:
        return "Low"
    elif fuel_price_increase < 7:
        return "Medium"
    else:
        return "High"
