import math
import pytest

from cleancoin_lab.mechanics import (
    ALG_CA_PLATEAU_EXPONENT,
    crosslink_density_from_young_modulus,
    mesh_size_from_crosslink_density,
    plateau_modulus_from_calcium_distance,
    reduced_calcium_distance,
    young_modulus_from_crosslink_density,
)


def test_grassi_3p8pct_modulus_from_crosslink_density():
    predicted = young_modulus_from_crosslink_density(6.4, 298.15)
    assert predicted == pytest.approx(47_587.0, rel=0.01)


def test_grassi_3p8pct_mesh_from_crosslink_density():
    predicted_nm = mesh_size_from_crosslink_density(6.4) * 1e9
    assert predicted_nm == pytest.approx(7.9, rel=0.01)


def test_modulus_crosslink_density_round_trip():
    rho = 2.8
    e = young_modulus_from_crosslink_density(rho, 298.15)
    assert crosslink_density_from_young_modulus(e, 298.15) == pytest.approx(rho)


def test_zero_crosslink_density_has_zero_modulus_and_unbounded_mesh():
    assert young_modulus_from_crosslink_density(0.0) == 0.0
    assert math.isinf(mesh_size_from_crosslink_density(0.0))


def test_liu_calcium_scaling_uses_reported_three_halves_exponent():
    assert ALG_CA_PLATEAU_EXPONENT == pytest.approx(1.5)
    epsilon = reduced_calcium_distance(30.0, 20.0)
    assert epsilon == pytest.approx(0.5)
    predicted = plateau_modulus_from_calcium_distance(30.0, 20.0, 10_000.0)
    assert predicted == pytest.approx(10_000.0 * 0.5**1.5)


def test_calcium_scaling_is_zero_at_or_below_gel_point():
    assert plateau_modulus_from_calcium_distance(20.0, 20.0, 10_000.0) == 0.0
    assert plateau_modulus_from_calcium_distance(10.0, 20.0, 10_000.0) == 0.0


def test_invalid_mechanics_inputs_rejected():
    with pytest.raises(ValueError):
        young_modulus_from_crosslink_density(-1.0)
    with pytest.raises(ValueError):
        mesh_size_from_crosslink_density(-1.0)
    with pytest.raises(ValueError):
        crosslink_density_from_young_modulus(-1.0)
    with pytest.raises(ValueError):
        reduced_calcium_distance(-1.0, 1.0)
    with pytest.raises(ValueError):
        reduced_calcium_distance(1.0, 0.0)
    with pytest.raises(ValueError):
        plateau_modulus_from_calcium_distance(2.0, 1.0, -1.0)
