import math

import numpy as np
import pytest

from cleancoin_lab.contact_load import (
    damage_onset_state,
    dimensionless_contact_load,
    exponential_threshold_time_s,
    local_strain,
    monte_carlo_contact_screen,
)
from cleancoin_lab.mechanics import ALG_CA_PLATEAU_EXPONENT


def test_dimensionless_contact_load_is_force_over_modulus_area():
    assert dimensionless_contact_load(0.2, 2_000.0, 1.0e-4) == pytest.approx(1.0)


def test_onset_state_is_exact_failure_crossing():
    load = 0.05
    localization = 1.4
    failure_strain = 0.35
    onset = damage_onset_state(load, localization, failure_strain)
    assert local_strain(onset, load, localization) == pytest.approx(failure_strain)


def test_doubling_contact_load_shifts_threshold_time_analytically():
    tau = 1_200.0
    low_load = 0.05
    high_load = 2.0 * low_load
    low_time = exponential_threshold_time_s(low_load, 1.0, 0.4, tau)
    high_time = exponential_threshold_time_s(high_load, 1.0, 0.4, tau)

    expected_shift = tau / ALG_CA_PLATEAU_EXPONENT * math.log(2.0)
    assert low_time - high_time == pytest.approx(expected_shift)


def test_zero_load_never_reaches_mechanical_threshold_in_reduced_model():
    assert math.isinf(exponential_threshold_time_s(0.0, 1.0, 0.4, 1_200.0))


def test_threshold_above_initial_state_reports_immediate_onset():
    assert damage_onset_state(0.5, 2.0, 0.25) > 1.0
    assert exponential_threshold_time_s(0.5, 2.0, 0.25, 1_200.0) == 0.0


def test_monte_carlo_screen_is_reproducible_and_exposes_broad_timing():
    first = monte_carlo_contact_screen(20_000, seed=7)
    second = monte_carlo_contact_screen(20_000, seed=7)

    assert np.array_equal(first.onset_time_s, second.onset_time_s)
    assert np.array_equal(first.dimensionless_load, second.dimensionless_load)

    in_target = first.fraction_in_window(600.0, 1_800.0)
    assert 0.0 < in_target < 1.0
    assert 0.0 < first.fraction_failed_at_initial_state < 1.0


def test_cycle_frequency_is_report_only_not_a_hidden_timer():
    slow = monte_carlo_contact_screen(
        2_000,
        seed=11,
        cycle_frequency_hz_range=(0.1, 0.2),
    )
    fast = monte_carlo_contact_screen(
        2_000,
        seed=11,
        cycle_frequency_hz_range=(2.0, 3.0),
    )

    # Frequency is sampled last and does not enter the threshold equation.
    assert np.array_equal(slow.onset_time_s, fast.onset_time_s)
    assert np.all(fast.cycles_at_onset >= slow.cycles_at_onset)


def test_invalid_contact_inputs_are_rejected():
    with pytest.raises(ValueError):
        dimensionless_contact_load(-1.0, 1.0, 1.0)
    with pytest.raises(ValueError):
        dimensionless_contact_load(1.0, 0.0, 1.0)
    with pytest.raises(ValueError):
        damage_onset_state(0.1, 0.0, 0.3)
    with pytest.raises(ValueError):
        local_strain(0.0, 0.1)
    with pytest.raises(ValueError):
        monte_carlo_contact_screen(0)
