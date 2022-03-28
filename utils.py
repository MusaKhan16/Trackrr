from math import pi


def convert_to_radians(angle: float | int) -> float:
    """Converts degrees to radians"""
    return angle * (pi / 180)


def convert_metric_distance(conversion_metric: str) -> float | int:
    """Converts meters to another distance from a mapping"""

    conversion_mapping = {
        "mm": 1000,
        "cm": 100,
        "km": 0.01,
        "mi": 0.001,
    }
    return conversion_mapping.get(conversion_metric, 1)
