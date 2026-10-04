from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

APP_DIR = Path(__file__).resolve().parents[1]
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from utils.charts import line_chart
from utils.data_loader import REPORTS_DIR, load_table
from utils.formatting import to_display_table


st.set_page_config(page_title="PD Validation", layout="wide")

st.title("PD Model Validation")
st.caption("Model comparison, embedded underwriting signal ablation, calibration, decile separation, and temporal validation.")

model_comp = load_table("pd_model_comparison")
if not model_comp.empty:
    st.subheader("Model Comparison")
    st.dataframe(to_display_table(model_comp), use_container_width=True, hide_index=True)
    st.write(
        "L2 logistic regression was retained because nonlinear models did not materially improve discrimination, "
        "while the logistic specification preserved interpretability and stability."
    )

feature_comp = load_table("feature_set_comparison")
if not feature_comp.empty:
    st.subheader("Embedded Underwriting Signal Ablation")
    ablation_cols = [
        "model_version",
        "feature_set_description",
        "roc_auc",
        "average_precision_ap",
        "brier_score",
        "highest_lowest_decile_default_rate_ratio",
    ]
    st.dataframe(to_display_table(feature_comp[ablation_cols]), use_container_width=True, hide_index=True)

holdout_vs_oot = load_table("pd_holdout_vs_oot")
if not holdout_vs_oot.empty:
    st.subheader("Random Holdout vs Out-of-Time")
    st.dataframe(to_display_table(holdout_vs_oot), use_container_width=True, hide_index=True)
    st.info(
        "The main model-risk finding is temporal calibration drift. The final OOT split evaluates loans "
        "originated on or after 2016-10-01, and the OOT cohort has an observed default rate above the "
        "model's average predicted PD."
    )

metrics = load_table("pd_validation_metrics")
if not metrics.empty:
    st.subheader("Credit-Risk Validation Metrics")
    st.dataframe(to_display_table(metrics), use_container_width=True, hide_index=True)

deciles = load_table("pd_decile")
if not deciles.empty:
    st.subheader("PD Decile Separation")
    display_cols = [
        "pd_decile",
        "loan_count",
        "mean_predicted_pd",
        "realized_default_rate",
        "expected_loss_rate",
        "share_of_total_expected_loss",
    ]
    st.dataframe(to_display_table(deciles[display_cols]), use_container_width=True, hide_index=True)
    line_chart(
        deciles,
        "pd_decile",
        ["mean_predicted_pd", "realized_default_rate", "expected_loss_rate"],
        "Predicted PD, Observed Default Rate, and EL Rate by Decile",
        y_is_percent=True,
    )

calibration = load_table("calibration")
if not calibration.empty:
    st.subheader("Calibration Method Comparison")
    st.dataframe(to_display_table(calibration), use_container_width=True, hide_index=True)

st.subheader("Reference Figures")
cols = st.columns(3)
figure_paths = [
    REPORTS_DIR / "figures" / "pd_model_family_roc_comparison_v1.png",
    REPORTS_DIR / "figures" / "pd_model_family_pr_comparison_v1.png",
    REPORTS_DIR / "figures" / "random_holdout_vs_out_of_time_validation_v1.png",
]
for col, path in zip(cols, figure_paths):
    if path.exists():
        col.image(str(path), use_container_width=True)
