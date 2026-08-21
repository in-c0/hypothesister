# RQ-003 surface classification-change screen result

Status: quantitative structural screen complete; calibration gate remains open.

Source implementation: `scripts/rq003_surface_classification_screen.py` on `main` at/after `9ec68f25`.

Run contract: 200,000 deterministic samples, seed `20260820`; front time uniform 600–1800 s; work/strength log-uniform 1e-5–1e-2; coupling exponent uniform 0.5–2.0; failure integrity uniform 0.2–0.8. These ranges are exploratory, not calibrated.

## Result

- Surface term advances terminal failure: **34.3695%** of samples.
- Existing 10–30 minute acceptance classification changes: **19.1470%** of samples.
- Combined failure-time quantiles (s): p05 **281.85**, p25 **659.82**, p50 **958.47**, p75 **1335.59**, p95 **1701.98**.

Work/strength quartiles:

| quartile | range | surface advances | classification changes | median combined failure (s) |
| --- | --- | ---: | ---: | ---: |
| Q1 | 1.000e-5–5.682e-5 | 0.0000% | 0.0000% | 1195.62 |
| Q2 | 5.682e-5–3.154e-4 | 0.4840% | 0.0000% | 1198.06 |
| Q3 | 3.154e-4–1.772e-3 | 39.7440% | 6.3460% | 1004.56 |
| Q4 | 1.772e-3–1.000e-2 | 97.2500% | 70.2420% | 453.22 |

## Gate interpretation

The classification changes are not confined to a small boundary subset across this exploratory envelope: the overall change fraction is ~19%, and the upper work/strength quartile changes classification in ~70% of samples. Therefore the bounded surface/interface term cannot yet be treated as safely secondary.

However, the result is strongly controlled by the deliberately broad, uncalibrated work/strength sweep: Q1–Q2 show zero classification changes while Q4 dominates the effect. Per the pre-registered decision rule, this does **not** justify promoting a high-fidelity abrasion model or claiming surface failure dominance. The RQ-003 gate remains unresolved pending calibration/provenance that constrains the physically plausible work/strength regime (or a bounded experiment/source that can rule out the high-sensitivity region).

Next bounded gate: constrain the work/strength regime from existing primary evidence or an explicitly defined physical measurement; then rerun the same classification screen without changing the decision rule.