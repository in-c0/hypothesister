"""RQ-003 reduced coupling of transport softening to mechanical failure.

The purpose of this module is structural: mechanics may advance final failure,
but it must not introduce a second independent clock.

The existing planar chelation-front model has penetration x(t) proportional to
sqrt(t).  If ``front_time_s`` is the time for that reduced front to traverse a
local transport path, then the remaining unpenetrated path fraction is

    n_path(t) = max(0, 1 - sqrt(t / front_time_s)).

For this coupling screen only, that retained-path fraction is used as the
normalized softening state consumed by ``contact_load.damage_onset_state``.
It is NOT claimed to be the true network connectivity or a calibrated modulus
state.  It simply couples the previously separate reduced models without
fitting an additional mechanical timescale.
"""
from __future__ import annotations

import numpy as np

from .collective_transition import transition_time_s
from .mechanics import ALG_CA_PLATEAU_EXPONENT


def retained_path_state(time_s: float, front_time_s: float) -> float:
    """Reduced remaining transport-path fraction under a planar sqrt(t) front."""
    if time_s < 0 or front_time_s <= 0:
        raise ValueError("time must be >= 0 and front_time_s must be > 0")
    return float(max(0.0, 1.0 - np.sqrt(time_s / front_time_s)))


def failure_time_from_front_state(front_time_s: float, onset_state: float) -> float:
    """Map a mechanical onset state onto the existing transport-front clock.

    ``onset_state >= 1`` means the reduced threshold is exceeded immediately.
    ``onset_state <= 0`` means mechanics never triggers before full front
    traversal, so transport alone sets the local failure time.
    """
    if front_time_s <= 0 or not np.isfinite(front_time_s):
        raise ValueError("front_time_s must be finite and > 0")
    if not np.isfinite(onset_state):
        raise ValueError("onset_state must be finite")
    if onset_state >= 1.0:
        return 0.0
    if onset_state <= 0.0:
        return float(front_time_s)
    return float(front_time_s * (1.0 - onset_state) ** 2)


def coupled_local_failure_times_s(
    front_times_s,
    dimensionless_load,
    localization_factor,
    failure_strain,
    *,
    modulus_exponent: float = ALG_CA_PLATEAU_EXPONENT,
) -> np.ndarray:
    """Return local failure times using transport as the only time base.

    Inputs may be scalars or broadcast-compatible arrays.  Contact parameters
    determine the network/path state at which failure accelerates; the local
    front time remains the sole dimensional clock.
    """
    if modulus_exponent <= 0:
        raise ValueError("modulus_exponent must be > 0")

    front, load, localization, failure = np.broadcast_arrays(
        np.asarray(front_times_s, dtype=float),
        np.asarray(dimensionless_load, dtype=float),
        np.asarray(localization_factor, dtype=float),
        np.asarray(failure_strain, dtype=float),
    )
    if np.any(~np.isfinite(front)) or np.any(front <= 0):
        raise ValueError("front times must be finite and > 0")
    if np.any(~np.isfinite(load)) or np.any(load < 0):
        raise ValueError("dimensionless load must be finite and >= 0")
    if np.any(~np.isfinite(localization)) or np.any(localization <= 0):
        raise ValueError("localization must be finite and > 0")
    if np.any(~np.isfinite(failure)) or np.any(failure <= 0):
        raise ValueError("failure strain must be finite and > 0")

    onset = (localization * load / failure) ** (1.0 / modulus_exponent)
    local_time = front * (1.0 - np.clip(onset, 0.0, 1.0)) ** 2
    return np.asarray(local_time, dtype=float)


def coupled_collective_failure_time_s(
    front_times_s,
    dimensionless_load,
    localization_factor,
    failure_strain,
    retained_connectivity_threshold: float,
    *,
    modulus_exponent: float = ALG_CA_PLATEAU_EXPONENT,
) -> float:
    """Apply the existing collective-transition quantile to coupled local times."""
    local = coupled_local_failure_times_s(
        front_times_s,
        dimensionless_load,
        localization_factor,
        failure_strain,
        modulus_exponent=modulus_exponent,
    )
    if local.ndim != 1:
        raise ValueError("collective failure requires one-dimensional local domains")
    return transition_time_s(local, retained_connectivity_threshold)
