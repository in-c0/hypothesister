"""A01 v0.3: preparation-history model with state-triggered chelate failure.

Primary evidence for HYP-001 A01 distinguishes three wet-state regimes:

1. swelling dominated by loss of temporary Ca2+ junctions;
2. an optional equilibrium/plateau regime; and
3. degradation after network expansion reaches a critical state and persistent
   chelate junctions begin to dissociate.

The v0.2 preparation/use model allowed strong junctions to dissociate from time
zero.  v0.3 removes that structural inconsistency.  It reuses v0.2's virtual
preparation and rinse stages, then adds a deliberately reduced-order
``expansion_proxy`` driven by temporary-junction loss relative to the persistent
junction scaffold. Persistent-junction dissociation is activated only when that
proxy crosses a shared critical threshold.

The expansion proxy is NOT a physical strain measurement. It is an explicit
placeholder for the missing swelling/poroelastic state and exists so source
phase-transition timings can falsify or constrain model structure before a full
continuum mechanics implementation is justified.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import math
import numpy as np

from .prepare_use_model import (
    PrepareUseDesign,
    PreparedState,
    prepare,
    rinse,
)


@dataclass(frozen=True)
class PhaseDesign:
    preparation: PrepareUseDesign = field(default_factory=PrepareUseDesign)

    # Reduced swelling/expansion state.  Defaults are exploratory only.
    expansion_relaxation_rate_s: float = 1.0e-4
    critical_expansion_proxy: float = 0.30
    activation_width: float = 0.03


@dataclass(frozen=True)
class PhaseUseResult:
    time_s: np.ndarray
    released_ca_mol: np.ndarray
    temporary_fraction: np.ndarray
    strong_fraction: np.ndarray
    expansion_proxy: np.ndarray
    strong_activation: np.ndarray
    degradation_onset_s: float

    def value_at(self, field: str, time_s: float) -> float:
        return float(np.interp(time_s, self.time_s, getattr(self, field)))


def _validate(design: PhaseDesign) -> None:
    if design.expansion_relaxation_rate_s <= 0:
        raise ValueError("expansion_relaxation_rate_s must be > 0")
    if design.critical_expansion_proxy <= 0:
        raise ValueError("critical_expansion_proxy must be > 0")
    if design.activation_width <= 0:
        raise ValueError("activation_width must be > 0")


def _alpha(d: PrepareUseDesign, dt_s: float, dx_m: float) -> float:
    alpha = d.mobile_ca_diffusivity_m2_s * dt_s / (dx_m * dx_m)
    if alpha > 0.5:
        raise ValueError(
            f"Explicit diffusion step unstable (D*dt/dx^2={alpha:.3g} > 0.5)"
        )
    return alpha


def _diffuse_mobile(mobile: np.ndarray, alpha: float) -> np.ndarray:
    lap = mobile[:-2] - 2.0 * mobile[1:-1] + mobile[2:]
    out = mobile.copy()
    out[1:-1] += alpha * lap
    out[0] = out[-1] = 0.0
    return np.maximum(out, 0.0)


def _activation(expansion: float, critical: float, width: float) -> float:
    z = np.clip((critical - expansion) / width, -60.0, 60.0)
    return float(1.0 / (1.0 + np.exp(z)))


def simulate_phase_use(
    design: PhaseDesign,
    initial_state: PreparedState,
    duration_s: float = 28_800.0,
    *,
    dt_s: float = 0.5,
    record_every_s: float = 10.0,
) -> PhaseUseResult:
    """Simulate wet use after preparation and rinse.

    Temporary junctions dissociate continuously. Their cumulative loss drives a
    low-order expansion state relative to the initial persistent-junction
    scaffold. Strong-junction loss is multiplied by a smooth activation term,
    becoming substantial only after the expansion state approaches the shared
    critical threshold.
    """
    _validate(design)
    p = design.preparation
    if duration_s < 0 or dt_s <= 0 or record_every_s <= 0:
        raise ValueError("invalid time arguments")

    dx = initial_state.dx_m
    alpha = _alpha(p, dt_s, dx)

    mobile = initial_state.mobile_ca_mol_m3.copy()
    temporary = initial_state.temporary_fraction.copy()
    strong = initial_state.strong_fraction.copy()
    temp_initial_mean = float(np.mean(temporary))
    strong_initial_mean = float(np.mean(strong))
    persistent_scale = max(strong_initial_mean, 1.0e-9)

    def total_ca_mol() -> float:
        concentration = p.junction_capacity_mol_m3 * (temporary + strong) + mobile
        return float(np.trapezoid(concentration, dx=dx) * p.exposed_area_m2)

    initial_total = total_ca_mol()
    expansion = 0.0
    onset = math.inf

    steps = int(np.ceil(duration_s / dt_s))
    stride = max(1, int(round(record_every_s / dt_s)))

    ts: list[float] = []
    released: list[float] = []
    temporary_out: list[float] = []
    strong_out: list[float] = []
    expansion_out: list[float] = []
    activation_out: list[float] = []

    for step in range(steps + 1):
        time = min(step * dt_s, duration_s)
        activation = _activation(
            expansion,
            design.critical_expansion_proxy,
            design.activation_width,
        )
        if activation >= 0.5 and math.isinf(onset):
            onset = time

        if step % stride == 0 or step == steps:
            ts.append(time)
            released.append(max(0.0, initial_total - total_ca_mol()))
            temporary_out.append(float(np.mean(temporary)))
            strong_out.append(float(np.mean(strong)))
            expansion_out.append(expansion)
            activation_out.append(activation)

        if step == steps:
            break

        local_dt = min(dt_s, duration_s - step * dt_s)

        temp_loss = temporary * (
            1.0 - np.exp(-p.temporary_dissociation_rate_s * local_dt)
        )
        strong_loss = strong * (
            1.0
            - np.exp(-p.strong_dissociation_rate_s * activation * local_dt)
        )
        temporary -= temp_loss
        strong -= strong_loss

        mobile = _diffuse_mobile(mobile, alpha * (local_dt / dt_s))
        mobile += p.junction_capacity_mol_m3 * (temp_loss + strong_loss)
        mobile = np.maximum(mobile, 0.0)
        mobile[0] = mobile[-1] = 0.0

        # Fixed-charge / expansion-drive proxy: cumulative temporary-junction
        # loss normalized by the persistent scaffold established during
        # preparation.  A first-order relaxation represents delayed lattice
        # expansion without pretending to resolve poroelastic mechanics.
        lost_temp_mean = max(0.0, temp_initial_mean - float(np.mean(temporary)))
        drive = lost_temp_mean / persistent_scale
        relax = 1.0 - math.exp(-design.expansion_relaxation_rate_s * local_dt)
        expansion += (drive - expansion) * relax

    return PhaseUseResult(
        time_s=np.asarray(ts),
        released_ca_mol=np.asarray(released),
        temporary_fraction=np.asarray(temporary_out),
        strong_fraction=np.asarray(strong_out),
        expansion_proxy=np.asarray(expansion_out),
        strong_activation=np.asarray(activation_out),
        degradation_onset_s=float(onset),
    )


def prepare_rinse_phase_use(
    design: PhaseDesign,
    crosslink_duration_s: float,
    *,
    rinse_duration_s: float = 60.0,
    use_duration_s: float = 28_800.0,
    dt_s: float = 0.5,
    nodes: int = 21,
    record_every_s: float = 10.0,
) -> tuple[PreparedState, PreparedState, PhaseUseResult]:
    """Run virtual ionotropic preparation, source-matched rinse, then v0.3 use."""
    prepared = prepare(
        design.preparation,
        crosslink_duration_s,
        dt_s=dt_s,
        nodes=nodes,
    )
    rinsed = rinse(
        design.preparation,
        prepared,
        rinse_duration_s,
        dt_s=dt_s,
    )
    result = simulate_phase_use(
        design,
        rinsed,
        use_duration_s,
        dt_s=dt_s,
        record_every_s=record_every_s,
    )
    return prepared, rinsed, result
