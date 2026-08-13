import pytest

from cleancoin_lab.swelling import second_order_progress, source_lambda_from_k_meq, characteristic_half_time_s


def test_second_order_half_time():
    lam = source_lambda_from_k_meq(0.0013, 120.48)
    assert characteristic_half_time_s(lam) == pytest.approx(383.2, rel=0.01)
    assert second_order_progress(characteristic_half_time_s(lam), lam) == pytest.approx(0.5)


def test_negative_syneresis_rate_rejected():
    with pytest.raises(ValueError):
        source_lambda_from_k_meq(-0.0024, 60.98)
