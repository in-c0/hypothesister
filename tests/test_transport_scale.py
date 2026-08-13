import pytest

from cleancoin_lab.transport_scale import diffusion_length_m, diffusion_time_s


def test_2025_ion_exchange_scale():
    d = 1.7e-11
    assert diffusion_length_m(1200.0, d) == pytest.approx(142.83e-6, rel=1e-3)
    assert diffusion_time_s(150e-6, d) / 60.0 == pytest.approx(22.06, rel=1e-3)
