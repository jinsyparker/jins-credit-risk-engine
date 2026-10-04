from __future__ import annotations

import numpy as np
import pandas as pd


def safe_ratio(numerator, denominator) -> pd.Series:
    """Divide two vectors and return NaN where the denominator is non-positive."""
    numerator = pd.Series(numerator, copy=False)
    denominator = pd.Series(denominator, copy=False)
    return numerator.where(denominator > 0) / denominator.where(denominator > 0)


def clipped_lgd(recovery_amount, ead) -> pd.Series:
    """Compute clipped LGD as 1 - recovery / EAD."""
    lgd = 1 - safe_ratio(recovery_amount, ead)
    return lgd.clip(lower=0, upper=1)


def recovery_based_lgd(data: pd.DataFrame, recovery_col: str = "recoveries", ead_col: str = "funded_amnt") -> pd.Series:
    """Baseline gross-recovery LGD used by the project."""
    return clipped_lgd(data[recovery_col].fillna(0), data[ead_col])


def lgd_sensitivity_summary(data: pd.DataFrame, lgd_columns: list[str]) -> pd.DataFrame:
    """Summarize alternative LGD definitions."""
    rows = []
    for col in lgd_columns:
        values = data[col].dropna()
        rows.append(
            {
                "lgd_definition": col,
                "valid_count": int(values.count()),
                "mean_lgd": float(values.mean()),
                "median_lgd": float(values.median()),
                "std_lgd": float(values.std()),
                "share_lgd_eq_1": float(np.mean(values.eq(1))),
                "share_lgd_eq_0": float(np.mean(values.eq(0))),
            }
        )
    return pd.DataFrame(rows)
