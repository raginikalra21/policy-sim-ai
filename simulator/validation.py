from utils.assumptions import (
    FUEL_DEMAND_ELASTICITY,
    BASE_EV_ADOPTION_RATE,
    AVG_FUEL_CONSUMPTION,
    CO2_PER_LITRE,
    TOTAL_VEHICLES
)

from simulator.fuel_demand import calculate_fuel_demand_change
from simulator.ev_adoption import estimate_ev_adoption
from simulator.emissions import calculate_emission_reduction
from simulator.government import calculate_government_impact
from ml_models.inflation_model import predict_inflation_risk


def run_simulation(fuel_tax, ev_subsidy):
    """
    Runs a single simulation scenario
    """

    # Proxy: treat ₹ fuel tax as % price increase for simulation
    price_increase_pct = fuel_tax

    fuel_demand_change = calculate_fuel_demand_change(
        price_increase_pct,
        FUEL_DEMAND_ELASTICITY
    )

    ev_adoption = estimate_ev_adoption(
        ev_subsidy,
        BASE_EV_ADOPTION_RATE
    )

    # Scale fuel reduction to national level
    fuel_reduction_litres = (
        abs(fuel_demand_change) / 100
        * AVG_FUEL_CONSUMPTION
        * TOTAL_VEHICLES
    )

    emissions_reduced = calculate_emission_reduction(
        fuel_reduction_litres,
        CO2_PER_LITRE
    )

    govt = calculate_government_impact(
        fuel_tax_increase=fuel_tax,
        total_fuel_consumption=AVG_FUEL_CONSUMPTION * TOTAL_VEHICLES,
        ev_subsidy=ev_subsidy,
        ev_units_sold=int(ev_adoption * TOTAL_VEHICLES)
    )

    inflation_risk = predict_inflation_risk(fuel_tax)

    return {
        "fuel_demand_change": fuel_demand_change,
        "ev_adoption": ev_adoption,
        "emissions_reduced": emissions_reduced,
        "government": govt,
        "inflation_risk": inflation_risk
    }


def validate_policy(fuel_tax, ev_subsidy):
    baseline = run_simulation(fuel_tax=0, ev_subsidy=0)
    policy = run_simulation(fuel_tax=fuel_tax, ev_subsidy=ev_subsidy)

    return {
        "baseline": baseline,
        "policy": policy
    }
