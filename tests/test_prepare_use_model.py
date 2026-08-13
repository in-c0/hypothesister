import numpy as np

from cleancoin_lab.prepare_use_model import (
    PrepareUseDesign,
    prepare,
    prepare_rinse_use,
)


def test_longer_crosslinking_increases_bound_and_strong_state():
    design = PrepareUseDesign()
    one_min = prepare(design, 60.0)
    five_min = prepare(design, 300.0)

    assert five_min.mean_bound_fraction > one_min.mean_bound_fraction
    assert five_min.mean_strong_fraction > one_min.mean_strong_fraction


def test_use_release_is_nonnegative_and_monotonic():
    _, _, result = prepare_rinse_use(
        PrepareUseDesign(),
        300.0,
        use_duration_s=1800.0,
    )
    assert np.all(result.released_ca_mol >= -1e-15)
    assert np.all(np.diff(result.released_ca_mol) >= -1e-12)
    assert np.all(np.diff(result.bound_fraction) <= 1e-10)


def test_preparation_history_changes_normalized_release_shape():
    design = PrepareUseDesign()
    _, _, one = prepare_rinse_use(design, 60.0, use_duration_s=7200.0)
    _, _, five = prepare_rinse_use(design, 300.0, use_duration_s=7200.0)

    one_60 = one.value_at("released_ca_mol", 3600.0)
    one_120 = one.value_at("released_ca_mol", 7200.0)
    five_60 = five.value_at("released_ca_mol", 3600.0)
    five_120 = five.value_at("released_ca_mol", 7200.0)

    assert one_120 > 0 and five_120 > 0
    # Smoke-test the intended model capability: preparation history can alter
    # release shape even when the use-stage kinetic constants are shared.
    assert not np.isclose(one_60 / one_120, five_60 / five_120, rtol=1e-3)


def test_fractions_remain_bounded_after_preparation():
    state = prepare(PrepareUseDesign(), 300.0)
    for field in (
        state.free_fraction,
        state.temporary_fraction,
        state.strong_fraction,
    ):
        assert np.all(field >= -1e-12)
        assert np.all(field <= 1 + 1e-12)
    total = state.free_fraction + state.temporary_fraction + state.strong_fraction
    assert np.allclose(total, 1.0, atol=1e-9)
