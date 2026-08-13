from __future__ import annotations

import math
import random
import numpy as np

from .depta_markov import generate_monomers

BOND_NM = {
    ("GG", "GG"): 0.92,
    ("GG", "MM"): 0.97,
    ("MM", "GG"): 0.97,
    ("GG", "GM"): 0.97,
    ("GM", "GG"): 0.97,
    ("MM", "MM"): 1.01,
    ("GM", "GM"): 1.02,
    ("MM", "GM"): 1.02,
    ("GM", "MM"): 1.02,
}


def monomers_to_dimers(sequence: str):
    if len(sequence) % 2:
        raise ValueError("monomer sequence length must be even")
    out = []
    for i in range(0, len(sequence), 2):
        pair = sequence[i:i+2]
        out.append("GM" if pair in {"GM", "MG"} else pair)
    return out


def random_unit_vector(rng: random.Random):
    z = 2.0*rng.random() - 1.0
    phi = 2.0*math.pi*rng.random()
    rxy = math.sqrt(max(0.0, 1.0-z*z))
    return np.array([rxy*math.cos(phi), rxy*math.sin(phi), z])


def generate_linear_chain(dimers, box_nm: float, seed: int):
    if box_nm <= 0 or len(dimers) < 1:
        raise ValueError("invalid chain inputs")
    rng = random.Random(seed)
    origin = np.array([rng.random()*box_nm for _ in range(3)])
    direction = random_unit_vector(rng)
    positions = np.empty((len(dimers), 3), dtype=float)
    positions[0] = origin
    for i in range(1, len(dimers)):
        step = BOND_NM[(dimers[i-1], dimers[i])]
        positions[i] = positions[i-1] + step*direction
    return np.mod(positions, box_nm)


def generate_case_chains(chain_count: int, dimers_per_chain: int, box_nm: float, seed: int = 0):
    if chain_count < 1 or dimers_per_chain < 1:
        raise ValueError("invalid system size")
    systems = []
    for chain_id in range(chain_count):
        monomers = generate_monomers(2*dimers_per_chain, seed=seed + 10_007*chain_id)
        dimers = monomers_to_dimers(monomers)
        positions = generate_linear_chain(dimers, box_nm, seed + 1_000_003 + chain_id)
        systems.append((dimers, positions))
    return systems
