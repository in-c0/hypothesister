from __future__ import annotations

AVOGADRO = 6.02214076e23


def expected_chain_count(
    box_edge_m: float,
    polymer_wt_fraction: float,
    chain_molar_mass_g_mol: float,
    solution_density_kg_m3: float = 1000.0,
) -> float:
    if box_edge_m <= 0 or not 0 < polymer_wt_fraction < 1:
        raise ValueError("invalid box or concentration")
    if chain_molar_mass_g_mol <= 0 or solution_density_kg_m3 <= 0:
        raise ValueError("invalid mass or density")
    volume_m3 = box_edge_m**3
    polymer_mass_kg = volume_m3 * solution_density_kg_m3 * polymer_wt_fraction
    chain_molar_mass_kg_mol = chain_molar_mass_g_mol / 1000.0
    return polymer_mass_kg / chain_molar_mass_kg_mol * AVOGADRO


def case_counts_from_integer_chains(
    chain_count: int,
    dimers_per_chain: int,
    crosslink_degree_f: float,
):
    if chain_count < 1 or dimers_per_chain < 1 or crosslink_degree_f < 0:
        raise ValueError("invalid case bookkeeping")
    dimers = chain_count * dimers_per_chain
    monomers = 2 * dimers
    calcium_ions = crosslink_degree_f * monomers
    return {
        "chains": chain_count,
        "dimers": dimers,
        "monomers": monomers,
        "calcium_ions": calcium_ions,
    }
