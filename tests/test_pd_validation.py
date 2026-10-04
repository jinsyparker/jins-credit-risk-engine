import numpy as np

from credit_risk.validation import gini_from_auc, ks_statistic


def test_gini_from_auc():
    assert gini_from_auc(0.7084432424073367) == 2 * 0.7084432424073367 - 1


def test_ks_statistic_is_bounded():
    y_true = np.array([0, 0, 1, 1])
    y_score = np.array([0.1, 0.4, 0.35, 0.9])

    ks = ks_statistic(y_true, y_score)

    assert 0 <= ks <= 1
