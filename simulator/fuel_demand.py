def calculate_fuel_demand_change(price_increase_pct, elasticity):
    """
    Calculates percentage change in fuel demand
    """
    return elasticity * price_increase_pct
