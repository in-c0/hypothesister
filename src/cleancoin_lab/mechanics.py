"""Source-backed reference mechanics for calcium-alginate networks.

Two distinct descriptions are kept separate:

1. Grassi et al. (2009), DOI 10.3390/molecules14083003: effective network
   crosslink density -> unswollen Young's modulus and mesh size.
2. Liu et al. (2016), DOI 10.1016/j.carbpol.2015.08.086: stable-gel plateau
   modulus follows ``G_e = k * epsilon**1.5`` as the gelling variable moves
   above its critical gel point.

Yuguchi et al. (2000), DOI 10.1016/S0022-2860(00)00556-1, additionally show
that substantial local alginate association can precede formation of a
sample-spanning elastic network. Therefore total/local junction occupancy must
not be treated as mechanically effective crosslink density without an explicit
connectivity/gel-point mapping.
"""
from __future__ import annotations
import math

R_GAS_J_MOL_K = 8.31446261815324
AVOGADRO_MOL_INV = 6.02214076e23
ALG_CA_PLATEAU_EXPONENT = 1.5


def young_modulus_from_crosslink_density(crosslink_density_mol_m3: float, temperature_K: float = 298.15) -> float:
    if crosslink_density_mol_m3 < 0 or temperature_K <= 0:
        raise ValueError("invalid crosslink density or temperature")
    return 3.0 * R_GAS_J_MOL_K * temperature_K * crosslink_density_mol_m3


def crosslink_density_from_young_modulus(young_modulus_Pa: float, temperature_K: float = 298.15) -> float:
    if young_modulus_Pa < 0 or temperature_K <= 0:
        raise ValueError("invalid modulus or temperature")
    return young_modulus_Pa / (3.0 * R_GAS_J_MOL_K * temperature_K)


def mesh_size_from_crosslink_density(crosslink_density_mol_m3: float) -> float:
    if crosslink_density_mol_m3 < 0:
        raise ValueError("crosslink density must be >= 0")
    if crosslink_density_mol_m3 == 0:
        return math.inf
    return (6.0 / (math.pi * AVOGADRO_MOL_INV * crosslink_density_mol_m3)) ** (1.0 / 3.0)


def plateau_modulus_from_reduced_gelling_distance(epsilon: float, modulus_prefactor_Pa: float) -> float:
    """Apply the source-reported stable-gel ``k*epsilon^1.5`` scaling."""
    if epsilon < 0 or modulus_prefactor_Pa < 0:
        raise ValueError("epsilon and modulus prefactor must be >= 0")
    return modulus_prefactor_Pa * epsilon**ALG_CA_PLATEAU_EXPONENT


def reduced_calcium_distance(calcium_concentration: float, critical_calcium_concentration: float) -> float:
    if calcium_concentration < 0 or critical_calcium_concentration <= 0:
        raise ValueError("invalid calcium concentrations")
    return max(0.0, (calcium_concentration - critical_calcium_concentration) / critical_calcium_concentration)


def plateau_modulus_from_calcium_distance(calcium_concentration: float, critical_calcium_concentration: float, modulus_prefactor_Pa: float) -> float:
    epsilon = reduced_calcium_distance(calcium_concentration, critical_calcium_concentration)
    return plateau_modulus_from_reduced_gelling_distance(epsilon, modulus_prefactor_Pa)
