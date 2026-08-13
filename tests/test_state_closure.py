import numpy as np

from cleancoin_lab.state_closure import StateClosureDesign, close_state_trajectory


def test_network_loss_lowers_equivalent_ca_and_modulus_and_raises_swelling_target():
    t = np.array([0.0, 300.0, 600.0])
    b = np.array([1.0, 0.7, 0.4])
    r = close_state_trajectory(t, b, StateClosureDesign())
    assert np.all(np.diff(r.source_equivalent_ca_mM) < 0)
    assert np.all(np.diff(r.plateau_modulus_Pa) < 0)
    assert np.all(np.diff(r.equilibrium_swelling_ratio) > 0)
    assert r.swelling_ratio[-1] > r.swelling_ratio[0]


def test_more_bound_network_starts_stiffer_and_less_swollen_at_equilibrium():
    t = np.array([0.0, 60.0])
    high = close_state_trajectory(t, np.array([0.9, 0.9]))
    low = close_state_trajectory(t, np.array([0.3, 0.3]))
    assert high.plateau_modulus_Pa[0] > low.plateau_modulus_Pa[0]
    assert high.equilibrium_swelling_ratio[0] < low.equilibrium_swelling_ratio[0]
