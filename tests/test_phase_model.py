import math
import numpy as np

from cleancoin_lab.phase_model import PhaseDesign, prepare_rinse_phase_use


def test_longer_preparation_delays_degradation_activation():
    design = PhaseDesign()
    _, _, one = prepare_rinse_phase_use(
        design,
        60.0,
        use_duration_s=8 * 3600.0,
    )
    _, _, five = prepare_rinse_phase_use(
        design,
        300.0,
        use_duration_s=8 * 3600.0,
    )

    assert math.isfinite(one.degradation_onset_s)
    assert five.degradation_onset_s > one.degradation_onset_s


def test_strong_failure_is_suppressed_initially():
    _, _, result = prepare_rinse_phase_use(
        PhaseDesign(),
        300.0,
        use_duration_s=600.0,
    )
    assert result.strong_activation[0] < 1e-3
    assert result.strong_fraction[-1] <= result.strong_fraction[0] + 1e-12


def test_release_remains_nonnegative_and_monotonic():
    _, _, result = prepare_rinse_phase_use(
        PhaseDesign(),
        60.0,
        use_duration_s=3600.0,
    )
    assert np.all(result.released_ca_mol >= -1e-15)
    assert np.all(np.diff(result.released_ca_mol) >= -1e-12)


def test_expansion_proxy_starts_at_zero_and_does_not_go_negative():
    _, _, result = prepare_rinse_phase_use(
        PhaseDesign(),
        60.0,
        use_duration_s=3600.0,
    )
    assert result.expansion_proxy[0] == 0.0
    assert np.all(result.expansion_proxy >= -1e-12)
