from __future__ import annotations

from dataclasses import dataclass
from .model import SimulationResult


@dataclass(frozen=True)
class Targets:
    hydration_t50_max_s: float = 10.0
    work_start_s: float = 60.0
    work_end_s: float = 1200.0
    min_work_cohesion: float = 0.70
    post_time_s: float = 2400.0
    max_post_cohesion: float = 0.20


def evaluate(result: SimulationResult, targets: Targets = Targets()) -> dict[str, float | bool]:
    t50 = result.hydration_t50()
    work_start = result.value_at("cohesion", targets.work_start_s)
    work_end = result.value_at("cohesion", targets.work_end_s)
    post = result.value_at("cohesion", targets.post_time_s)

    hydration_pass = t50 <= targets.hydration_t50_max_s
    work_pass = min(work_start, work_end) >= targets.min_work_cohesion
    post_pass = post <= targets.max_post_cohesion

    # Continuous score is useful for optimization; hard pass remains explicit.
    activation_score = min(1.0, targets.hydration_t50_max_s / max(t50, 1e-9))
    work_score = min(1.0, min(work_start, work_end) / targets.min_work_cohesion)
    post_score = min(1.0, targets.max_post_cohesion / max(post, 1e-9))
    score = activation_score * work_score * post_score

    return {
        "hydration_t50_s": t50,
        "cohesion_work_start": work_start,
        "cohesion_work_end": work_end,
        "cohesion_post": post,
        "activation_pass": hydration_pass,
        "work_pass": work_pass,
        "post_pass": post_pass,
        "pass": hydration_pass and work_pass and post_pass,
        "score": score,
    }
