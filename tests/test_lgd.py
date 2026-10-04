import pandas as pd

from credit_risk.lgd import recovery_based_lgd


def test_recovery_based_lgd_is_clipped():
    data = pd.DataFrame(
        {
            "recoveries": [0.0, 50.0, 150.0],
            "funded_amnt": [100.0, 100.0, 100.0],
        }
    )

    lgd = recovery_based_lgd(data)

    assert lgd.tolist() == [1.0, 0.5, 0.0]
    assert lgd.between(0, 1, inclusive="both").all()
