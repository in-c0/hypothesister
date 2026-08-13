# RQ-001E — Source-derived phase-transition targets

Status: **PRIMARY CALIBRATION TARGETS ESTABLISHED**

## Correction to the earlier normalized-release interpretation

The interval-average Ca²⁺ release rates in Tavakoli et al. (2019), DOI `10.1016/j.msec.2019.109951`, do not all represent the same physical phase.

The paper's phase assignments are:

### 1-minute crosslink

- swelling: approximately **0–30 min**
- degradation begins: approximately **30 min**
- early degradation: approximately **30–60 min**
- continued degradation: **60–120 min** in the reported interval

The reported Ca²⁺ release rate of ~0.046 mM/min over 0–60 min therefore mixes temporary-junction release during swelling with release associated with the onset of chelate-network degradation.

### 5-minute crosslink

- swelling: approximately **0–240 min**
- equilibrium plateau: approximately **240–360 min**
- degradation: **after ~360 min**

The reported 0.067, 0.025 and 0.007 mM/min intervals through 240 min are all assigned to the swelling region by the authors; release and weight change are negligible during the 240–360 min equilibrium region.

## Mechanistic interpretation reported by the source

The authors propose:

1. water diffusion dissociates temporary Ca²⁺ junctions;
2. loss of those counterions increases fixed negative charge density;
3. electrostatic repulsion increases water uptake and enlarges the network lattice;
4. when lattice size reaches a critical value, chelate junctions dissociate and the hydrogel degrades.

This makes **phase-transition timing** a more defensible calibration target than treating all release observations as one first-order process.

## New model-adequacy targets

A source-matched preparation/use model should aim to reproduce, with shared physical laws:

| preparation | swelling end / degradation onset | plateau |
|---|---:|---|
| 1 min in 100 mM CaCl₂ | ~30 min | no clear long plateau before degradation |
| 5 min in 100 mM CaCl₂ | >360 min for degradation onset | ~240–360 min |

The exact transition times should carry uncertainty because they are identified from plotted phase regions rather than a reported kinetic confidence interval.

## Consequence for v0.2

`prepare_use_model` v0.2 continuously dissociates both temporary and strong junction populations during use. That is structurally inconsistent with the source mechanism because strong/chelate failure should remain strongly suppressed until a swelling/network-expansion criterion is reached.

The next reduced model must therefore add a state-triggered strong-junction failure mechanism. Until explicit swelling mechanics are introduced, the trigger may use a clearly labelled reduced-order expansion proxy derived from temporary-junction loss relative to persistent scaffold/junction state.

## Implication for RQ-001C

The source-derived `k_app` values in `RQ-001C-normalized-release-timescale.md` remain useful descriptive summaries of the observed release-curve shapes, but the 1-minute `k_app` must **not** be interpreted as a temporary-junction swelling-stage timescale: its 0–120 min target spans both swelling and degradation.

## Gate

A01 advances from calcium-release characterization to mechanics only after a preparation-history model can explain the large shift in phase timing without assigning independent arbitrary decay laws to the 1-minute and 5-minute samples.
