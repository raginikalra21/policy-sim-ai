def calculate_emission_reduction(
    fuel_reduction_litres,
    co2_per_litre
):
    return fuel_reduction_litres * co2_per_litre / 1e6  # convert to MT
