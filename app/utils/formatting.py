from __future__ import annotations

import pandas as pd


DISPLAY_NAME_OVERRIDES = {
    "roc_auc": "ROC-AUC",
    "average_precision_ap": "Average Precision (AP)",
    "random_split_average_precision_ap": "Random Split Average Precision (AP)",
    "time_split_average_precision_ap": "Time Split Average Precision (AP)",
    "brier_score": "Brier Score",
    "log_loss": "Log Loss",
    "gini": "Gini",
    "ks_statistic": "KS Statistic",
    "mean_predicted_pd": "Mean Predicted PD",
    "observed_default_rate": "Observed Default Rate",
    "coefficient": "Coefficient",
    "exp_coefficient": "Exp(Coefficient)",
    "metric": "Metric",
    "random_holdout": "Random Holdout",
    "out_of_time": "Out-of-Time",
    "interpretation": "Interpretation",
}


def scale_value(value: float, display_scale: str) -> float:
    if display_scale == "Millions":
        return value / 1_000_000
    if display_scale == "Billions":
        return value / 1_000_000_000
    return value


def currency_suffix(display_scale: str) -> str:
    if display_scale == "Millions":
        return "M"
    if display_scale == "Billions":
        return "B"
    return ""


def format_currency(value: float, display_scale: str = "Full dollars") -> str:
    if pd.isna(value):
        return "N/A"
    scaled = scale_value(float(value), display_scale)
    suffix = currency_suffix(display_scale)
    if display_scale == "Full dollars":
        return f"${scaled:,.2f}"
    return f"${scaled:,.2f}{suffix}"


def format_rate(value: float) -> str:
    if pd.isna(value):
        return "N/A"
    return f"{float(value):.4f}"


def format_percent(value: float) -> str:
    if pd.isna(value):
        return "N/A"
    return f"{float(value) * 100:.2f}%"


def compact_count(value: float) -> str:
    if pd.isna(value):
        return "N/A"
    return f"{int(value):,}"


def to_display_table(df: pd.DataFrame, display_scale: str = "Millions") -> pd.DataFrame:
    out = df.copy()
    for col in out.columns:
        lower = col.lower()
        if lower in {"loan_count", "default_count", "valid_count"}:
            out[col] = out[col].map(compact_count)
        elif any(token in lower for token in ["rate", "share", "percent_difference"]):
            if pd.api.types.is_numeric_dtype(out[col]):
                out[col] = out[col].map(format_percent)
        elif any(token in lower for token in ["ead", "expected_loss", "realized_loss", "difference"]):
            if pd.api.types.is_numeric_dtype(out[col]):
                out[col] = out[col].map(lambda x: format_currency(x, display_scale))
        elif any(
            token in lower
            for token in [
                "pd",
                "lgd",
                "ratio",
                "precision",
                "coefficient",
                "mean_",
                "median_",
                "std_",
                "p05",
                "p25",
                "p75",
                "p95",
            ]
        ):
            if pd.api.types.is_numeric_dtype(out[col]):
                out[col] = out[col].map(format_rate)
    return out.rename(columns=DISPLAY_NAME_OVERRIDES)
