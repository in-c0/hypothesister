"""Two-stage preparation -> rinse/use model for calcium-alginate A01.

This v0.2 model exists to test a specific model-structure hypothesis supported
by primary literature: calcium-crosslinking duration changes the *spatial
network state* of alginate, not merely its total calcium inventory.

Stage 1: preparation / ionotropic gelation
------------------------------------------
Mobile Ca2+ diffuses inward from a CaCl2 bath, occupies available junction
capacity, and temporary junctions may mature into a more persistent population.

Stage 2: rinse + use
--------------------
Boundary conditions switch to a calcium-free sink. Temporary and strong
junction populations dissociate at different rates and released mobile Ca2+
diffuses outward. External release is recovered by calcium mass loss from the
simulated material domain.

This remains an intentionally reduced model. Parameters are NOT calibrated,
and its absolute predictions MUST NOT be treated as HYP-001 evidence. In
particular, the temporary->strong maturation state is a coarse-grained proxy
for preparation-induced topology, not a claim that calcium-alginate chemistry
literally follows a two-state reaction pathway.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class PrepareUseDesign:
    thickness_m: float = 0.002
    exposed_area_m2: float = 1.0e-3
    ca_bath_mol_m3: float = 100.0  # 100 mM
    junction_capacity_mol_m3: float = 60.0

    mobile_ca_diffusivity_m2_s: float = 9.0e-10
    binding_rate_m3_mol_s: float = 8.0e-4
    maturation_rate_s: float = 8.0e-3

    temporary_dissociation_rate_s: float = 8.0e-4
    strong_dissociation_rate_s: float = 1.0e-4


@dataclass(frozen=True)
class PreparedState:
    mobile_ca_mol_m3: np.ndarray
    free_fraction: np.ndarray
    temporary_fraction: np.ndarray
    strong_fraction: np.ndarray
    dx_m: float

    @property
    def mean_bound_fraction(self) -> float:
        return float(np.mean(self.temporary_fraction + self.strong_fraction))

    @property
    def mean_temporary_fraction(self) -> float:
        return float(np.mean(self.temporary_fraction))

    @property
    def mean_strong_fraction(self) -> float:
        return float(np.mean(self.strong_fraction))


@dataclass(frozen=True)
class UseResult:
    time_s: np.ndarray
    released_ca_mol: np.ndarray
    bound_fraction: np.ndarray
    temporary_fraction: np.ndarray
    strong_fraction: np.ndarray

    def value_at(self, field: str, time_s: float) -> float:
        return float(np.interp(time_s, self.time_s, getattr(self, field)))

    def normalized_release(self, reference_time_s: float) -> np.ndarray:
        reference = self.value_at("released_ca_mol", reference_time_s)
        if reference <= 0:
            raise ValueError("reference release must be > 0")
        return self.released_ca_mol / reference


def _validate(design: PrepareUseDesign) -> None:
    positive = {
        "thickness_m": design.thickness_m,
        "exposed_area_m2": design.exposed_area_m2,
        "ca_bath_mol_m3": design.ca_bath_mol_m3,
        "junction_capacity_mol_m3": design.junction_capacity_mol_m3,
        "mobile_ca_diffusivity_m2_s": design.mobile_ca_diffusivity_m2_s,
        "binding_rate_m3_mol_s": design.binding_rate_m3_mol_s,
    }
    for name, value in positive.items():
        if value <= 0:
            raise ValueError(f"{name} must be > 0")
    for name in (
        "maturation_rate_s",
        "temporary_dissociation_rate_s",
        "strong_dissociation_rate_s",
    ):
        if getattr(design, name) < 0:
            raise ValueError(f"{name} must be >= 0")


def _alpha(design: PrepareUseDesign, dt_s: float, dx_m: float) -> float:
    alpha = design.mobile_ca_diffusivity_m2_s * dt_s / (dx_m * dx_m)
    if alpha > 0.5:
        raise ValueError(
            f"Explicit diffusion step unstable (D*dt/dx^2={alpha:.3g} > 0.5)"
        )
    return alpha


def _diffuse_mobile(
    mobile: np.ndarray,
    alpha: float,
    boundary_concentration: float,
) -> np.ndarray:
    lap = mobile[:-2] - 2.0 * mobile[1:-1] + mobile[2:]
    out = mobile.copy()
    out[1:-1] += alpha * lap
    out[0] = boundary_concentration
    out[-1] = boundary_concentration
    return np.maximum(out, 0.0)


def prepare(
    design: PrepareUseDesign,
    crosslink_duration_s: float,
    *,
    dt_s: float = 0.5,
    nodes: int = 21,
) -> PreparedState:
    """Simulate Ca2+ ingress, binding, and preparation-state maturation."""
    _validate(design)
    if crosslink_duration_s < 0 or dt_s <= 0 or nodes < 5:
        raise ValueError("invalid duration, dt, or node count")

    dx = design.thickness_m / (nodes - 1)
    alpha = _alpha(design, dt_s, dx)

    mobile = np.zeros(nodes, dtype=float)
    free = np.ones(nodes, dtype=float)
    temporary = np.zeros(nodes, dtype=float)
    strong = np.zeros(nodes, dtype=float)

    steps = int(np.ceil(crosslink_duration_s / dt_s))
    for step in range(steps):
        local_dt = min(dt_s, crosslink_duration_s - step * dt_s)
        if local_dt <= 0:
            break

        mobile[0] = mobile[-1] = design.ca_bath_mol_m3

        # First-order site occupancy with local Ca concentration.  Exponential
        # integration keeps the fraction bounded even when surface binding is
        # fast relative to dt.
        form_fraction = free * (
            1.0 - np.exp(-design.binding_rate_m3_mol_s * mobile * local_dt)
        )
        mature_fraction = temporary * (
            1.0 - np.exp(-design.maturation_rate_s * local_dt)
        )

        free -= form_fraction
        temporary += form_fraction - mature_fraction
        strong += mature_fraction

        mobile = _diffuse_mobile(mobile, alpha * (local_dt / dt_s), design.ca_bath_mol_m3)
        mobile -= design.junction_capacity_mol_m3 * form_fraction
        mobile = np.maximum(mobile, 0.0)
        mobile[0] = mobile[-1] = design.ca_bath_mol_m3

    return PreparedState(
        mobile_ca_mol_m3=mobile,
        free_fraction=free,
        temporary_fraction=temporary,
        strong_fraction=strong,
        dx_m=dx,
    )


def _sink_step(
    design: PrepareUseDesign,
    state: PreparedState,
    dt_s: float,
    alpha: float,
) -> PreparedState:
    mobile = state.mobile_ca_mol_m3.copy()
    temporary = state.temporary_fraction.copy()
    strong = state.strong_fraction.copy()

    mobile[0] = mobile[-1] = 0.0

    temporary_loss = temporary * (
        1.0 - np.exp(-design.temporary_dissociation_rate_s * dt_s)
    )
    strong_loss = strong * (
        1.0 - np.exp(-design.strong_dissociation_rate_s * dt_s)
    )
    temporary -= temporary_loss
    strong -= strong_loss

    mobile = _diffuse_mobile(mobile, alpha, 0.0)
    mobile += design.junction_capacity_mol_m3 * (temporary_loss + strong_loss)
    mobile = np.maximum(mobile, 0.0)
    mobile[0] = mobile[-1] = 0.0

    return PreparedState(
        mobile_ca_mol_m3=mobile,
        free_fraction=state.free_fraction,
        temporary_fraction=temporary,
        strong_fraction=strong,
        dx_m=state.dx_m,
    )


def rinse(
    design: PrepareUseDesign,
    state: PreparedState,
    rinse_duration_s: float = 60.0,
    *,
    dt_s: float = 0.5,
) -> PreparedState:
    """Apply the source-matched calcium-free rinse before release measurement."""
    if rinse_duration_s < 0 or dt_s <= 0:
        raise ValueError("invalid rinse duration or dt")
    alpha = _alpha(design, dt_s, state.dx_m)
    current = state
    steps = int(np.ceil(rinse_duration_s / dt_s))
    for step in range(steps):
        local_dt = min(dt_s, rinse_duration_s - step * dt_s)
        if local_dt <= 0:
            break
        current = _sink_step(
            design,
            current,
            local_dt,
            alpha * (local_dt / dt_s),
        )
    return current


def simulate_use(
    design: PrepareUseDesign,
    initial_state: PreparedState,
    duration_s: float = 14_400.0,
    *,
    dt_s: float = 0.5,
    record_every_s: float = 10.0,
) -> UseResult:
    """Simulate calcium egress and junction loss after the rinse stage."""
    if duration_s < 0 or dt_s <= 0 or record_every_s <= 0:
        raise ValueError("invalid time arguments")
    alpha = _alpha(design, dt_s, initial_state.dx_m)

    def total_ca_mol(state: PreparedState) -> float:
        concentration = (
            design.junction_capacity_mol_m3
            * (state.temporary_fraction + state.strong_fraction)
            + state.mobile_ca_mol_m3
        )
        return float(
            np.trapezoid(concentration, dx=state.dx_m) * design.exposed_area_m2
        )

    initial_total = total_ca_mol(initial_state)
    current = initial_state
    stride = max(1, int(round(record_every_s / dt_s)))
    steps = int(np.ceil(duration_s / dt_s))

    ts: list[float] = []
    released: list[float] = []
    bound: list[float] = []
    temp: list[float] = []
    strong: list[float] = []

    for step in range(steps + 1):
        time = min(step * dt_s, duration_s)
        if step % stride == 0 or step == steps:
            remaining = total_ca_mol(current)
            ts.append(time)
            released.append(max(0.0, initial_total - remaining))
            temp_mean = float(np.mean(current.temporary_fraction))
            strong_mean = float(np.mean(current.strong_fraction))
            temp.append(temp_mean)
            strong.append(strong_mean)
            bound.append(temp_mean + strong_mean)

        if step == steps:
            break
        local_dt = min(dt_s, duration_s - step * dt_s)
        current = _sink_step(
            design,
            current,
            local_dt,
            alpha * (local_dt / dt_s),
        )

    return UseResult(
        time_s=np.asarray(ts),
        released_ca_mol=np.asarray(released),
        bound_fraction=np.asarray(bound),
        temporary_fraction=np.asarray(temp),
        strong_fraction=np.asarray(strong),
    )


def prepare_rinse_use(
    design: PrepareUseDesign,
    crosslink_duration_s: float,
    *,
    rinse_duration_s: float = 60.0,
    use_duration_s: float = 14_400.0,
    dt_s: float = 0.5,
    nodes: int = 21,
    record_every_s: float = 10.0,
) -> tuple[PreparedState, PreparedState, UseResult]:
    """Convenience wrapper returning pre-rinse, post-rinse, and use states."""
    prepared = prepare(
        design,
        crosslink_duration_s,
        dt_s=dt_s,
        nodes=nodes,
    )
    rinsed = rinse(
        design,
        prepared,
        rinse_duration_s,
        dt_s=dt_s,
    )
    result = simulate_use(
        design,
        rinsed,
        use_duration_s,
        dt_s=dt_s,
        record_every_s=record_every_s,
    )
    return prepared, rinsed, result
