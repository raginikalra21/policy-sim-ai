def calculate_government_impact(
    fuel_tax_increase,
    total_fuel_consumption,
    ev_subsidy,
    ev_units_sold
):
    revenue = fuel_tax_increase * total_fuel_consumption
    subsidy_cost = ev_subsidy * ev_units_sold
    return revenue - subsidy_cost
