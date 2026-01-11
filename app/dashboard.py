import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import matplotlib.pyplot as plt

from utils.assumptions import (
    FUEL_DEMAND_ELASTICITY,
    BASE_EV_ADOPTION_RATE,
    AVG_FUEL_CONSUMPTION,
    CO2_PER_LITRE
)

from simulator.fuel_demand import calculate_fuel_demand_change
from simulator.ev_adoption import estimate_ev_adoption
from simulator.emissions import calculate_emission_reduction
from simulator.government import calculate_government_impact
from ml_models.inflation_model import predict_inflation_risk

# ---------------- UI ----------------

st.set_page_config(page_title="PolicySim.ai", layout="wide")

st.title("🧠 PolicySim.ai")
st.subheader("Fuel Tax & EV Subsidy Policy Simulator")

st.markdown(
    "Simulate the **economic and environmental impact** of transport policies "
    "before real-world implementation."
)

# ---------------- Inputs ----------------

st.sidebar.header("🔧 Policy Inputs")

fuel_tax = st.sidebar.slider(
    "Fuel Tax Increase (₹ per litre)",
    min_value=0,
    max_value=15,
    value=5
)

ev_subsidy = st.sidebar.slider(
    "EV Subsidy (₹)",
    min_value=0,
    max_value=100000,
    value=50000,
    step=5000
)

simulate = st.sidebar.button("▶ Simulate Policy")

# ---------------- Simulation ----------------

if simulate:
    price_increase_pct = (fuel_tax / 100) * 100  # simple proxy

    fuel_demand_change = calculate_fuel_demand_change(
        price_increase_pct,
        FUEL_DEMAND_ELASTICITY
    )

    ev_adoption = estimate_ev_adoption(
        ev_subsidy,
        BASE_EV_ADOPTION_RATE
    )

    fuel_reduction_litres = abs(fuel_demand_change) * AVG_FUEL_CONSUMPTION

    emissions_reduced = calculate_emission_reduction(
        fuel_reduction_litres,
        CO2_PER_LITRE
    )

    govt = calculate_government_impact(
        fuel_tax_increase=fuel_tax,
        total_fuel_consumption=AVG_FUEL_CONSUMPTION,
        ev_subsidy=ev_subsidy,
        ev_units_sold=int(ev_adoption * 100000)
    )

    inflation_risk = predict_inflation_risk(fuel_tax)

    # ---------------- Metrics ----------------

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("⛽ Fuel Demand Change (%)", f"{fuel_demand_change:.2f}")
    col2.metric("⚡ EV Adoption Rate", f"{ev_adoption*100:.1f}%")
    col3.metric("🌍 CO₂ Reduction (MT)", f"{emissions_reduced:.2f}")
    col4.metric("⚠ Inflation Risk", inflation_risk)

    # ---------------- Government Impact ----------------

    st.subheader("🏛 Government Fiscal Impact")

    st.write(f"**Fuel Tax Revenue:** ₹{govt['revenue']:,}")
    st.write(f"**EV Subsidy Cost:** ₹{govt['subsidy_cost']:,}")
    st.write(f"**Net Impact:** ₹{govt['net_impact']:,}")

    # ---------------- Graph ----------------

    st.subheader("📊 Emissions Impact Visualization")

    fig, ax = plt.subplots()
    ax.bar(
        ["Before Policy", "After Policy"],
        [0, emissions_reduced]
    )
    ax.set_ylabel("CO₂ Reduction (MT)")
    ax.set_title("Emission Impact of Policy")

    st.pyplot(fig)

else:
    st.info("Adjust policy parameters and click **Simulate Policy**")
