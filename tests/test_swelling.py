import pytest

from cleancoin_lab.swelling import (
    characteristic_half_time_s,
    equilibrium_swelling_ratio_for_alginate,
    second_order_progress,
    second_order_relaxation_step,
    source_lambda_from_k_meq,
)


def test_second_order_half_time():
    lam = source_lambda_from_k_meq(0.0013, 120.48)
    assert characteristic_half_time_s(lam) == pytest.approx(383.2, rel=0.01)
    assert second_order_progress(characteristic_half_time_s(lam), lam) == pytest.approx(0.5)


def test_low_g_equilibrium_swelling_decreases_with_source_calcium():
    q12 = equilibrium_swelling_ratio_for_alginate(12.5, "LF240D")
    q40 = equilibrium_swelling_ratio_for_alginate(40.0, "LF240D")
    assert q12 > q40
    assert q12 == pytest.approx(6.556 * 12.5**-0.509)


def test_second_order_relaxation_moves_toward_target_from_either_side():
    swelling = second_order_relaxation_step(1.0, 2.0, 0.01, 10.0)
    syneresis = second_order_relaxation_step(2.0, 1.0, 0.01, 10.0)
    assert 1.0 < swelling < 2.0
    assert 1.0 < syneresis < 2.0
    assert swelling - 1.0 == pytest.approx(2.0 - syneresis)


def test_negative_syneresis_rate_rejected():
    with pytest.raises(ValueError):
        source_lambda_from_k_meq(-0.0024, 60.98)
