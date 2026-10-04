import numpy as np

from credit_risk.validation import bootstrap_auc_interval, classification_probability_metrics, gini_from_auc, ks_statistic


def test_gini_from_auc():
    assert gini_from_auc(0.7084432424073367) == 2 * 0.7084432424073367 - 1


def test_ks_statistic_is_bounded():
    y_true = np.array([0, 0, 1, 1])
    y_score = np.array([0.1, 0.4, 0.35, 0.9])

    ks = ks_statistic(y_true, y_score)

    assert 0 <= ks <= 1
    assert ks == 0.5


def test_classification_probability_metrics_use_average_precision_key():
    y_true = np.array([0, 0, 1, 1])
    y_score = np.array([0.05, 0.25, 0.75, 0.95])

    metrics = classification_probability_metrics(y_true, y_score)

    assert set(metrics) >= {"roc_auc", "average_precision_ap", "brier_score", "gini", "ks_statistic"}
    assert 0 <= metrics["average_precision_ap"] <= 1
    assert metrics["observed_default_rate"] == 0.5


def test_bootstrap_auc_interval_is_bounded_and_ordered():
    y_true = np.array([0, 0, 1, 1, 1, 0])
    y_score = np.array([0.05, 0.25, 0.75, 0.95, 0.80, 0.10])

    lower, upper = bootstrap_auc_interval(y_true, y_score, n_bootstrap=100, random_state=7)

    assert 0 <= lower <= upper <= 1
