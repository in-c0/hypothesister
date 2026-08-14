"""RQ-003 reduced contact-load sensitivity model.

This module asks a narrow falsification question: can a mechanics threshold be a
robust lifecycle timer once user/contact uncertainty is exposed, or is it better
interpreted as a terminal accelerator after chemistry/transport has already
softened the network?

The model is deliberately dimensionless.  It does NOT calibrate a CleanCoin
hand force, contact area, friction coefficient, failure strain, or lifetime.
Those quantities are not yet source-constrained for the proposed product.

Let

    lambda = F / (E0 * A_eff)

be the nominal dimensionless contact load, and let C collect geometry,
friction and poroelastic localisation effects.  With the current source-backed
stable-gel scaling E/E0 = n^p and p = 1.5, the reduced local strain is

    epsilon_local = C * lambda * n^-p.

Damage onset at epsilon_local = epsilon_c therefore occurs at

    n* = (C * lambda / epsilon_c)^(1/p).

For the intentionally simple softening law n(t) = exp(-t/tau), this gives an
analytic threshold time.  The exponential law is a sensitivity scaffold, not a
claim about CleanCoin chemistry.
"""
from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np

from .mechanics import ALG_CA_PLATEAU_EXPONENT


@dataclass(frozen=True)
class ContactScreenResult:
    """Monte Carlo samples from the reduced contact-load screen."""

    dimensionless_load: np.ndarray
    localization_factor: np.ndarray
    failure_strain: np.ndarray
    softening_tau_s: np.ndarray
    cycle_frequency_hz: np.ndarray
    onset_state: np.ndarray
    onset_time_s: np.ndarray
    cycles_at_onset: np.ndarray

    def fraction_in_window(self, lower_s: float, upper_s: float) -> float:
        if lower_s < 0 or upper_s <= lower_s:
            raise ValueError("invalid time window")
        inside = (self.onset_time_s >= lower_s) & (self.onset_time_s <= upper_s)
        return float(np.mean(inside))

    @property
    def fraction_failed_at_initial_state(self) -> float:
        return float(np.mean(self.onset_state >= 1.0))


def dimensionless_contact_load(
    force_N: float,
    initial_modulus_Pa: float,
    effective_area_m2: float,
) -> float:
    """Return F/(E0*A_eff) without asserting product-specific calibration."""
    if force_N < 0 or initial_modulus_Pa <= 0 or effective_area_m2 <= 0:
        raise ValueError("force must be >= 0; modulus and area must be > 0")
    return force_N / (initial_modulus_Pa * effective_area_m2)


def damage_onset_state(
    dimensionless_load_value: float,
    localization_factor: float,
    failure_strain: float,
    *,
    modulus_exponent: float = ALG_CA_PLATEAU_EXPONENT,
) -> float:
    """Return network state n* at which the reduced local strain reaches failure.

    Values >= 1 mean the assumed load/failure combination is already beyond the
    reduced threshold at the initial state.  The value is intentionally not
    clipped because that is useful falsification information.
    """
    if dimensionless_load_value < 0:
        raise ValueError("dimensionless load must be >= 0")
    if localization_factor <= 0 or failure_strain <= 0 or modulus_exponent <= 0:
        raise ValueError("localization, failure strain and exponent must be > 0")
    if dimensionless_load_value == 0:
        return 0.0
    return (
        localization_factor * dimensionless_load_value / failure_strain
    ) ** (1.0 / modulus_exponent)


def local_strain(
    network_state: float,
    dimensionless_load_value: float,
    localization_factor: float = 1.0,
    *,
    modulus_exponent: float = ALG_CA_PLATEAU_EXPONENT,
) -> float:
    """Reduced local strain C*lambda*n^-p at a mechanically effective state n."""
    if network_state <= 0:
        raise ValueError("network_state must be > 0")
    if dimensionless_load_value < 0 or localization_factor <= 0 or modulus_exponent <= 0:
        raise ValueError("invalid reduced contact parameters")
    return (
        localization_factor
        * dimensionless_load_value
        * network_state ** (-modulus_exponent)
    )


