from __future__ import annotations

import random
from collections import Counter

HIGH_G_TRIADS = {
    "GGG": 0.475,
    "GGM": 0.050,
    "GMG": 0.055,
    "GMM": 0.050,
    "MGG": 0.050,
    "MGM": 0.055,
    "MMG": 0.050,
    "MMM": 0.215,
}


def _pair_probabilities(triads=HIGH_G_TRIADS):
    out = Counter()
    for triad, p in triads.items():
        out[triad[:2]] += p
    return dict(out)


def _transition_probabilities(triads=HIGH_G_TRIADS):
    pairs = _pair_probabilities(triads)
    return {
        pair: {
            "G": triads.get(pair + "G", 0.0) / total,
            "M": triads.get(pair + "M", 0.0) / total,
        }
        for pair, total in pairs.items()
    }


def generate_monomers(length: int, seed: int = 0) -> str:
    if length < 2:
        raise ValueError("length must be >= 2")
    rng = random.Random(seed)
    pairs = _pair_probabilities()
    pair_names = tuple(pairs)
    pair_weights = tuple(pairs[p] for p in pair_names)
    seq = list(rng.choices(pair_names, weights=pair_weights, k=1)[0])
    transitions = _transition_probabilities()
    while len(seq) < length:
        pair = "".join(seq[-2:])
        p_g = transitions[pair]["G"]
        seq.append("G" if rng.random() < p_g else "M")
    return "".join(seq)


def monomer_fraction(sequence: str, unit: str = "G") -> float:
    if not sequence or unit not in {"G", "M"}:
        raise ValueError("invalid sequence or unit")
    return sequence.count(unit) / len(sequence)


def triad_fractions(sequence: str):
    if len(sequence) < 3:
        raise ValueError("sequence must contain at least 3 monomers")
    counts = Counter(sequence[i:i+3] for i in range(len(sequence)-2))
    total = sum(counts.values())
    return {k: counts.get(k, 0) / total for k in HIGH_G_TRIADS}
