import pandas as pd
import pytest


@pytest.fixture
def sample_loans():
    return pd.DataFrame(
        {
            "grade": ["A", "B", "C"],
            "predicted_pd": [0.05, 0.15, 0.30],
            "lgd_estimate": [0.4, 0.5, 0.8],
            "ead_proxy": [100.0, 200.0, 300.0],
            "expected_loss_prelim": [2.0, 15.0, 72.0],
        }
    )
