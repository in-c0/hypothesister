import numpy as np
import pytest
from cleancoin_lab.collective_transition import transition_time_s


def test_transition_uses_failed_fraction_quantile():
    times = np.arange(100, dtype=float)
    assert transition_time_s(times, 0.35) == pytest.approx(np.quantile(times, 0.65))
