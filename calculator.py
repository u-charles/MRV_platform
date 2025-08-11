# calculator.py
from typing import Dict, Tuple
import pandas as pd

# Exact factors you provided (defaults)
EMISSION_FACTORS = { 
    # Energy
    "electricity_kwh": 0.47,
    "diesel_litre": 2.68,
    "petrol_litre": 2.31,
    "lpg_litre": 1.51,
    "natural_gas_m3": 1.9,

    # Water & Waste
    "water_litres": 0.0003,
    "waste_kg": 0.72,

    # Private Transport (per km)
    "petrol_car_km": 0.192,
    "diesel_car_km": 0.171,
    "ev_car_km": 0.075,

    # Public Transport (per person per km)
    "bus_km": 0.089,
    "motorcycle_km": 0.103
}

# Scope mapping for categories (Scope 1/2/3)
SCOPE_MAPPING = {
    "electricity_kwh": "Scope 2",
    "diesel_litre": "Scope 1",
    "petrol_litre": "Scope 1",
    "lpg_litre": "Scope 1",
    "natural_gas_m3": "Scope 1",
    "water_litres": "Scope 3",
    "waste_kg": "Scope 3",
    "petrol_car_km": "Scope 1",
    "diesel_car_km": "Scope 1",
    "ev_car_km": "Scope 2",
    "bus_km": "Scope 3",
    "motorcycle_km": "Scope 3"
}

def get_factors() -> Dict[str, float]:
    return EMISSION_FACTORS.copy()

def get_scope(activity_key: str) -> str:
    return SCOPE_MAPPING.get(activity_key, "Scope 3")

def calculate_category_emission(activity_key: str, value: float) -> float:
    factor = EMISSION_FACTORS.get(activity_key)
    if factor is None:
        raise KeyError(f"No emission factor for '{activity_key}'")
    return round(float(value) * float(factor), 6)

def calculate_bulk(inputs: Dict[str, float]) -> Tuple[Dict[str, float], float]:
    details = {}
    total = 0.0
    for k, v in inputs.items():
        if v is None or float(v) <= 0:
            continue
        e = calculate_category_emission(k, v)
        details[k] = e
        total += e
    return details, round(total, 6)
