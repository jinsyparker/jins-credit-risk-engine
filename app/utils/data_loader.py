from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "processed"
DEMO_DIR = BASE_DIR / "data" / "demo"
REPORTS_DIR = BASE_DIR / "reports"

CORE_LOAN_FILE = DATA_DIR / "loans_with_pd_lgd_ead_v1.csv"
DEMO_LOAN_FILE = DEMO_DIR / "loans_with_pd_lgd_ead_sample_v1.csv"

CORE_LOAN_COLUMNS = [
    "predicted_pd",
    "lgd_estimate",
    "ead_proxy",
    "expected_loss_prelim",
    "default_flag",
    "grade",
    "term",
    "purpose",
    "issue_year",
    "issue_d",
    "pd_risk_decile",
]

DATA_FILES = {
    "grade": DATA_DIR / "expected_loss_by_grade_v1.csv",
    "sub_grade": DATA_DIR / "expected_loss_by_sub_grade_v1.csv",
    "term": DATA_DIR / "expected_loss_by_term_v1.csv",
    "purpose": DATA_DIR / "expected_loss_by_purpose_v1.csv",
    "issue_year": DATA_DIR / "expected_loss_by_issue_year_v1.csv",
    "pd_decile": DATA_DIR / "expected_loss_by_pd_decile_v1.csv",
    "concentration": DATA_DIR / "expected_loss_top_concentration_v1.csv",
    "pd_ead_matrix": DATA_DIR / "expected_loss_pd_ead_matrix_v1.csv",
    "lgd_sensitivity": DATA_DIR / "lgd_sensitivity_summary_v1.csv",
    "el_lgd_sensitivity": DATA_DIR / "expected_loss_lgd_sensitivity_summary_v1.csv",
    "realized_proxy": DATA_DIR / "realized_vs_expected_loss_summary_v1.csv",
    "pd_model_comparison": REPORTS_DIR / "tables" / "pd_model_comparison_readme_v1.csv",
    "pd_holdout_vs_oot": REPORTS_DIR / "tables" / "pd_holdout_vs_oot_v1.csv",
    "pd_validation_metrics": REPORTS_DIR / "tables" / "pd_validation_metrics_v1.csv",
    "feature_set_comparison": REPORTS_DIR / "tables" / "pd_model_feature_set_comparison_v1.csv",
    "calibration": REPORTS_DIR / "tables" / "pd_calibration_model_comparison_v1.csv",
    "coefficients": REPORTS_DIR / "tables" / "pd_coefficients_v1.csv",
}


def existing_path(path: Path) -> bool:
    return path.exists() and path.is_file()


@st.cache_data(show_spinner=False)
def read_csv_cached(path_str: str, usecols: tuple[str, ...] | None = None) -> pd.DataFrame:
    path = Path(path_str)
    if not existing_path(path):
        return pd.DataFrame()
    if usecols is None:
        return pd.read_csv(path)
    available = pd.read_csv(path, nrows=0).columns.tolist()
    selected = [col for col in usecols if col in available]
    return pd.read_csv(path, usecols=selected)


def ensure_issue_year(df: pd.DataFrame) -> pd.DataFrame:
    if "issue_year" in df.columns:
        return df
    if "issue_d" not in df.columns:
        return df
    out = df.copy()
    parsed = pd.to_datetime(out["issue_d"], format="%b-%Y", errors="coerce")
    if parsed.isna().all():
        parsed = pd.to_datetime(out["issue_d"], errors="coerce")
    out["issue_year"] = parsed.dt.year
    return out


def load_loans() -> tuple[pd.DataFrame, bool]:
    active_file = CORE_LOAN_FILE if existing_path(CORE_LOAN_FILE) else DEMO_LOAN_FILE
    using_demo = active_file == DEMO_LOAN_FILE
    loans = read_csv_cached(str(active_file), tuple(CORE_LOAN_COLUMNS))
    if loans.empty:
        st.error(
            "Required dashboard data is missing. Add either "
            f"{CORE_LOAN_FILE.relative_to(BASE_DIR)} or {DEMO_LOAN_FILE.relative_to(BASE_DIR)}."
        )
        st.stop()
    loans = ensure_issue_year(loans)
    return loans, using_demo


def load_table(name: str) -> pd.DataFrame:
    return read_csv_cached(str(DATA_FILES[name]))


def portfolio_metrics(df: pd.DataFrame) -> dict[str, float]:
    total_ead = df["ead_proxy"].sum()
    total_el = df["expected_loss_prelim"].sum()
    return {
        "loan_count": len(df),
        "default_count": df["default_flag"].sum() if "default_flag" in df.columns else np.nan,
        "observed_default_rate": df["default_flag"].mean() if "default_flag" in df.columns else np.nan,
        "total_ead": total_ead,
        "mean_predicted_pd": df["predicted_pd"].mean(),
        "portfolio_lgd": df["lgd_estimate"].mean(),
        "total_expected_loss": total_el,
        "expected_loss_rate": total_el / total_ead if total_ead else np.nan,
    }


def apply_sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    filtered = df.copy()
    st.sidebar.markdown("### Filters")
    st.sidebar.caption("Filters apply to loan-level views and scenario analysis.")

    if "grade" in filtered.columns:
        grades = sorted(filtered["grade"].dropna().astype(str).unique().tolist())
        selected = st.sidebar.multiselect("Grade", grades)
        if selected:
            filtered = filtered[filtered["grade"].astype(str).isin(selected)]

    if "term" in filtered.columns:
        terms = sorted(filtered["term"].dropna().unique().tolist(), key=lambda value: str(value))
        selected = st.sidebar.multiselect("Term", terms)
        if selected:
            filtered = filtered[filtered["term"].isin(selected)]

    if "purpose" in filtered.columns:
        purposes = sorted(filtered["purpose"].dropna().astype(str).unique().tolist())
        selected = st.sidebar.multiselect("Purpose", purposes)
        if selected:
            filtered = filtered[filtered["purpose"].astype(str).isin(selected)]

    if "issue_year" in filtered.columns:
        years = sorted([int(y) for y in filtered["issue_year"].dropna().unique().tolist()])
        selected = st.sidebar.multiselect("Issue year", years)
        if selected:
            filtered = filtered[filtered["issue_year"].isin(selected)]

    if filtered.empty:
        st.error("No loans match the selected filters.")
        st.stop()

    return filtered
