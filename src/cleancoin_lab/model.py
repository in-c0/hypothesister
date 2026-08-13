"""Transparent 1-D hydration / sacrificial-network model.

IMPORTANT
---------
This is a mechanistic *workflow model*, not a calibrated materials model.
Its parameters are dimensionally explicit but currently exploratory. It exists
so literature-derived parameters can replace assumptions without changing the
research pipeline.

Equations (finite-difference approximation):

    dc/dt = D * d²c/dx²
    ds/dt = -(k_h * c + k_m * load(t)) * s

where c is normalized local water concentration and s is the fraction of
sacrificial network remaining. Normalized cohesion is approximated as a
weighted combination of a permanent network and the hydrated sacrificial
network. The model intentionally omits swelling mechanics, poroelasticity,
fracture, chemistry-specific kinetics, and geometry-dependent stress fields.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class Design:
    thickness_m: float = 0.004
    water_diffusivity_m2_s: float = 2.0e-9
    hydration_crosslink_rate_s: float = 2.5e-4
    mechanical_damage_rate_s: float = 3.0e-5
    permanent_network_fraction: float = 0.10
    initial_sacrificial_fraction: float = 0.90
    scrub_load: float = 1.0


@dataclass(frozen=True)
class SimulationResult:
    time_s: np.ndarray
    hydration: np.ndarray
    sacrificial_fraction: np.ndarray
    cohesion: np.ndarray

    def hydration_t50(self) -> float:
        idx = np.flatnonzero(self.hydration >= 0.5)
        return float(self.time_s[idx[0]]) if len(idx) else float("inf")

    def value_at(self, field: str, time_s: float) -> float:
        arr = getattr(self, field)
        return float(np.interp(time_s, self.time_s, arr))


def _load_profile(t: float, design: Design) -> float:
    """Standardized virtual use: cyclic-loading exposure between 60 s and 1200 s.

    This is currently an effective averaged loading term, not an explicit
    mechanical-cycle solver.
    """
    return design.scrub_load if 60.0 <= t <= 1200.0 else 0.0


def simulate(
    design: Design,
    duration_s: float = 2400.0,
    dt_s: float = 0.25,
    nodes: int = 41,
    record_every_s: float = 2.0,
) -> SimulationResult:
    if nodes < 5:
        raise ValueError("nodes must be >= 5")
    if not 0 <= design.permanent_network_fraction <= 1:
        raise ValueError("permanent_network_fraction must be in [0, 1]")
    if not 0 <= design.initial_sacrificial_fraction <= 1:
        raise ValueError("initial_sacrificial_fraction must be in [0, 1]")

    dx = design.thickness_m / (nodes - 1)
    stability = design.water_diffusivity_m2_s * dt_s / (dx * dx)
    if stability > 0.5:
        raise ValueError(
            f"Explicit diffusion step unstable (D*dt/dx^2={stability:.3g} > 0.5). "
            "Reduce dt_s or nodes, or use an implicit solver."
        )

    c = np.zeros(nodes, dtype=float)
    s = np.full(nodes, design.initial_sacrificial_fraction, dtype=float)

    steps = int(np.ceil(duration_s / dt_s))
    stride = max(1, int(round(record_every_s / dt_s)))
    ts, hydration, sacrificial, cohesion = [], [], [], []

    for step in range(steps + 1):
        t = step * dt_s

        # Both exposed faces are instantaneously wetted in v0.
        c[0] = 1.0
        c[-1] = 1.0

        if step % stride == 0:
            h = float(c.mean())
            sf = float(s.mean())
            # Permanent network becomes mechanically relevant as it hydrates;
            # sacrificial contribution decays according to s.
            coh = design.permanent_network_fraction * h + sf * h
            ts.append(t)
            hydration.append(h)
            sacrificial.append(sf)
            cohesion.append(coh)

        if step == steps:
            break

        lap = c[:-2] - 2.0 * c[1:-1] + c[2:]
        c_new = c.copy()
        c_new[1:-1] += design.water_diffusivity_m2_s * dt_s / (dx * dx) * lap
        c_new[0] = 1.0
        c_new[-1] = 1.0
        c = np.clip(c_new, 0.0, 1.0)

        rate = design.hydration_crosslink_rate_s * c + design.mechanical_damage_rate_s * _load_profile(t, design)
        s *= np.exp(-rate * dt_s)

    return SimulationResult(
        time_s=np.asarray(ts),
        hydration=np.asarray(hydration),
        sacrificial_fraction=np.asarray(sacrificial),
        cohesion=np.asarray(cohesion),
    )
