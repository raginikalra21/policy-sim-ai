def calculate_government_impact(
    fuel_tax_increase,
    total_fuel_consumption,
    ev_subsidy,
    ev_units_sold
):
    fuel_tax_revenue = fuel_tax_increase * total_fuel_consumption
    subsidy_cost = ev_subsidy * ev_units_sold

    return {
        "revenue": fuel_tax_revenue,
        "subsidy_cost": subsidy_cost,
        "net_impact": fuel_tax_revenue - subsidy_cost
    }
