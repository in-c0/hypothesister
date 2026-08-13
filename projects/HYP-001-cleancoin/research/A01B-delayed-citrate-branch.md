# A01B — Delayed citrate-triggered de-crosslinking branch

Status: **KEEP AS VIRTUAL MECHANISM BRANCH — no formulation recommendation**

## Motivation

The passive A01 mechanism relies on water/ion exchange eventually removing enough Ca²⁺ junctions to trigger network failure. Primary rheology data show that an externally imposed calcium-sequestration front can accelerate loss of alginate stiffness on a tens-of-minutes timescale.

Diryak et al. (2015), DOI `10.1016/j.foodhyd.2015.11.002`, directly measured external gelation and degradation of 4% w/w alginate in situ:

- alginate M:G reported as 0.39:0.61;
- CaCl₂ source concentrations: 50, 100, 200 mM;
- 1 mm rheometer gap;
- G' and G'' measured continuously at 0.5% strain, 10 rad/s;
- gelation showed a sharp rise in moduli over the first ~3 min;
- degradation experiment used 20 min crosslinking with 200 mM CaCl₂;
- the CaCl₂ source was then replaced by either 500 mM EDTA or 500 mM sodium citrate;
- EDTA returned G' to a level similar to uncrosslinked sodium alginate after ~35 min;
- sodium citrate reduced G' by about one order of magnitude over the degradation observation, compared with about two orders for EDTA.

This is a **mechanism benchmark**, not a CleanCoin recipe. The chelator concentrations are high external-source conditions and have not been screened for the product's later safety/environment constraints.

## A01B hypothesis

A spatially or chemically delayed citrate source could create an induction period in which the Ca-alginate network remains mechanically useful, followed by accelerated Ca²⁺ sequestration and loss of network connectivity.

Possible virtual architectures include:

1. citrate encapsulated behind a water-dissolving sacrificial barrier;
2. citrate immobilized/complexed in a phase whose release rate is hydration-controlled;
3. a spatially separated citrate-rich core and load-bearing Ca-alginate shell;
4. citrate release accelerated by cyclic compression/shear through transport enhancement or barrier fatigue.

No one architecture is preferred yet.

## Why this is scientifically attractive

A purely passive network has to satisfy two competing requirements with the same chemistry:

- resist water/ion exchange during washing;
- then rapidly de-crosslink afterward.

A delayed chelation front separates the **timer** from the **load-bearing network**. In principle this could broaden the feasible design region because the alginate can be optimized for wet performance while the trigger phase is optimized for induction time and post-induction failure.

## Why it may fail

A01B should be killed if virtual modelling shows any of the following across realistic uncertainty:

- citrate leaks early enough to materially reduce wet strength during the useful window;
- the required concentration/source mass is impractically high;
- diffusion smears the transition so much that there is no useful induction period;
- citrate-Ca transport merely weakens the gel gradually rather than producing a sharp enough loss of connectivity;
- the trigger layer itself prevents rapid hydration/expansion;
- later safety/environment constraints exclude the required chemistry or dose.

## First virtual model

Use a 1-D coupled transport model with separate state variables for:

- water/hydration;
- releasable citrate reservoir `c_res(x,t)`;
- mobile citrate `c_cit(x,t)`;
- mobile Ca²⁺ `c_ca(x,t)`;
- temporary/persistent Ca-alginate junction state;
- effective load-bearing crosslink density `rho_x(x,t)`;
- reference modulus from the source-backed mechanics layer.

The release barrier should be parameterized by an induction-time distribution rather than assumed instantaneous. Citrate-Ca binding may initially be represented by a reduced effective reaction only if its equilibrium/kinetic constants are separately sourced and uncertainty-propagated.

## Benchmark targets

Before any CleanCoin optimization, the model should be able to reproduce the qualitative Diryak benchmark:

- rapid external Ca-driven stiffening of a 4% alginate layer;
- substantial stiffness loss after switching to an external chelator;
- citrate produces slower/weaker softening than EDTA under the reported equal 500 mM source concentration.

Then the actual CleanCoin inverse-design question is:

> Is there a robust parameter region with <10–20% loss of useful mechanical performance during the chosen wash interval, followed by rapid enough loss of alginate-network cohesion afterward?

## Relation to A01

A01 remains the simpler passive mechanism and should not be displaced merely because A01B is easier to tune in a toy model. A01B earns priority only if source-calibrated virtual screening shows a substantially larger robust design region.
