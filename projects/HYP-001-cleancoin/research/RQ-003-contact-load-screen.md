# RQ-003 contact-load sensitivity screen

Status: **reduced-model result; not a lifecycle prediction**

This note records the first reproducible screen after replacing the fixed
stress-control approximation with an explicit contact-load uncertainty state.
It answers a model-structure question: whether mechanics can plausibly serve as
the primary lifecycle timer before product-specific loading is calibrated.

## Model

The reduced nominal contact load is

\[
\lambda = \frac{F}{E_0 A_{\mathrm{eff}}}.
\]

A dimensionless factor `C` collects stress localisation from contact geometry,
friction and poroelastic contact effects. Reusing the current stable-gel
mechanics exponent `p = 1.5`, the reduced strain law is

\[
\epsilon_{\mathrm{local}} = C\lambda n^{-p},
\]

where `n` is normalized mechanically effective network state. Threshold onset
at `epsilon_local = epsilon_c` occurs at

\[
n^* = \left(\frac{C\lambda}{\epsilon_c}\right)^{1/p}.
\]

For this sensitivity screen only, chemistry/transport softening is represented
as `n(t) = exp(-t/tau)`. This is an analytic scaffold, not a fitted CleanCoin
rate law.

## Why contact uncertainty is explicit

Primary-source transfer anchors motivating the structure:

- Ramanova et al. (2026), DOI `10.1016/j.ijbiomac.2025.149768`: cyclic
  compression of calcium-alginate gels with different loading geometries;
  geometry materially changes stress localisation / response. The reported
  formulation, force and modulus values are transfer anchors, not direct
  CleanCoin calibration.
- Böl et al. (2013), DOI `10.1016/j.jmbbm.2013.04.009`: alginate used as a soft
  material phantom in non-ideal compression; contact friction and constitutive
  response cannot simply be treated as a frictionless homogeneous test.
- Poroelastic hydrogel-friction work (PMID `27901546`): hydrogel friction depends
  on contact duration relative to poroelastic relaxation, motivating a
  timescale-dependent localisation factor rather than one universal stress.

## Reproducible screen

Command:

```bash
python scripts/rq003_contact_screen.py --samples 200000 --seed 20260814
```

Default exploratory ranges:

| Parameter | Range | Sampling |
|---|---:|---|
| `lambda` | 0.02–0.30 | log-uniform |
| `C` | 0.5–3.0 | log-uniform |
| `epsilon_c` | 0.25–0.50 | uniform |
| `tau` | 900–2700 s | uniform |
| cycle frequency | 0.2–2.0 Hz | uniform |

**These ranges are not calibrated CleanCoin parameter bounds.** They are a broad
uncertainty envelope for model-structure falsification.

## Result

200,000 deterministic samples, seed `20260814`:

- fraction with threshold onset in the desired **10–30 min** interval:
  **0.372295**;
- fraction already beyond the reduced mechanical threshold at the initial
  network state: **0.08691**;
- onset-time median: **1493.95 s (24.90 min)**;
- onset-time p25 / p75: **703.28 s (11.72 min)** / **2430.68 s (40.51 min)**;
- onset-time p90: **3399.80 s (56.66 min)**.

The effective contact drive `C*lambda/epsilon_c` produces a strong stratification:

| Drive quartile | Median onset | In 10–30 min | Immediate onset |
|---|---:|---:|---:|
| Q1, lowest | 3058.17 s / 50.97 min | 9.664% | 0% |
| Q2 | 2014.58 s / 33.58 min | 39.304% | 0% |
| Q3 | 1169.06 s / 19.48 min | 83.098% | 0% |
| Q4, highest | 204.53 s / 3.41 min | 16.852% | 34.764% |

The analytic two-fold-load test is pinned in the automated suite. Under the
reduced exponential softening law, doubling `C*lambda` shifts threshold time by

\[
\Delta t = \frac{\tau}{p}\ln 2,
\]

which is large relative to a narrow use window when `tau` itself is on the
order of tens of minutes.

## Decision

**Do not use the mechanical threshold as the primary lifecycle timer in the
current model architecture.** Under a broad contact envelope it is too
sensitive to effective loading to robustly define a 10–30 minute interval.

Retain mechanics as a **terminal accelerator**:

1. chemistry / ion exchange / transport establishes the approximate softening
   timescale;
2. network state approaches a mechanically vulnerable regime;
3. cyclic contact then sharply accelerates final loss of cohesion.

This is a model-structure decision, not a finding that the physical product
will or will not work. A future source-backed or measured user/contact envelope
may narrow `C*lambda`; if so, rerun this screen rather than inheriting the broad
range as truth.

## Next gate

Couple this threshold state to the transport/network model instead of fitting an
independent mechanical clock. RQ-003 remains open until that coupled model is
screened and the need for a separate surface shear / fibre-pullout term is
resolved.
