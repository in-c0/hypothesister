import math

import pytest

from cleancoin_lab.surface_coupling import (
    coupled_surface_integrity,
    coupled_surface_threshold_time_s,
    network_coupled_surface_integrity,
    network_coupled_surface_threshold_time_s,
    surface_advances_transport_failure,
)


def test_surface_loss_starts_from_transport_weakening_not_independent_clock():
    assert coupled_surface_integrity(0.0, 1200.0, 0.01, 1.0) == pytest.approx(1.0)
    assert coupled_surface_integrity(300.0, 1200.0, 0.01, 1.0) < 1.0


def test_zero_work_never_creates_surface_clock():
    assert math.isinf(coupled_surface_threshold_time_s(1200.0, 0.0, 1.0, 0.5))
    assert math.isinf(
        network_coupled_surface_threshold_time_s(1200.0, 0.0, 1.0, 0.5)
    )


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


def test_network_strength_coupling_recovers_old_model_when_strength_is_constant():
    old = coupled_surface_threshold_time_s(
        1200.0,
        0.001,
        1.0,
        0.5,
        coupling_exponent=1.0,
    )
    coupled = network_coupled_surface_threshold_time_s(
        1200.0,
        0.001,
        1.0,
        0.5,
        coupling_exponent=1.0,
        residual_strength_fraction=1.0,
        integration_steps=512,
    )
    assert coupled == pytest.approx(old, rel=5e-4)


def test_network_weakening_can_only_accelerate_surface_loss_vs_constant_strength():
    constant = network_coupled_surface_threshold_time_s(
        1500.0,
        0.001,
        1.0,
        0.5,
        residual_strength_fraction=1.0,
    )
    weakening = network_coupled_surface_threshold_time_s(
        1500.0,
        0.001,
        1.0,
        0.5,
        residual_strength_fraction=0.2,
    )
    assert weakening < constant


def test_network_coupled_threshold_reproduces_requested_integrity():
    t = network_coupled_surface_threshold_time_s(
        1800.0,
        0.002,
        1.0,
        0.6,
        residual_strength_fraction=0.3,
    )
    integrity = network_coupled_surface_integrity(
        t,
        1800.0,
        0.002,
        1.0,
        residual_strength_fraction=0.3,
    )
    assert integrity == pytest.approx(0.6, rel=1e-9)


def test_network_strength_parameters_are_bounded():
    with pytest.raises(ValueError):
        network_coupled_surface_integrity(
            60.0,
            1200.0,
            0.001,
            1.0,
            residual_strength_fraction=0.0,
        )
    with pytest.raises(ValueError):
        network_coupled_surface_integrity(
            60.0,
            1200.0,
            0.001,
            1.0,
            integration_steps=4,
        )
