# RQ-001C — Normalized calcium-release timescale targets

Status: **DERIVED CALIBRATION TARGET — not an intrinsic bond-rate measurement**

The Tavakoli 2019 study does not report the total swelling-bath volume in the accessible methods text, so its external Ca²⁺ concentration cannot yet be converted unambiguously to released moles or fractional junction loss. However, the **shape** of the reported release curve can be used without bath-volume normalization.

## Source observations

Tavakoli et al. (2019), DOI `10.1016/j.msec.2019.109951`, 4% w/w Sigma A1112 alginate, 100 mM CaCl₂.

### 1-minute crosslink

Reported release-rate segments:

- 0–60 min: 0.046 mM/min
- 60–120 min: 0.0034 mM/min

Assuming the reported interval rates represent interval-average slopes, integration gives:

- cumulative at 60 min: 2.760 mM-equivalent
- cumulative at 120 min: 2.964 mM-equivalent
- normalized `F(60)/F(120) = 0.93117`

### 5-minute crosslink

Reported release-rate segments during swelling:

- 0–60 min: 0.067 mM/min
- 60–120 min: 0.025 mM/min
- 120–240 min: 0.007 mM/min

Integrated values:

- cumulative at 60 min: 4.020 mM-equivalent
- cumulative at 120 min: 5.520 mM-equivalent
- cumulative at 240 min: 6.360 mM-equivalent
- normalized `F(60)/F(240) = 0.63208`
- normalized `F(120)/F(240) = 0.86792`

The paper reports negligible change from 240–360 min for the 5-minute-crosslinked system, identifying an equilibrium plateau before later degradation.

## Reduced one-timescale fit

For a deliberately minimal descriptive curve

`F(t) = 1 - exp(-k_app t)`

fitted only to the normalized swelling-stage release shape:

| crosslink duration | best-fit `k_app` | characteristic time `1/k_app` | role |
|---|---:|---:|---|
| 1 min | ~7.24e-4 s^-1 | ~23.0 min | shape target |
| 5 min | ~2.66e-4 s^-1 | ~62.7 min | shape target |

For the 5-minute case, the fitted normalized curve predicts approximately 0.630 at 60 min and 0.871 at 120 min versus observed derived values 0.632 and 0.868, respectively.

## Interpretation

This is a useful result because it establishes a source-derived **system-level release timescale** without requiring absolute calcium inventory or bath volume.

It is **not** valid to assign `k_t = k_app` directly. `k_app` conflates:

- hydration transport;
- temporary-junction dissociation;
- mobile Ca²⁺ diffusion;
- geometry / diffusion length;
- possible rebinding / ion exchange;
- sampling and external-bath conditions.

Under simple serial transport/kinetic limitations, the intrinsic temporary-junction dissociation can be faster than the externally observed apparent release, but the coupled swelling problem is not sufficiently simple to convert this into a strict inequality without further assumptions.

## Strong signal for model calibration

A01 v0.1 now has quantitative **shape constraints**:

1. A source-matched 1-minute-crosslink simulation should reproduce a substantially faster normalized swelling-stage release trajectory than the 5-minute-crosslink case.
2. The 5-minute-crosslink swelling-stage trajectory should be close to a ~2.7e-4 s^-1 one-timescale release shape over 0–240 min.
3. The model must reproduce or explain the 240–360 min near-plateau before later chelate-network degradation; a single irreversible first-order junction population cannot do this.

The third point is particularly important: it independently supports the v0.1 decision to separate temporary and strong/chelate junction populations.

## Next calibration step

Fit the explicit `ca_model` release shape using nuisance parameters for geometry and calcium scale while constraining `D_w` and `D_Ca` by the source-backed priors. Compare whether one shared temporary-junction kinetic law plus different initial junction-population states can reproduce both 1-minute and 5-minute crosslink curves.

If it cannot, the model needs an explicit crosslink-duration-dependent network topology/state variable rather than merely different calcium inventories.
