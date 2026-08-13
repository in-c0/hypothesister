"""RQ-002 closure: junction trajectory -> source-equivalent Ca -> Q and G_e.

This is deliberately feed-forward. It converts a simulated bound-junction
trajectory into observable swelling/mechanics states using source-backed
alginate closures. The junction->Ca mapping remains explicit and uncalibrated.
"""
from dataclasses import dataclass
import numpy as np

from .mechanics import plateau_modulus_from_calcium_distance
from .swelling import equilibrium_swelling_ratio_for_alginate, second_order_relaxation_step


@dataclass(frozen=True)
class StateClosureDesign:
    source_alginate: str = "LF240D"
    ca_floor_mM: float = 5.0
    ca_ceiling_mM: float = 20.0
    reference_bound_fraction: float = 1.0
    network_to_ca_exponent: float = 1.0
    swelling_beta_s_inv_ratio_inv: float = 5.0e-3
    gel_point_ca_mM: float = 5.0
    modulus_prefactor_Pa: float = 10_000.0


@dataclass(frozen=True)
class StateClosureResult:
    source_equivalent_ca_mM: np.ndarray
    equilibrium_swelling_ratio: np.ndarray
    swelling_ratio: np.ndarray
    plateau_modulus_Pa: np.ndarray


def _validate(d: StateClosureDesign) -> None:
    if d.ca_floor_mM <= 0 or d.ca_ceiling_mM <= d.ca_floor_mM:
        raise ValueError("invalid source-equivalent calcium range")
    if d.reference_bound_fraction <= 0 or d.network_to_ca_exponent <= 0:
        raise ValueError("invalid junction-to-calcium mapping")
    if d.swelling_beta_s_inv_ratio_inv < 0:
        raise ValueError("swelling beta must be >= 0")
    if d.gel_point_ca_mM <= 0 or d.modulus_prefactor_Pa < 0:
        raise ValueError("invalid mechanics closure")


def source_equivalent_calcium_mM(d: StateClosureDesign, bound_fraction: float) -> float:
    """Explicit reduced bridge; this is NOT total/free/bound Ca identity."""
    _validate(d)
    if bound_fraction < 0:
        raise ValueError("bound_fraction must be >= 0")
    x = min(1.0, bound_fraction / d.reference_bound_fraction)
    return d.ca_floor_mM + (d.ca_ceiling_mM - d.ca_floor_mM) * x**d.network_to_ca_exponent


def close_state_trajectory(
    time_s: np.ndarray,
    bound_fraction: np.ndarray,
    design: StateClosureDesign = StateClosureDesign(),
    initial_swelling_ratio: float = 1.0,
) -> StateClosureResult:
    """Map a monotonically sampled network trajectory into Q(t) and G_e(t)."""
    _validate(design)
    t = np.asarray(time_s, dtype=float)
    b = np.asarray(bound_fraction, dtype=float)
    if t.ndim != 1 or b.ndim != 1 or len(t) != len(b) or len(t) == 0:
        raise ValueError("time_s and bound_fraction must be equal non-empty vectors")
    if np.any(np.diff(t) < 0) or np.any(b < 0) or initial_swelling_ratio <= 0:
        raise ValueError("invalid trajectory")

    ca = np.array([source_equivalent_calcium_mM(design, x) for x in b])
    qeq = np.array([
        equilibrium_swelling_ratio_for_alginate(x, design.source_alginate) for x in ca
    ])
    modulus = np.array([
        plateau_modulus_from_calcium_distance(
            x, design.gel_point_ca_mM, design.modulus_prefactor_Pa
        ) for x in ca
    ])

    q = np.empty_like(t)
    q[0] = initial_swelling_ratio
    for i in range(1, len(t)):
        q[i] = second_order_relaxation_step(
            q[i - 1], qeq[i], design.swelling_beta_s_inv_ratio_inv, t[i] - t[i - 1]
        )
    return StateClosureResult(ca, qeq, q, modulus)
