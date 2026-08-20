import pytest

from cleancoin_lab.surface_classification_screen import classification_change_screen


def test_classification_change_screen_is_deterministic_and_bounded():
    a = classification_change_screen(n_samples=256, seed=17)
    b = classification_change_screen(n_samples=256, seed=17)
    assert a == b
    assert a.n_samples == 256
    for value in (
        a.bulk_accept_fraction,
        a.combined_accept_fraction,
        a.changed_fraction,
        a.surface_first_fraction,
    ):
        assert 0.0 <= value <= 1.0


def test_zeroish_surface_susceptibility_recovers_bulk_classification():
    result = classification_change_screen(
        n_samples=256,
        seed=3,
        surface_rate_over_strength_range=(1e-12, 1e-11),
    )
    assert result.changed_fraction == pytest.approx(0.0)
    assert result.surface_first_fraction == pytest.approx(0.0)


def test_invalid_acceptance_window_is_rejected():
    with pytest.raises(ValueError):
        classification_change_screen(n_samples=8, acceptance_window_s=(1800.0, 600.0))
