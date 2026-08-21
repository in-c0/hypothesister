# Hypothesister Invention Mode v0

Invention Mode is a bounded workflow for discovering and falsifying **technical mechanisms** that may later justify patent investigation.

It does **not** determine patentability, infringement, freedom to operate, or legal validity. Those require jurisdiction-specific prior-art/FTO analysis and, where warranted, professional patent advice.

## Objective

Convert a broad product vision into concrete engineering mechanisms that:

1. solve a measurable technical problem;
2. make falsifiable predictions;
3. can be enabled well enough to build or simulate;
4. survive a cheap discriminating experiment; and
5. still appear to have meaningful whitespace after a targeted prior-art search.

The mode intentionally rejects claims whose only merit is that they sound futuristic.

## Candidate contract

Each candidate uses `hypothesister/schemas/invention_candidate.schema.json` and records:

- the technical problem;
- the proposed causal mechanism;
- a *novelty hypothesis* (never a declaration of novelty);
- predictions and explicit falsifiers;
- the cheapest discriminating experiment;
- six 0–5 triage scores;
- known prior-art references and their relationship;
- an enablement note; and
- the next stage gate.

## Scores

- **technical_novelty** — how materially different the mechanism appears from known approaches.
- **utility** — how much the mechanism improves the target technical problem.
- **non_obviousness** — whether the mechanism appears to require more than a routine combination of known techniques.
- **testability** — whether a discriminating experiment can be run cheaply and objectively.
- **enablement** — whether the mechanism is concrete enough that an engineer could attempt it.
- **ip_whitespace** — preliminary evidence that nearby prior art does not already occupy the same mechanism.

Scores are research triage only. They are not legal conclusions.

## Stage gates

### G0 — Problem decomposition

Describe the physical or computational failure precisely. Avoid solution words in the problem statement where possible.

### G1 — Competing mechanisms

Generate at least three materially different mechanisms for the same problem. A synonym or parameter tweak is not a competing mechanism.

### G2 — Cheap falsification

For each candidate, state what observable result would kill it and run the cheapest test capable of distinguishing it from the baseline.

### G3 — Enablement

Survivors must become concrete enough to specify components, state transitions, geometry, algorithms, or fabrication steps. A slogan cannot advance.

### G4 — Targeted prior-art screen

Search the mechanism, not the product category. Record the closest references. Mark a candidate `prior_art_blocked` when a reference appears to disclose the same essential mechanism; otherwise use `prior_art_unclear` until a qualified review or stronger search resolves it.

### G5 — Combination check

Only after individual mechanisms survive should compatible candidates be combined. Re-run obviousness and prior-art checks on the combination; do not assume combining known components creates an invention.

### G6 — IP review packet

A candidate may reach `ready_for_ip_review` only when it has:

- a concrete mechanism;
- at least one discriminating result;
- known alternatives;
- closest prior art recorded;
- drawings or implementation notes sufficient for enablement; and
- a clear statement of what is believed to be technically different.

## Disclosure rule

If a project may be patented, keep its project-specific Invention Mode records private until an IP filing/disclosure decision has been made. Do not place confidential candidate mechanisms in this public repository merely to use the workflow.

## Research rule

**Do not patent the vision. Discover solutions while making the vision work, then investigate those solutions.**
