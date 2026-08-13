import math


def diffusion_time_s(length_m: float, diffusivity_m2_s: float) -> float:
    if length_m < 0 or diffusivity_m2_s <= 0:
        raise ValueError("invalid transport inputs")
    return length_m * length_m / diffusivity_m2_s


def diffusion_length_m(time_s: float, diffusivity_m2_s: float) -> float:
    if time_s < 0 or diffusivity_m2_s <= 0:
        raise ValueError("invalid transport inputs")
    return math.sqrt(diffusivity_m2_s * time_s)
