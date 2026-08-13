"""Reduced calcium/junction reaction-diffusion model for HYP-001 A01.

This model is deliberately intermediate fidelity.  It upgrades the original
single-rate sacrificial-network toy model by explicitly representing:

* hydration transport from both exposed faces;
* two populations of Ca2+-mediated junctions (temporary and strong/chelate);
* mobile Ca2+ released into the pore liquid;
* diffusion of mobile Ca2+ to an ideal well-stirred bath; and
* threshold-like activation of strong-junction loss after network weakening.

It is NOT calibrated yet.  Default values are exploratory and MUST NOT be used
to claim a CleanCoin lifetime.  The purpose of this module is to provide a
model whose observables can be fitted to source-specific calcium-release data
without pretending that an external-bath mM/min value is itself a universal
first-order crosslink-loss constant.

For a one-dimensional slab, x in [0, L]:

    dh/dt = D_w d2h/dx2

    db_t/dt = -k_t h b_t

    db_s/dt = -k_s h A(B) b_s

    dc_m/dt = D_ca d2c_m/dx2
               + C_t0 (-db_t/dt) + C_s0 (-db_s/dt)

where h is normalized hydration, b_t and b_s are fractions of the initial
junction populations, c_m is mobile Ca2+ concentration in the pore phase, and
A(B) is a smooth activation function that turns on strong-junction loss as the
remaining bound-junction fraction B falls below a configurable threshold.

Boundary conditions in v0.1:

    h(0,t) = h(L,t) = 1        (instantaneous wetting)
    c_m(0,t) = c_m(L,t) = 0    (ideal well-stirred infinite sink)

The bath concentration is recovered by mass balance.  Finite-bath transport,
swelling/poroelasticity, mechanical fatigue, ion rebinding, Na+/Ca2+ exchange,
and moving geometry are intentionally deferred.
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class CalciumDesign:
    thickness_m: float = 0.004
    exposed_area_m2: float = 1.0e-3
    bath_volume_L: float = 0.050

    water_diffusivity_m2_s: float = 2.0e-9
    mobile_ca_diffusivity_m2_s: float = 5.0e-10

    temporary_ca_mol_m3: float = 20.0
    strong_ca_mol_m3: float = 20.0
    temporary_dissociation_rate_s: float = 3.0e-4
    strong_dissociation_rate_s: float = 1.0e-4

    strong_activation_bound_fraction: float = 0.45
    strong_activation_width: float = 0.04


@dataclass(frozen=True)
class CalciumSimulationResult:
    time_s: np.ndarray
    hydration: np.ndarray
    temporary_fraction: np.ndarray
    strong_fraction: np.ndarray
    bound_fraction: np.ndarray
    internal_mobile_ca_mol: np.ndarray
    released_ca_mol: np.ndarray
    released_ca_mM: np.ndarray
    mass_balance_error_mol: np.ndarray

    def value_at(self, field: str, time_s: float) -> float:
        arr = getattr(self, field)
        return float(np.interp(time_s, self.time_s, arr))


def _activation(bound_fraction: np.ndarray, threshold: float, width: float) -> np.ndarray:
    """Smooth 0..1 activation of strong-junction loss below a bound threshold."""
    if width <= 0:
        raise ValueError("strong_activation_width must be > 0")
    z = np.clip((bound_fraction - threshold) / width, -60.0, 60.0)
    return 1.0 / (1.0 + np.exp(z))


def _validate_design(d: CalciumDesign) -> None:
    positive = {
        "thickness_m": d.thickness_m,
        "exposed_area_m2": d.exposed_area_m2,
        "bath_volume_L": d.bath_volume_L,
        "water_diffusivity_m2_s": d.water_diffusivity_m2_s,
        "mobile_ca_diffusivity_m2_s": d.mobile_ca_diffusivity_m2_s,
        "strong_activation_width": d.strong_activation_width,
    }
    for name, value in positive.items():
        if value <= 0:
            raise ValueError(f"{name} must be > 0")
    nonnegative = {
        "temporary_ca_mol_m3": d.temporary_ca_mol_m3,
        "strong_ca_mol_m3": d.strong_ca_mol_m3,
        "temporary_dissociation_rate_s": d.temporary_dissociation_rate_s,
        "strong_dissociation_rate_s": d.strong_dissociation_rate_s,
    }
    for name, value in nonnegative.items():
        if value < 0:
            raise ValueError(f"{name} must be >= 0")
    if d.temporary_ca_mol_m3 + d.strong_ca_mol_m3 <= 0:
        raise ValueError("initial bound calcium inventory must be > 0")
    if not 0 < d.strong_activation_bound_fraction < 1:
        raise ValueError("strong_activation_bound_fraction must be in (0, 1)")


def simulate_calcium(
    design: CalciumDesign,
    duration_s: float = 7200.0,
    dt_s: float = 0.25,
    nodes: int = 41,
    record_every_s: float = 5.0,
) -> CalciumSimulationResult:
    """Simulate the reduced A01 calcium/junction model.

    Explicit finite differences are used so every state transition remains
    inspectable.  The function rejects numerically unstable diffusion steps.
    """
    _validate_design(design)
    if nodes < 5:
        raise ValueError("nodes must be >= 5")
    if duration_s < 0 or dt_s <= 0 or record_every_s <= 0:
        raise ValueError("duration_s >= 0 and time steps > 0 are required")

    dx = design.thickness_m / (nodes - 1)
    alpha_w = design.water_diffusivity_m2_s * dt_s / (dx * dx)
    alpha_ca = design.mobile_ca_diffusivity_m2_s * dt_s / (dx * dx)
    if max(alpha_w, alpha_ca) > 0.5:
        raise ValueError(
            "Explicit diffusion step unstable: "
            f"max(D*dt/dx^2)={max(alpha_w, alpha_ca):.3g} > 0.5"
        )

    h = np.zeros(nodes, dtype=float)
    b_t = np.ones(nodes, dtype=float)
    b_s = np.ones(nodes, dtype=float)
    c_mobile = np.zeros(nodes, dtype=float)

    c_t0 = design.temporary_ca_mol_m3
    c_s0 = design.strong_ca_mol_m3
    c_total0 = c_t0 + c_s0

    material_volume_m3 = design.exposed_area_m2 * design.thickness_m
    initial_bound_mol = c_total0 * material_volume_m3

    steps = int(np.ceil(duration_s / dt_s))
    stride = max(1, int(round(record_every_s / dt_s)))

    ts: list[float] = []
    hydration: list[float] = []
    temp_frac: list[float] = []
    strong_frac: list[float] = []
    bound_frac_out: list[float] = []
    mobile_mol_out: list[float] = []
    released_mol_out: list[float] = []
    released_mM_out: list[float] = []
    mass_err_out: list[float] = []

    def volume_average(y: np.ndarray) -> float:
        return float(np.trapezoid(y, dx=dx) / design.thickness_m)

    def total_moles_from_concentration(y: np.ndarray) -> float:
        return float(np.trapezoid(y, dx=dx) * design.exposed_area_m2)

    for step in range(steps + 1):
        time = step * dt_s

        h[0] = h[-1] = 1.0
        c_mobile[0] = c_mobile[-1] = 0.0

        if step % stride == 0:
            bound_conc = c_t0 * b_t + c_s0 * b_s
            bound_mol = total_moles_from_concentration(bound_conc)
            mobile_mol = total_moles_from_concentration(c_mobile)
            released_mol = max(0.0, initial_bound_mol - bound_mol - mobile_mol)
            bath_mM = released_mol / design.bath_volume_L * 1000.0
            mass_error = initial_bound_mol - (bound_mol + mobile_mol + released_mol)

            ts.append(time)
            hydration.append(volume_average(h))
            temp_frac.append(volume_average(b_t))
            strong_frac.append(volume_average(b_s))
            bound_frac_out.append(bound_mol / initial_bound_mol)
            mobile_mol_out.append(mobile_mol)
            released_mol_out.append(released_mol)
            released_mM_out.append(bath_mM)
            mass_err_out.append(mass_error)

        if step == steps:
            break

        lap_h = h[:-2] - 2.0 * h[1:-1] + h[2:]
        h_new = h.copy()
        h_new[1:-1] += alpha_w * lap_h
        h_new[0] = h_new[-1] = 1.0
        h = np.clip(h_new, 0.0, 1.0)

        local_bound_fraction = (c_t0 * b_t + c_s0 * b_s) / c_total0
        activation = _activation(
            local_bound_fraction,
            design.strong_activation_bound_fraction,
            design.strong_activation_width,
        )

        temp_rate = design.temporary_dissociation_rate_s * h
        strong_rate = design.strong_dissociation_rate_s * h * activation

        b_t_new = b_t * np.exp(-temp_rate * dt_s)
        b_s_new = b_s * np.exp(-strong_rate * dt_s)

        released_source = (
            c_t0 * (b_t - b_t_new) + c_s0 * (b_s - b_s_new)
        ) / dt_s
        b_t = b_t_new
        b_s = b_s_new

        lap_ca = c_mobile[:-2] - 2.0 * c_mobile[1:-1] + c_mobile[2:]
        mobile_new = c_mobile.copy()
        mobile_new[1:-1] += alpha_ca * lap_ca
        mobile_new += released_source * dt_s
        mobile_new[0] = mobile_new[-1] = 0.0
        c_mobile = np.maximum(mobile_new, 0.0)

    return CalciumSimulationResult(
        time_s=np.asarray(ts),
        hydration=np.asarray(hydration),
        temporary_fraction=np.asarray(temp_frac),
        strong_fraction=np.asarray(strong_frac),
        bound_fraction=np.asarray(bound_frac_out),
        internal_mobile_ca_mol=np.asarray(mobile_mol_out),
        released_ca_mol=np.asarray(released_mol_out),
        released_ca_mM=np.asarray(released_mM_out),
        mass_balance_error_mol=np.asarray(mass_err_out),
    )
