import math


def remaining_fraction(tau: float, terms: int = 100) -> float:
    if tau < 0 or terms < 1:
        raise ValueError("invalid inputs")
    if tau == 0:
        return 1.0
    return (6.0/(math.pi**2))*sum(
        math.exp(-(n*n)*(math.pi**2)*tau)/(n*n)
        for n in range(1, terms + 1)
    )


def tau_from_time(time_s: float, diffusivity_m2_s: float, radius_m: float) -> float:
    if time_s < 0 or diffusivity_m2_s <= 0 or radius_m <= 0:
        raise ValueError("invalid inputs")
    return diffusivity_m2_s*time_s/(radius_m*radius_m)
