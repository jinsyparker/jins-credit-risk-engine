from __future__ import annotations

import sys
from pathlib import Path

import plotly.express as px
import streamlit as st

APP_DIR = Path(__file__).resolve().parents[1]
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from utils.charts import bar_chart, line_chart
from utils.data_loader import load_table
from utils.formatting import to_display_table


st.set_page_config(page_title="Expected Loss", layout="wide")

st.title("Expected Loss and Portfolio Risk")
st.caption("Baseline Expected Loss decomposition by segment, PD decile, concentration group, and LGD assumption.")

display_scale = st.sidebar.selectbox("Dollar display", ["Full dollars", "Millions", "Billions"], index=1)

segment_options = {
    "grade": "Grade",
    "term": "Term",
    "purpose": "Purpose",
    "pd_decile": "PD Decile",
}
selected = st.selectbox("Segment view", list(segment_options.keys()), format_func=segment_options.get)
segment = load_table(selected)
if not segment.empty:
    st.subheader(f"Baseline Expected Loss by {segment_options[selected]}")
    st.dataframe(to_display_table(segment, display_scale), use_container_width=True, hide_index=True)
    x_col = selected
    if selected == "pd_decile":
        x_col = "pd_decile"
        line_chart(
            segment,
            "pd_decile",
            ["mean_predicted_pd", "realized_default_rate", "expected_loss_rate"],
            "Risk and Expected Loss Rate by PD Decile",
            y_is_percent=True,
        )
    else:
        bar_chart(
            segment.sort_values("total_expected_loss", ascending=False),
            x_col,
            "total_expected_loss",
            "Total Baseline Expected Loss",
            display_scale=display_scale,
            y_is_currency=True,
        )
        bar_chart(
            segment.sort_values("expected_loss_rate", ascending=False),
            x_col,
            "expected_loss_rate",
            "Baseline Expected Loss Rate",
            y_is_percent=True,
        )

concentration = load_table("concentration")
if not concentration.empty:
    st.subheader("Loan-Level Expected Loss Concentration")
    st.dataframe(to_display_table(concentration, display_scale), use_container_width=True, hide_index=True)
    bar_chart(concentration, "top_group", "share_of_total_expected_loss", "Share of Total Expected Loss", y_is_percent=True)

matrix = load_table("pd_ead_matrix")
if not matrix.empty:
    st.subheader("PD x EAD Driver Matrix")
    st.dataframe(to_display_table(matrix.sort_values("total_expected_loss", ascending=False), display_scale), use_container_width=True, hide_index=True)
    if {"predicted_pd_quartile", "ead_proxy_quartile", "share_of_total_expected_loss"}.issubset(matrix.columns):
        heatmap = matrix.pivot(
            index="predicted_pd_quartile",
            columns="ead_proxy_quartile",
            values="share_of_total_expected_loss",
        ) * 100
        fig = px.imshow(
            heatmap,
            aspect="auto",
            title="Share of Total Expected Loss by PD and EAD Quartile",
            labels=dict(x="EAD quartile", y="PD quartile", color="Share of EL (%)"),
        )
        fig.update_layout(height=430, margin=dict(l=10, r=10, t=55, b=10))
        st.plotly_chart(fig, use_container_width=True)

lgd_sensitivity = load_table("el_lgd_sensitivity")
if not lgd_sensitivity.empty:
    st.subheader("LGD Sensitivity")
    st.dataframe(to_display_table(lgd_sensitivity, display_scale), use_container_width=True, hide_index=True)
    bar_chart(
        lgd_sensitivity,
        "scenario_name",
        "total_expected_loss",
        "Portfolio Expected Loss by LGD Definition",
        display_scale=display_scale,
        y_is_currency=True,
    )

reasonableness = load_table("realized_proxy")
if not reasonableness.empty:
    st.subheader("Expected Loss Reasonableness Check")
    st.write(
        "This comparison is an internal consistency check, not independent validation, because the expected-loss and realized-loss proxy calculations use related recovery information."
    )
    st.dataframe(to_display_table(reasonableness, display_scale), use_container_width=True, hide_index=True)
