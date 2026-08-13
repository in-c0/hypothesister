"""Source-backed reference mechanics for calcium-alginate networks.

This module intentionally keeps two distinct constitutive descriptions separate:

1. Grassi et al. (2009), DOI 10.3390/molecules14083003, maps an *effective*
   network crosslink density to an unswollen reference Young's modulus and mesh
   size.
2. Liu et al. (2015), DOI 10.1016/j.carbpol.2015.08.086, reports an
   alginate-specific stable-gel scaling law in which the plateau modulus obeys
   ``G_e = k * epsilon**1.5`` as calcium concentration moves above the gel
   point.

Domain restriction
------------------
The Flory relation used by Grassi et al. applies to solution-crosslinked gels
that did not undergo further swelling/shrinking before mechanical testing.
CleanCoin is explicitly a swelling/de-crosslinking material, so those functions
define an *unswollen reference network* only.

The calcium scaling law is likewise not a mapping from *total calcium inventory*
to modulus. ``calcium_concentration`` and ``critical_calcium_concentration``
must refer to the same experimentally meaningful gelling variable. Converting
A01's simulated temporary/strong junction state into that variable remains a
separate calibration problem.
"""

from __future__ import annotations

import math

R_GAS_J_MOL_K = 8.31446261815324
AVOGADRO_MOL_INV = 6.02214076e23
ALG_CA_PLATEAU_EXPONENT = 1.5


def young_modulus_from_crosslink_density(
    crosslink_density_mol_m3: float,
    temperature_K: float = 298.15,
) -> float:
    """Return unswollen reference Young's modulus in Pa.

    Uses the Flory/equivalent-network relation numerically reported in Grassi
    et al. (2009): ``E = 3 R T rho_x``.
    """
    if crosslink_density_mol_m3 < 0:
        raise ValueError("crosslink density must be >= 0")
    if temperature_K <= 0:
        raise ValueError("temperature_K must be > 0")
    return 3.0 * R_GAS_J_MOL_K * temperature_K * crosslink_density_mol_m3


def crosslink_density_from_young_modulus(
    young_modulus_Pa: float,
    temperature_K: float = 298.15,
) -> float:
    """Invert the reference Flory relation and return mol/m^3."""
    if young_modulus_Pa < 0:
        raise ValueError("Young's modulus must be >= 0")
    if temperature_K <= 0:
        raise ValueError("temperature_K must be > 0")
    return young_modulus_Pa / (3.0 * R_GAS_J_MOL_K * temperature_K)


def mesh_size_from_crosslink_density(
    crosslink_density_mol_m3: float,
) -> float:
    """Return equivalent-network spherical mesh diameter in metres.

    Grassi et al. use the equivalent-network construction in which the volume
    assigned to one crosslink is ``1 / (N_A rho_x)`` and is represented by a
    sphere whose diameter is the mean mesh size. Therefore:

        xi = (6 / (pi N_A rho_x)) ** (1/3)

    ``rho_x = 0`` corresponds to an unbounded mesh and returns ``inf``.
    """
    if crosslink_density_mol_m3 < 0:
        raise ValueError("crosslink density must be >= 0")
    if crosslink_density_mol_m3 == 0:
        return math.inf
    return (
        6.0
        / (math.pi * AVOGADRO_MOL_INV * crosslink_density_mol_m3)
    ) ** (1.0 / 3.0)


def reduced_calcium_distance(
    calcium_concentration: float,
    critical_calcium_concentration: float,
) -> float:
    """Return epsilon, the relative distance of calcium from the gel point.

    ``epsilon = (C_Ca - C_Ca,gel) / C_Ca,gel``.

    The value is clipped at zero because the Liu et al. stable-gel scaling is
    defined on the gel side of the transition; this function does not attempt
    to model the sol state.
    """
    if calcium_concentration < 0:
        raise ValueError("calcium_concentration must be >= 0")
    if critical_calcium_concentration <= 0:
        raise ValueError("critical_calcium_concentration must be > 0")
    return max(
        0.0,
        (calcium_concentration - critical_calcium_concentration)
        / critical_calcium_concentration,
    )


def plateau_modulus_from_calcium_distance(
    calcium_concentration: float,
    critical_calcium_concentration: float,
    modulus_prefactor_Pa: float,
) -> float:
    """Return alginate plateau modulus from the source-reported scaling law.

    Liu et al. (2015) report ``G_e = k * epsilon**1.5`` for stable calcium
    alginate gels, where epsilon is the relative distance of Ca2+ concentration
    from the gel point. ``modulus_prefactor_Pa`` is formulation-specific and
    must be calibrated rather than treated as universal.
    """
    if modulus_prefactor_Pa < 0:
        raise ValueError("modulus_prefactor_Pa must be >= 0")
    epsilon = reduced_calcium_distance(
        calcium_concentration,
        critical_calcium_concentration,
    )
    return modulus_prefactor_Pa * epsilon**ALG_CA_PLATEAU_EXPONENT
