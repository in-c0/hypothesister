import numpy as np
from cleancoin_lab.model import Design, simulate
from cleancoin_lab.scoring import evaluate


def test_hydration_is_bounded_and_monotonic_on_average():
    r = simulate(Design(), duration_s=120.0)
    assert np.all((r.hydration >= 0) & (r.hydration <= 1))
    assert np.all(np.diff(r.hydration) >= -1e-12)


def test_sacrificial_network_does_not_grow():
    r = simulate(Design(), duration_s=120.0)
    assert np.all(np.diff(r.sacrificial_fraction) <= 1e-12)


def test_scoring_has_explicit_pass():
    r = simulate(Design())
    metrics = evaluate(r)
    assert "pass" in metrics
    assert 0 <= metrics["score"] <= 1
