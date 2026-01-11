def adoption_trend(years, base_rate):
    return [base_rate * (1 + 0.15 * y) for y in range(years)]
