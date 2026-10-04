from __future__ import annotations

import numpy as np
import pandas as pd


def calculate_expected_loss(pd_values, lgd_values, ead_values) -> pd.Series:
    """Calculate loan-level expected loss as PD x LGD x EAD."""
    expected_loss = pd.Series(pd_values, copy=False) * pd.Series(lgd_values, copy=False) * pd.Series(ead_values, copy=False)
    return expected_loss.rename("expected_loss")


def portfolio_summary(data: pd.DataFrame, el_col: str = "expected_loss_prelim", ead_col: str = "ead_proxy") -> dict[str, float]:
    """Aggregate expected loss and exposure at portfolio level."""
    total_ead = float(data[ead_col].sum())
    total_el = float(data[el_col].sum())
    return {
        "loan_count": int(len(data)),
        "total_ead": total_ead,
        "total_expected_loss": total_el,
        "expected_loss_rate": total_el / total_ead if total_ead else np.nan,
    }


def segment_summary(data: pd.DataFrame, segment_col: str, el_col: str = "expected_loss_prelim", ead_col: str = "ead_proxy") -> pd.DataFrame:
    """Aggregate expected loss by a portfolio segment."""
    grouped = (
        data.groupby(segment_col, dropna=False)
        .agg(
            loan_count=(segment_col, "size"),
            total_ead=(ead_col, "sum"),
            total_expected_loss=(el_col, "sum"),
        )
        .reset_index()
    )
    grouped["expected_loss_rate"] = grouped["total_expected_loss"] / grouped["total_ead"]
    return grouped


def concentration_summary(data: pd.DataFrame, shares: tuple[float, ...] = (0.01, 0.05, 0.10, 0.20), el_col: str = "expected_loss_prelim") -> pd.DataFrame:
    """Calculate share of expected loss held in top loan-level EL groups."""
    ordered = data.sort_values(el_col, ascending=False)
    total_el = ordered[el_col].sum()
    rows = []
    for share in shares:
        n = max(1, int(np.ceil(len(ordered) * share)))
        subset = ordered.head(n)
        rows.append(
            {
                "share_of_loans": share,
                "loan_count": int(n),
                "total_expected_loss": float(subset[el_col].sum()),
                "share_of_total_expected_loss": float(subset[el_col].sum() / total_el) if total_el else np.nan,
            }
        )
    return pd.DataFrame(rows)
