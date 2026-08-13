import numpy as np


def transition_time_s(local_transition_times_s, retained_connectivity_threshold):
    """Time when failed local fraction reaches 1 - retained threshold."""
    times = np.asarray(local_transition_times_s, dtype=float)
    if times.ndim != 1 or len(times) == 0 or np.any(times < 0):
        raise ValueError("invalid local transition times")
    if not 0 < retained_connectivity_threshold < 1:
        raise ValueError("threshold must be in (0,1)")
    failed_fraction = 1.0 - retained_connectivity_threshold
    return float(np.quantile(times, failed_fraction))
