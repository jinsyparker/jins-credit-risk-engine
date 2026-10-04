from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

APP_DIR = Path(__file__).resolve().parents[1]
ROOT_DIR = APP_DIR.parent
SRC_DIR = ROOT_DIR / "src"
for path in [APP_DIR, SRC_DIR]:
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from credit_risk.scenarios import deterministic_expected_loss_scenario
from utils.charts import bar_chart
from utils.data_loader import apply_sidebar_filters, load_loans
from utils.formatting import format_currency, format_percent, to_display_table


st.set_page_config(page_title="Scenario Analysis", layout="wide")

st.title("Expected Loss Scenario Analysis")
st.warning("This is a deterministic sensitivity framework rather than an estimated macroeconomic stress-testing model.")

loans, using_demo_data = load_loans()
display_scale = st.sidebar.selectbox("Dollar display", ["Full dollars", "Millions", "Billions"], index=1)
filtered = apply_sidebar_filters(loans)

if using_demo_data:
    st.info("Using the demo sample. Scenario results are for dashboard demonstration only.")

c1, c2, c3 = st.columns(3)
with c1:
    pd_multiplier = st.slider("PD multiplier", min_value=0.50, max_value=2.00, value=1.00, step=0.05)
with c2:
    lgd_multiplier = st.slider("LGD multiplier", min_value=0.50, max_value=1.50, value=1.00, step=0.05)
with c3:
    ead_multiplier = st.slider("EAD multiplier", min_value=0.75, max_value=1.25, value=1.00, step=0.05)

scenario = deterministic_expected_loss_scenario(
    filtered,
    pd_multiplier=pd_multiplier,
    lgd_multiplier=lgd_multiplier,
    ead_multiplier=ead_multiplier,
)

baseline_el = filtered["expected_loss_prelim"].sum()
baseline_ead = filtered["ead_proxy"].sum()
scenario_el = scenario["scenario_expected_loss"].sum()
scenario_ead = scenario["scenario_ead"].sum()
diff = scenario_el - baseline_el
pct_diff = diff / baseline_el if baseline_el else 0
scenario_el_rate = scenario_el / scenario_ead if scenario_ead else 0

row = st.columns(5)
row[0].metric("Baseline EL", format_currency(baseline_el, display_scale))
row[1].metric("Scenario EL", format_currency(scenario_el, display_scale))
row[2].metric("Difference", format_currency(diff, display_scale))
row[3].metric("Percent difference", format_percent(pct_diff))
row[4].metric("Scenario EL rate", format_percent(scenario_el_rate))

if "grade" in scenario.columns:
    st.subheader("Scenario Expected Loss by Grade")
    grouped = (
        scenario.groupby("grade", dropna=False)
        .agg(
            loan_count=("grade", "size"),
            scenario_ead=("scenario_ead", "sum"),
            scenario_expected_loss=("scenario_expected_loss", "sum"),
        )
        .reset_index()
    )
    grouped["scenario_expected_loss_rate"] = grouped["scenario_expected_loss"] / grouped["scenario_ead"]
    st.dataframe(to_display_table(grouped, display_scale), use_container_width=True, hide_index=True)
    bar_chart(
        grouped.sort_values("scenario_expected_loss", ascending=False),
        "grade",
        "scenario_expected_loss",
        "Scenario Expected Loss by Grade",
        display_scale=display_scale,
        y_is_currency=True,
    )
