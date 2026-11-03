"""
Automotive and thermodynamic unit conversion utilities.
"""

def kw_to_hp(kw: float) -> float:
    """Converts Kilowatts to Mechanical Horsepower (hp)."""
    return kw * 1.34102209


def hp_to_kw(hp: float) -> float:
    """Converts Mechanical Horsepower to Kilowatts (kW)."""
    return hp / 1.34102209


def celsius_to_kelvin(celsius: float) -> float:
    """Converts Celsius to Kelvin."""
    return celsius + 273.15


def kelvin_to_celsius(kelvin: float) -> float:
    """Converts Kelvin to Celsius."""
    return kelvin - 273.15


def kwh_to_mj(kwh: float) -> float:
    """Converts Kilowatt-hours to Megajoules."""
    return kwh * 3.6


def mj_to_kwh(mj: float) -> float:
    """Converts Megajoules to Kilowatt-hours."""
    return mj / 3.6

