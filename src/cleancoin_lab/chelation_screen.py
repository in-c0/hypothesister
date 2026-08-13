from __future__ import annotations

import numpy as np

from .chelation_front import planar_front_time_s
from .collective_transition import transition_time_s


def sample_local_times_s(
    rng,
    n,
    *,
    capacity_mol_m3,
    nominal_path_m,
    path_cv,
    diffusivity_m2_s,
    boundary_concentration_mol_m3,
):
    sigma = np.sqrt(np.log1p(path_cv**2))
    paths = nominal_path_m * np.exp(rng.normal(-0.5*sigma**2, sigma, n))
    return capacity_mol_m3 * paths**2 / (2.0*diffusivity_m2_s*boundary_concentration_mol_m3)


def one_product_transition_s(
    rng,
    *,
    capacity_mol_m3,
    nominal_path_m,
    path_cv,
    diffusivity_m2_s,
    boundary_concentration_mol_m3,
    retained_connectivity_threshold,
    domains=2000,
):
    times = sample_local_times_s(
        rng,
        domains,
        capacity_mol_m3=capacity_mol_m3,
        nominal_path_m=nominal_path_m,
        path_cv=path_cv,
        diffusivity_m2_s=diffusivity_m2_s,
        boundary_concentration_mol_m3=boundary_concentration_mol_m3,
    )
    return transition_time_s(times, retained_connectivity_threshold)
