"""Source-backed reference mechanics for calcium-alginate networks.

This module encodes only the narrow constitutive relations used by Grassi et al.
(2009), DOI 10.3390/molecules14083003, to map effective network crosslink
density to Young's modulus and equivalent-network mesh size.

Domain restriction
------------------
The Flory relation is used by that source for gels crosslinked in solution that
did not undergo further swelling/shrinking before mechanical testing. CleanCoin
is explicitly a swelling/de-crosslinking material, so these functions define an
*unswollen reference network* only. A swelling/ionic-state correction and a
mapping from calcium inventory to mechanically effective crosslinks are separate
research problems and are intentionally not hidden in this module.
"""

from __future__ import annotations

import math

R_GAS_J_MOL_K = 8.31446261815324
AVOGADRO_MOL_INV = 6.02214076e23


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
