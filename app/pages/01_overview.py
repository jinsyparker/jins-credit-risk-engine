from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

APP_DIR = Path(__file__).resolve().parents[1]
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from utils.charts import bar_chart
from utils.data_loader import apply_sidebar_filters, load_loans, portfolio_metrics
from utils.formatting import compact_count, format_currency, format_percent, scale_value


st.set_page_config(page_title="Portfolio Overview", layout="wide")


loans, using_demo_data = load_loans()
display_scale = st.sidebar.selectbox("Dollar display", ["Full dollars", "Millions", "Billions"], index=1)
filtered = apply_sidebar_filters(loans)
metrics = portfolio_metrics(filtered)

st.title("Portfolio Overview")
st.caption("Portfolio-level exposure, probability-of-default, LGD, and baseline Expected Loss metrics.")

if using_demo_data:
    st.warning("Using the committed demo sample. Add the full processed loan-level file locally for complete portfolio metrics.")

row1 = st.columns(4)
row1[0].metric("Loans", compact_count(metrics["loan_count"]))
row1[1].metric("Defaulted loans", compact_count(metrics["default_count"]))
row1[2].metric("Observed default rate", format_percent(metrics["observed_default_rate"]))
row1[3].metric("Total EAD", format_currency(metrics["total_ead"], display_scale))

row2 = st.columns(4)
row2[0].metric("Mean predicted PD", format_percent(metrics["mean_predicted_pd"]))
row2[1].metric("Portfolio LGD", format_percent(metrics["portfolio_lgd"]))
row2[2].metric("Baseline Expected Loss", format_currency(metrics["total_expected_loss"], display_scale))
row2[3].metric("Baseline EL rate", format_percent(metrics["expected_loss_rate"]))

left, right = st.columns(2)
with left:
    fig = px.histogram(filtered, x="predicted_pd", nbins=50, title="Predicted PD Distribution")
    fig.update_layout(xaxis_title="Predicted PD", yaxis_title="Loan count", height=420)
    st.plotly_chart(fig, use_container_width=True)

with right:
    plot_df = pd.DataFrame({"baseline_expected_loss": filtered["expected_loss_prelim"].map(lambda value: scale_value(value, display_scale))})
    fig = px.histogram(plot_df, x="baseline_expected_loss", nbins=50, title="Baseline Expected Loss Distribution")
    fig.update_layout(xaxis_title=f"Baseline Expected Loss ({display_scale})", yaxis_title="Loan count", height=420)
    st.plotly_chart(fig, use_container_width=True)

summary_df = pd.DataFrame(
    {
        "metric": ["Total EAD", "Baseline Expected Loss"],
        "value": [metrics["total_ead"], metrics["total_expected_loss"]],
    }
)
bar_chart(summary_df, "metric", "value", "Total EAD vs Baseline Expected Loss", display_scale=display_scale, y_is_currency=True)
