import math


def planar_front_time_s(capacity_mol_m3, path_m, diffusivity_m2_s, boundary_concentration_mol_m3):
    """Quasi-steady moving-front estimate: t = B L^2 / (2 D C0)."""
    if capacity_mol_m3 <= 0 or path_m < 0 or diffusivity_m2_s <= 0 or boundary_concentration_mol_m3 <= 0:
        raise ValueError("invalid chelation-front inputs")
    return capacity_mol_m3 * path_m**2 / (2.0 * diffusivity_m2_s * boundary_concentration_mol_m3)


def planar_path_for_time_m(capacity_mol_m3, time_s, diffusivity_m2_s, boundary_concentration_mol_m3):
    if capacity_mol_m3 <= 0 or time_s < 0 or diffusivity_m2_s <= 0 or boundary_concentration_mol_m3 <= 0:
        raise ValueError("invalid chelation-front inputs")
    return math.sqrt(2.0 * diffusivity_m2_s * boundary_concentration_mol_m3 * time_s / capacity_mol_m3)
