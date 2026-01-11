def estimate_ev_adoption(subsidy_amount, base_rate):
    """
    Estimates increase in EV adoption due to subsidy
    """
    adoption_boost = subsidy_amount / 100000
    return min(base_rate + adoption_boost, 1.0)
