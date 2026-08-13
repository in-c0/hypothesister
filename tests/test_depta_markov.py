import pytest

from cleancoin_lab.depta_markov import HIGH_G_TRIADS, generate_monomers, monomer_fraction, triad_fractions


def test_depta_high_g_ensemble_reproduces_source_statistics():
    seq = generate_monomers(300_000, seed=42)
    assert monomer_fraction(seq, "G") == pytest.approx(0.630, abs=0.004)
    observed = triad_fractions(seq)
    for triad, expected in HIGH_G_TRIADS.items():
        assert observed[triad] == pytest.approx(expected, abs=0.004)


def test_200kda_chain_has_1142_monomers_for_571_dimers():
    seq = generate_monomers(1142, seed=7)
    assert len(seq) == 2 * 571
