"""RQ-002 feed-forward closure: junction trajectory -> observable Q and G_e.

Swelling and mechanics intentionally use different explicit bridges:
- swelling uses a source-equivalent calcium axis because the empirical Q(Ca)
  data require one;
- mechanics uses a connectivity/gel-point distance because SAXS+rheology show
  local junction association precedes formation of a sample-spanning network.
Neither bridge is yet a calibrated chemical identity.
"""
from dataclasses import dataclass
import numpy as np

from .mechanics import plateau_modulus_from_reduced_gelling_distance
from .swelling import equilibrium_swelling_ratio_for_alginate, second_order_relaxation_step


@dataclass(frozen=True)
class StateClosureDesign:
    source_alginate: str = "LF240D"
    ca_floor_mM: float = 5.0
    ca_ceiling_mM: float = 20.0
    reference_bound_fraction: float = 1.0
    network_to_ca_exponent: float = 1.0
    swelling_beta_s_inv_ratio_inv: float = 5.0e-3
    critical_bound_fraction: float = 0.10
    bound_to_gelling_distance_scale: float = 0.20
    modulus_prefactor_Pa: float = 10_000.0


@dataclass(frozen=True)
class StateClosureResult:
    source_equivalent_ca_mM: np.ndarray
    reduced_gelling_distance: np.ndarray
    equilibrium_swelling_ratio: np.ndarray
    swelling_ratio: np.ndarray
    plateau_modulus_Pa: np.ndarray


def _validate(d: StateClosureDesign) -> None:
    if d.ca_floor_mM <= 0 or d.ca_ceiling_mM <= d.ca_floor_mM:
        raise ValueError("invalid source-equivalent calcium range")
    if d.reference_bound_fraction <= 0 or d.network_to_ca_exponent <= 0:
        raise ValueError("invalid swelling-state mapping")
    if d.swelling_beta_s_inv_ratio_inv < 0:
        raise ValueError("swelling beta must be >= 0")
    if not 0 <= d.critical_bound_fraction < d.reference_bound_fraction:
        raise ValueError("invalid mechanical connectivity threshold")
    if d.bound_to_gelling_distance_scale <= 0 or d.modulus_prefactor_Pa < 0:
        raise ValueError("invalid mechanics mapping")


def source_equivalent_calcium_mM(d: StateClosureDesign, bound_fraction: float) -> float:
    """Reduced swelling bridge; not total/free/bound calcium identity."""
    _validate(d)
    if bound_fraction < 0:
        raise ValueError("bound_fraction must be >= 0")
    x = min(1.0, bound_fraction / d.reference_bound_fraction)
    return d.ca_floor_mM + (d.ca_ceiling_mM - d.ca_floor_mM) * x**d.network_to_ca_exponent


def reduced_network_gelling_distance(d: StateClosureDesign, bound_fraction: float) -> float:
    """Percolation-aware mechanical bridge, explicitly uncalibrated."""
    _validate(d)
    if bound_fraction < 0:
        raise ValueError("bound_fraction must be >= 0")
    return max(0.0, (bound_fraction - d.critical_bound_fraction) / d.bound_to_gelling_distance_scale)


def close_state_trajectory(time_s, bound_fraction, design=StateClosureDesign(), initial_swelling_ratio=1.0):
    """Map a sampled junction trajectory into empirical Q(t) and G_e(t)."""
    _validate(design)
    t = np.asarray(time_s, dtype=float)
    b = np.asarray(bound_fraction, dtype=float)
    if t.ndim != 1 or b.ndim != 1 or len(t) != len(b) or len(t) == 0:
        raise ValueError("time_s and bound_fraction must be equal non-empty vectors")
    if np.any(np.diff(t) < 0) or np.any(b < 0) or initial_swelling_ratio <= 0:
        raise ValueError("invalid trajectory")

    ca = np.array([source_equivalent_calcium_mM(design, x) for x in b])
    epsilon = np.array([reduced_network_gelling_distance(design, x) for x in b])
    qeq = np.array([equilibrium_swelling_ratio_for_alginate(x, design.source_alginate) for x in ca])
    modulus = np.array([
        plateau_modulus_from_reduced_gelling_distance(x, design.modulus_prefactor_Pa)
        for x in epsilon
    ])

    q = np.empty_like(t)
    q[0] = initial_swelling_ratio
    for i in range(1, len(t)):
        q[i] = second_order_relaxation_step(
            q[i - 1], qeq[i], design.swelling_beta_s_inv_ratio_inv, t[i] - t[i - 1]
        )
    return StateClosureResult(ca, epsilon, qeq, q, modulus)
