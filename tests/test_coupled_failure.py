import numpy as np
import pytest

from cleancoin_lab.contact_load import damage_onset_state
from cleancoin_lab.coupled_failure import (
    coupled_collective_failure_time_s,
    coupled_local_failure_times_s,
    failure_time_from_front_state,
    retained_path_state,
)


def test_failure_time_hits_contact_onset_state_on_transport_front():
    front_time = 2_400.0
    onset = damage_onset_state(0.05, 1.4, 0.35)
    failure_time = failure_time_from_front_state(front_time, onset)
    assert retained_path_state(failure_time, front_time) == pytest.approx(onset)


def test_zero_load_leaves_transport_as_full_local_failure_time():
    front = np.array([600.0, 1_200.0, 2_400.0])
    result = coupled_local_failure_times_s(front, 0.0, 1.0, 0.4)
    assert np.array_equal(result, front)


def test_load_beyond_initial_threshold_fails_immediately():
    front = np.array([600.0, 1_200.0])
    result = coupled_local_failure_times_s(front, 0.5, 2.0, 0.25)
    assert np.array_equal(result, np.zeros_like(front))


def test_stronger_contact_advances_but_never_delays_transport_failure():
    front = np.array([900.0, 1_800.0, 3_600.0])
    weak = coupled_local_failure_times_s(front, 0.03, 1.0, 0.4)
    strong = coupled_local_failure_times_s(front, 0.12, 1.0, 0.4)
    assert np.all(strong < weak)
    assert np.all(weak <= front)
    assert np.all(strong <= front)


def test_transport_rescaling_rescales_failure_without_new_mechanical_clock():
    front = np.array([700.0, 1_000.0, 1_500.0, 2_000.0])
    base = coupled_local_failure_times_s(front, 0.06, 1.3, 0.35)
    scaled = coupled_local_failure_times_s(3.0 * front, 0.06, 1.3, 0.35)
    assert scaled == pytest.approx(3.0 * base)

    collective = coupled_collective_failure_time_s(
        front, 0.06, 1.3, 0.35, retained_connectivity_threshold=0.65
    )
    collective_scaled = coupled_collective_failure_time_s(
        3.0 * front, 0.06, 1.3, 0.35, retained_connectivity_threshold=0.65
    )
    assert collective_scaled == pytest.approx(3.0 * collective)


def test_collective_failure_reuses_existing_failed_fraction_quantile():
    front = np.array([100.0, 200.0, 300.0, 400.0, 500.0])
    local = coupled_local_failure_times_s(front, 0.05, 1.0, 0.4)
    result = coupled_collective_failure_time_s(
        front, 0.05, 1.0, 0.4, retained_connectivity_threshold=0.6
    )
    assert result == pytest.approx(np.quantile(local, 0.4))


def test_invalid_coupled_inputs_are_rejected():
    with pytest.raises(ValueError):
        retained_path_state(-1.0, 10.0)
    with pytest.raises(ValueError):
        failure_time_from_front_state(0.0, 0.5)
    with pytest.raises(ValueError):
        coupled_local_failure_times_s([1.0, -1.0], 0.1, 1.0, 0.3)
    with pytest.raises(ValueError):
        coupled_collective_failure_time_s(
            np.ones((2, 2)), 0.1, 1.0, 0.3, retained_connectivity_threshold=0.5
        )
