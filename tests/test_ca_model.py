import numpy as np

from cleancoin_lab.ca_model import CalciumDesign, simulate_calcium


def test_calcium_release_is_nonnegative_and_monotonic():
    r = simulate_calcium(CalciumDesign(), duration_s=600.0)
    assert np.all(r.released_ca_mM >= -1e-12)
    assert np.all(np.diff(r.released_ca_mM) >= -1e-10)


def test_bound_junction_fraction_does_not_grow():
    r = simulate_calcium(CalciumDesign(), duration_s=600.0)
    assert np.all((r.bound_fraction >= 0) & (r.bound_fraction <= 1 + 1e-12))
    assert np.all(np.diff(r.bound_fraction) <= 1e-10)


def test_mass_balance_is_closed_to_numerical_precision():
    r = simulate_calcium(CalciumDesign(), duration_s=600.0)
    assert np.max(np.abs(r.mass_balance_error_mol)) < 1e-12


def test_thinner_slab_hydrates_faster():
    thin = simulate_calcium(CalciumDesign(thickness_m=0.001), duration_s=600.0, dt_s=0.05)
    thick = simulate_calcium(CalciumDesign(thickness_m=0.004), duration_s=600.0)
    assert thin.value_at("hydration", 300.0) > thick.value_at("hydration", 300.0)
