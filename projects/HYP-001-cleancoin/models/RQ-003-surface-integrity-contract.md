# RQ-003 surface-integrity model contract

Status: bounded sensitivity gate; parameter calibration intentionally deferred
Date: 2026-08-20

## Purpose

Translate the RQ-003 surface-shear decision into the smallest testable model extension without inventing CleanCoin-specific tribology parameters.

## State

Add one normalized surface/interface integrity state `s(t) in [0,1]` alongside the existing transport/network/contact state:

- `s=1`: intact surface/interface;
- `s=0`: surface/interface failure.

The state is independent of the bulk contact-load factor. Bulk failure must not be used as a surrogate for fibre pull-out or scrubbing shear.

## Minimal law

Use accumulated normalized tangential work/slip `W_t` as the forcing coordinate and network weakening `w(t) in [0,1]` as a coupling term, where larger `w` means more weakened network state:

`ds/dW_t = -k_s * s * (epsilon + w)^p`

with:

- `k_s > 0`: uncalibrated surface susceptibility;
- `p >= 0`: coupling strength between network weakening and surface loss;
- `epsilon > 0`: small baseline susceptibility so intact-network shear is representable rather than forced to zero.

Clamp `s` to `[0,1]`. Do not fit `k_s`, `p`, or `epsilon` to the desired 10–30 min outcome.

## Coupling to acceptance state

Run the existing transport/contact model unchanged, then evaluate surface failure as an additional terminal condition. A conservative combined survival indicator is:

`survives = bulk_survives AND (s > s_fail)`

where `s_fail` is sensitivity-screened rather than asserted as a measured CleanCoin threshold.

## Required sensitivity screen

Before adding model fidelity, sweep broad dimensionless ranges for `(k_s * W_total)`, `p`, and `s_fail` across the same transport/contact uncertainty ensemble used by RQ-003. Compare:

1. bulk-only acceptance classification;
2. bulk + surface classification;
3. timing of first terminal failure.

Report the fraction of the uncertainty ensemble whose 10–30 min acceptance classification changes solely because of the surface term.

## Decision rule

- If the surface term changes the acceptance classification only in a small boundary subset, retain it as a documented secondary failure mode and do **not** build a high-fidelity abrasion model yet.
- If it changes the classification across a material fraction of the uncertainty ensemble, surface/interface calibration becomes a dominant RQ-003 uncertainty and physical measurement is required before a lifetime claim.
- If results depend mainly on arbitrary parameter bounds, report the gate as unresolved; do not select bounds that force a preferred outcome.

## Provenance / limits

The model structure is justified by the evidence summarized in `research/RQ-003-surface-shear-decision.md`. Those sources establish that interface-controlled pull-out/shear response can be distinct from homogeneous bulk compression. They do not supply CleanCoin household-wash parameter values.

## Next executable gate

Implement this law as a separable sensitivity layer around the existing RQ-003 ensemble, preserving the existing bulk model and frozen uncertainty assumptions. The implementation should emit a compact classification-change table before any calibration or higher-fidelity mechanics work is considered.
