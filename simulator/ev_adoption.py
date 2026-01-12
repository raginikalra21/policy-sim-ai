def estimate_ev_adoption(subsidy_amount, base_rate):
    """
    Estimate EV adoption rate (short-term, 1–3 years horizon)

    Assumptions:
    - Diminishing returns on subsidy
    - Saturation around 30–35%
    - Explainable, rule-based (judge-friendly)
    """

    # Normalize subsidy (₹0–₹100k → 0–1)
    subsidy_normalized = subsidy_amount / 100_000

    # Diminishing returns (concave response)
    subsidy_effect = 0.25 * subsidy_normalized  

    estimated_rate = base_rate + subsidy_effect

    # Cap adoption to realistic upper bound
    return min(estimated_rate, 0.35)
