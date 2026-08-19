import math

import pytest

from cleancoin_lab.surface_integrity import surface_integrity, surface_threshold_time_s


def test_intact_network_does_not_activate_surface_loss():
    assert surface_integrity(1800.0, 1.0, 0.01, 1.0) == pytest.approx(1.0)
    assert math.isinf(surface_threshold_time_s(1.0, 0.01, 1.0, 0.5))


def test_zero_tangential_work_does_not_activate_surface_loss():
    assert surface_integrity(1800.0, 0.5, 0.0, 1.0) == pytest.approx(1.0)


def test_weaker_network_accelerates_surface_threshold():
    stronger = surface_threshold_time_s(0.8, 0.01, 1.0, 0.5)
    weaker = surface_threshold_time_s(0.4, 0.01, 1.0, 0.5)
    assert weaker < stronger


def test_interface_strength_is_independent_sensitivity_axis():
    weak_interface = surface_threshold_time_s(0.5, 0.01, 0.5, 0.5)
    strong_interface = surface_threshold_time_s(0.5, 0.01, 2.0, 0.5)
    assert strong_interface == pytest.approx(4.0 * weak_interface)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"time_s": -1, "network_state": 0.5, "tangential_work_rate": 0.01, "interface_strength": 1.0},
        {"time_s": 1, "network_state": 1.1, "tangential_work_rate": 0.01, "interface_strength": 1.0},
        {"time_s": 1, "network_state": 0.5, "tangential_work_rate": -0.01, "interface_strength": 1.0},
        {"time_s": 1, "network_state": 0.5, "tangential_work_rate": 0.01, "interface_strength": 0.0},
    ],
)
def test_surface_integrity_rejects_invalid_inputs(kwargs):
    with pytest.raises(ValueError):
        surface_integrity(**kwargs)
