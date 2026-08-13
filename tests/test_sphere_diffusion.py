import pytest
from cleancoin_lab.sphere_diffusion import remaining_fraction, tau_from_time


def test_sphere_diffusion_limits():
    assert remaining_fraction(0.0) == 1.0
    assert remaining_fraction(1.0) < 1e-4


def test_200um_radius_at_ma2025_diffusivity():
    tau = tau_from_time(600.0, 1.7e-11, 200e-6)
    assert remaining_fraction(tau) == pytest.approx(0.049, rel=0.08)
