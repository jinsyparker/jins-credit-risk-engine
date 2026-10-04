from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.formatting import currency_suffix, scale_value


def bar_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    *,
    display_scale: str = "Millions",
    y_is_currency: bool = False,
    y_is_percent: bool = False,
) -> None:
    if df.empty or x not in df.columns or y not in df.columns:
        st.info("Chart unavailable because the required columns are missing.")
        return
    chart_df = df.copy()
    y_label = y
    if y_is_currency:
        chart_df[y] = chart_df[y].map(lambda value: scale_value(value, display_scale))
        y_label = f"{y} ({currency_suffix(display_scale) or 'dollars'})"
    if y_is_percent:
        chart_df[y] = chart_df[y] * 100
        y_label = f"{y} (%)"
    fig = px.bar(chart_df, x=x, y=y, title=title)
    fig.update_layout(xaxis_title=x, yaxis_title=y_label, height=420, margin=dict(l=10, r=10, t=55, b=10))
    st.plotly_chart(fig, use_container_width=True)


def line_chart(df: pd.DataFrame, x: str, y_columns: list[str], title: str, *, y_is_percent: bool = False) -> None:
    required = [x] + y_columns
    if df.empty or any(col not in df.columns for col in required):
        st.info("Chart unavailable because the required columns are missing.")
        return
    chart_df = df[required].copy()
    y_label = "value"
    if y_is_percent:
        for col in y_columns:
            chart_df[col] = chart_df[col] * 100
        y_label = "percent"
    long_df = chart_df.melt(id_vars=x, value_vars=y_columns, var_name="metric", value_name="value")
    fig = px.line(long_df, x=x, y="value", color="metric", markers=True, title=title)
    fig.update_layout(xaxis_title=x, yaxis_title=y_label, height=420, margin=dict(l=10, r=10, t=55, b=10))
    st.plotly_chart(fig, use_container_width=True)
