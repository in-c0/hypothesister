# Model contract: HYP-001

A computational result is allowed to influence the stage gate only if every influential parameter has provenance and uncertainty.

## State variables required by first real continuum model

- `c_w(x,t)` — local water activity/concentration
- `c_ion(x,t)` — relevant mobile ion concentration(s)
- `q(x,t)` — crosslink/binder integrity state
- `u(x,t)` — displacement field
- `d(x,t)` — scalar damage / fracture field (or an explicitly justified alternative)

## Minimum coupled physics

1. water transport;
2. relevant ion/binder transport;
3. network association/dissociation kinetics;
4. swelling strain;
5. hydrated constitutive mechanics;
6. cyclic damage accumulation;
7. loss of connectivity / disintegration criterion.

## Calibration hierarchy

1. primary experimental literature;
2. secondary literature only as navigation to primary measurements;
3. molecular/coarse-grained simulation for missing high-sensitivity parameters;
4. targeted physical measurement only when uncertainty cannot be bounded virtually.

## Inference prohibition

The current `cleancoin_lab.model` is an infrastructure test model. A pass from it MUST NOT be reported as support for HYP-001.
