from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score, brier_score_loss, log_loss, roc_auc_score


def gini_from_auc(auc: float) -> float:
    """Convert ROC-AUC to the credit-risk Gini coefficient."""
    return 2 * float(auc) - 1


def ks_statistic(y_true, y_score) -> float:
    """Compute the Kolmogorov-Smirnov statistic for default scores."""
    y_true = np.asarray(y_true).astype(int)
    y_score = np.asarray(y_score, dtype=float)
    order = np.argsort(y_score)
    y_sorted = y_true[order][::-1]
    bad_total = y_sorted.sum()
    good_total = len(y_sorted) - bad_total
    if bad_total == 0 or good_total == 0:
        return float("nan")
    bad_cdf = np.cumsum(y_sorted) / bad_total
    good_cdf = np.cumsum(1 - y_sorted) / good_total
    return float(np.max(np.abs(bad_cdf - good_cdf)))


def classification_probability_metrics(y_true, y_score) -> dict[str, float]:
    """Calculate PD validation metrics used in the project."""
    auc = roc_auc_score(y_true, y_score)
    return {
        "roc_auc": float(auc),
        "average_precision_ap": float(average_precision_score(y_true, y_score)),
        "brier_score": float(brier_score_loss(y_true, y_score)),
        "log_loss": float(log_loss(y_true, y_score)),
        "gini": gini_from_auc(auc),
        "ks_statistic": ks_statistic(y_true, y_score),
        "mean_predicted_pd": float(np.mean(y_score)),
        "observed_default_rate": float(np.mean(y_true)),
    }


def bootstrap_auc_interval(
    y_true,
    y_score,
    *,
    n_bootstrap: int = 500,
    confidence: float = 0.95,
    random_state: int = 42,
) -> tuple[float, float]:
    """Percentile bootstrap confidence interval for ROC-AUC."""
    y_true = np.asarray(y_true).astype(int)
    y_score = np.asarray(y_score, dtype=float)
    rng = np.random.default_rng(random_state)
    aucs: list[float] = []
    for _ in range(n_bootstrap):
        idx = rng.integers(0, len(y_true), len(y_true))
        sample_y = y_true[idx]
        if sample_y.min() == sample_y.max():
            continue
        aucs.append(float(roc_auc_score(sample_y, y_score[idx])))
    alpha = 1 - confidence
    lower, upper = np.percentile(aucs, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return float(lower), float(upper)


def decile_table(data: pd.DataFrame, score_col: str, target_col: str, *, n_bins: int = 10) -> pd.DataFrame:
    """Create a PD score decile table with observed default rates."""
    out = data[[score_col, target_col]].copy()
    out["decile"] = pd.qcut(out[score_col], q=n_bins, labels=False, duplicates="drop") + 1
    return (
        out.groupby("decile", as_index=False)
        .agg(
            loan_count=(target_col, "size"),
            mean_predicted_pd=(score_col, "mean"),
            observed_default_rate=(target_col, "mean"),
            default_count=(target_col, "sum"),
            min_predicted_pd=(score_col, "min"),
            max_predicted_pd=(score_col, "max"),
        )
        .sort_values("decile")
    )
