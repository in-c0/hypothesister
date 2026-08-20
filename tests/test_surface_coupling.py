import math

import pytest

from cleancoin_lab.surface_coupling import (
    coupled_surface_integrity,
    coupled_surface_threshold_time_s,
    surface_advances_transport_failure,
)


def test_surface_loss_starts_from_transport_weakening_not_independent_clock():
    assert coupled_surface_integrity(0.0, 1200.0, 0.01, 1.0) == pytest.approx(1.0)
    assert coupled_surface_integrity(300.0, 1200.0, 0.01, 1.0) < 1.0


def test_zero_work_never_creates_surface_clock():
    assert math.isinf(coupled_surface_threshold_time_s(1200.0, 0.0, 1.0, 0.5))


def test_stronger_interface_delays_threshold():
    weak = coupled_surface_threshold_time_s(1200.0, 0.01, 0.5, 0.5)
    strong = coupled_surface_threshold_time_s(1200.0, 0.01, 2.0, 0.5)
    assert strong > weak


def test_screen_distinguishes_material_and_secondary_surface_modes():
    assert surface_advances_transport_failure(1200.0, 0.01, 0.5, 0.5)
    assert not surface_advances_transport_failure(1200.0, 0.0001, 2.0, 0.5)


def test_threshold_reproduces_requested_integrity():
    t = coupled_surface_threshold_time_s(1800.0, 0.002, 1.0, 0.6)
    assert coupled_surface_integrity(t, 1800.0, 0.002, 1.0) == pytest.approx(0.6)
