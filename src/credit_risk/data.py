from __future__ import annotations

from pathlib import Path

import pandas as pd


DEFAULT_STATUS_MAP = {
    "Fully Paid": 0,
    "Charged Off": 1,
    "Default": 1,
}


def load_csv(path: str | Path, **kwargs) -> pd.DataFrame:
    """Load a CSV file with a path-like input."""
    return pd.read_csv(Path(path), **kwargs)


def create_default_flag(
    data: pd.DataFrame,
    status_column: str = "loan_status",
    target_column: str = "default_flag",
) -> pd.DataFrame:
    """Create the documented binary default target from resolved loan statuses."""
    if status_column not in data.columns:
        raise KeyError(f"Missing status column: {status_column}")
    out = data.copy()
    out[target_column] = out[status_column].map(DEFAULT_STATUS_MAP)
    return out


def filter_resolved_loans(data: pd.DataFrame, target_column: str = "default_flag") -> pd.DataFrame:
    """Keep rows with a resolved target value."""
    if target_column not in data.columns:
        raise KeyError(f"Missing target column: {target_column}")
    return data.loc[data[target_column].notna()].copy()


def parse_percent(series: pd.Series) -> pd.Series:
    """Convert percentage strings such as '13.5%' to floating-point percentages."""
    return pd.to_numeric(series.astype(str).str.replace("%", "", regex=False), errors="coerce")


def parse_term_months(series: pd.Series) -> pd.Series:
    """Extract loan term in months from LendingClub term strings."""
    return pd.to_numeric(series.astype(str).str.extract(r"(\\d+)")[0], errors="coerce")


def parse_emp_length(series: pd.Series) -> pd.Series:
    """Convert LendingClub employment length strings to numeric years."""
    cleaned = series.astype(str).str.strip().str.lower()
    cleaned = cleaned.replace({"nan": None, "n/a": None, "< 1 year": "0", "10+ years": "10"})
    return pd.to_numeric(cleaned.str.extract(r"(\\d+)")[0], errors="coerce")


def clean_lendingclub_fields(data: pd.DataFrame) -> pd.DataFrame:
    """Apply the core field conversions used by the project notebooks."""
    out = data.copy()
    if "int_rate" in out.columns:
        out["int_rate"] = parse_percent(out["int_rate"])
    if "revol_util" in out.columns:
        out["revol_util"] = parse_percent(out["revol_util"])
    if "term" in out.columns:
        out["term"] = parse_term_months(out["term"])
    if "emp_length" in out.columns:
        out["emp_length"] = parse_emp_length(out["emp_length"])
    return out
