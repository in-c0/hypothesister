import pytest

from cleancoin_lab.calibration import (
    cumulative_from_piecewise_rates,
    fit_apparent_first_order,
    normalize_cumulative,
)


def test_tavakoli_one_minute_apparent_timescale():
    cumulative = cumulative_from_piecewise_rates(
        [(0, 60, 0.046), (60, 120, 0.0034)]
    )
    normalized = normalize_cumulative(cumulative)
    fit = fit_apparent_first_order(normalized, grid_size=50_000)

    assert cumulative[60.0] == pytest.approx(2.76)
    assert cumulative[120.0] == pytest.approx(2.964)
    assert normalized[60.0] == pytest.approx(0.931174, rel=1e-5)
    assert fit.rate_s == pytest.approx(7.24e-4, rel=0.02)


def test_tavakoli_five_minute_apparent_timescale():
    cumulative = cumulative_from_piecewise_rates(
        [(0, 60, 0.067), (60, 120, 0.025), (120, 240, 0.007)]
    )
    normalized = normalize_cumulative(cumulative)
    fit = fit_apparent_first_order(normalized, grid_size=50_000)

    assert cumulative[240.0] == pytest.approx(6.36)
    assert normalized[60.0] == pytest.approx(0.632075, rel=1e-5)
    assert normalized[120.0] == pytest.approx(0.867925, rel=1e-5)
    assert fit.rate_s == pytest.approx(2.66e-4, rel=0.02)
    assert fit.normalized_prediction[60.0] == pytest.approx(0.630, abs=0.005)
    assert fit.normalized_prediction[120.0] == pytest.approx(0.871, abs=0.005)


def test_noncontiguous_segments_rejected():
    with pytest.raises(ValueError):
        cumulative_from_piecewise_rates([(0, 10, 1.0), (20, 30, 1.0)])
