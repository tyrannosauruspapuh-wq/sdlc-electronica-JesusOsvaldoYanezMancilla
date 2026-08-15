def celsius_to_fahrenheit(c: float) -> float:
    """Convierte grados Celsius a Fahrenheit."""
    return round((c * 9 / 5) + 32, 2)


def fahrenheit_to_celsius(f: float) -> float:
    """Convierte grados Fahrenheit a Celsius y redondea a 2 decimales."""
    return round((f - 32) * 5 / 9, 2)