def exponential_threshold_time_s(
    dimensionless_load_value: float,
    localization_factor: float,
    failure_strain: float,
    softening_tau_s: float,
    *,
    modulus_exponent: float = ALG_CA_PLATEAU_EXPONENT,
) -> float:
    """Threshold time under n(t)=exp(-t/tau), solely for sensitivity analysis."""
    if softening_tau_s <= 0:
        raise ValueError("softening_tau_s must be > 0")
    onset = damage_onset_state(
        dimensionless_load_value,
        localization_factor,
        failure_strain,
        modulus_exponent=modulus_exponent,
    )
    if onset == 0.0:
        return math.inf
    if onset >= 1.0:
        return 0.0
    return -softening_tau_s * math.log(onset)


def _log_uniform(
    rng: np.random.Generator,
    low: float,
    high: float,
    size: int,
) -> np.ndarray:
    if low <= 0 or high <= low:
        raise ValueError("log-uniform bounds must satisfy 0 < low < high")
    return np.exp(rng.uniform(math.log(low), math.log(high), size=size))


def monte_carlo_contact_screen(
    n_samples: int = 100_000,
    *,
    seed: int = 0,
    dimensionless_load_range: tuple[float, float] = (0.02, 0.30),
    localization_factor_range: tuple[float, float] = (0.5, 3.0),
    failure_strain_range: tuple[float, float] = (0.25, 0.50),
    softening_tau_s_range: tuple[float, float] = (900.0, 2700.0),
    cycle_frequency_hz_range: tuple[float, float] = (0.2, 2.0),
    modulus_exponent: float = ALG_CA_PLATEAU_EXPONENT,
) -> ContactScreenResult:
    """Sample a broad reduced uncertainty envelope without fitting to a target.

    Loads and localisation factors are log-uniform because their uncertainty is
    multiplicative.  Failure strain, softening timescale and cycle frequency
    are uniform over caller-supplied ranges.  Cycle frequency does not change
    the threshold time in this reduced model; it reports how many loading
    cycles have occurred by chemically governed onset, making that modelling
    boundary explicit.
    """
    if n_samples <= 0:
        raise ValueError("n_samples must be > 0")
    if failure_strain_range[0] <= 0 or failure_strain_range[1] <= failure_strain_range[0]:
        raise ValueError("invalid failure_strain_range")
    if softening_tau_s_range[0] <= 0 or softening_tau_s_range[1] <= softening_tau_s_range[0]:
        raise ValueError("invalid softening_tau_s_range")
    if cycle_frequency_hz_range[0] <= 0 or cycle_frequency_hz_range[1] <= cycle_frequency_hz_range[0]:
        raise ValueError("invalid cycle_frequency_hz_range")
    if modulus_exponent <= 0:
        raise ValueError("modulus_exponent must be > 0")

    rng = np.random.default_rng(seed)
    load = _log_uniform(rng, *dimensionless_load_range, n_samples)
    localization = _log_uniform(rng, *localization_factor_range, n_samples)
    failure = rng.uniform(*failure_strain_range, size=n_samples)
    tau = rng.uniform(*softening_tau_s_range, size=n_samples)
    frequency = rng.uniform(*cycle_frequency_hz_range, size=n_samples)

    onset = (localization * load / failure) ** (1.0 / modulus_exponent)
    onset_time = np.where(onset >= 1.0, 0.0, -tau * np.log(onset))
    cycles = onset_time * frequency

    return ContactScreenResult(
        dimensionless_load=load,
        localization_factor=localization,
        failure_strain=failure,
        softening_tau_s=tau,
        cycle_frequency_hz=frequency,
        onset_state=onset,
        onset_time_s=onset_time,
        cycles_at_onset=cycles,
    )
