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

from simulator.validation import validate_policy

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
    results = validate_policy(fuel_tax, ev_subsidy)

    baseline = results["baseline"]
    policy = results["policy"]

    # ---------------- Key Metrics ----------------

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "⛽ Fuel Demand Change (%)",
        f"{policy['fuel_demand_change']:.2f}",
        delta=f"{policy['fuel_demand_change'] - baseline['fuel_demand_change']:.2f}"
    )

    col2.metric(
        "⚡ EV Adoption Rate",
        f"{policy['ev_adoption']*100:.1f}%",
        delta=f"{(policy['ev_adoption'] - baseline['ev_adoption'])*100:.1f}%"
    )

    col3.metric(
        "🌍 CO₂ Reduction (MT)",
        f"{policy['emissions_reduced']:.2f}",
        delta=f"{policy['emissions_reduced'] - baseline['emissions_reduced']:.2f}"
    )

    col4.metric(
        "⚠ Inflation Risk",
        policy["inflation_risk"]
    )

    # ---------------- Government Impact ----------------

    st.subheader("🏛 Government Fiscal Impact")

    policy_govt = policy["government"]
    baseline_govt = baseline["government"]

    st.write(f"**Fuel Tax Revenue:** ₹{policy_govt['revenue']:,}")
    st.write(f"**EV Subsidy Cost:** ₹{policy_govt['subsidy_cost']:,}")
    st.write(f"**Net Impact:** ₹{policy_govt['net_impact']:,}")

    st.caption(
        f"Baseline net impact: ₹{baseline_govt['net_impact']:,}"
    )

    # ---------------- Emissions Visualization ----------------

    st.subheader("📊 Emissions Impact Visualization")

    fig, ax = plt.subplots()
    ax.bar(
        ["Baseline", "Policy"],
        [
            baseline["emissions_reduced"],
            policy["emissions_reduced"]
        ]
    )
    ax.set_ylabel("CO₂ Reduction (MT)")
    ax.set_title("Baseline vs Policy Emissions Impact")

    st.pyplot(fig)

else:
    st.info("Adjust policy parameters and click **Simulate Policy**")
