from __future__ import annotations

import math

PAIR_PARAMS = {
    "GG-GG": {"r_min_nm": 0.60, "epsilon_kJ_mol": 22.0, "attractive": True},
    "MM-MM": {"r_min_nm": 0.70, "epsilon_kJ_mol": 3.0, "attractive": True},
    "XX": {"r_min_nm": 0.70, "epsilon_kJ_mol": 1.0, "attractive": False},
}
CUTOFF_NM = 1.50


def sigma_from_minimum_nm(r_min_nm: float) -> float:
    if r_min_nm <= 0:
        raise ValueError("r_min_nm must be > 0")
    return r_min_nm / (2.0 ** (1.0 / 6.0))


def raw_lj_kj_mol(r_nm: float, r_min_nm: float, epsilon_kJ_mol: float) -> float:
    if r_nm <= 0 or r_min_nm <= 0 or epsilon_kJ_mol < 0:
        raise ValueError("invalid Lennard-Jones inputs")
    sigma = sigma_from_minimum_nm(r_min_nm)
    x = sigma / r_nm
    return 4.0 * epsilon_kJ_mol * (x**12 - x**6)


def shifted_attractive_lj_kj_mol(
    r_nm: float,
    r_min_nm: float,
    epsilon_kJ_mol: float,
    cutoff_nm: float = CUTOFF_NM,
) -> float:
    if cutoff_nm <= r_min_nm:
        raise ValueError("cutoff must exceed potential minimum")
    if r_nm >= cutoff_nm:
        return 0.0
    return raw_lj_kj_mol(r_nm, r_min_nm, epsilon_kJ_mol) - raw_lj_kj_mol(
        cutoff_nm, r_min_nm, epsilon_kJ_mol
    )


def repulsive_only_lj_kj_mol(r_nm: float, r_min_nm: float, epsilon_kJ_mol: float) -> float:
    if r_nm >= r_min_nm:
        return 0.0
    return raw_lj_kj_mol(r_nm, r_min_nm, epsilon_kJ_mol) + epsilon_kJ_mol
