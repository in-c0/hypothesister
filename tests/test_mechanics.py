import math
import pytest

from cleancoin_lab.mechanics import (
    crosslink_density_from_young_modulus,
    mesh_size_from_crosslink_density,
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


def test_invalid_mechanics_inputs_rejected():
    with pytest.raises(ValueError):
        young_modulus_from_crosslink_density(-1.0)
    with pytest.raises(ValueError):
        mesh_size_from_crosslink_density(-1.0)
    with pytest.raises(ValueError):
        crosslink_density_from_young_modulus(-1.0)
