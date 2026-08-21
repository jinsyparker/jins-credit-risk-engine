from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import Iterable
from xml.sax.saxutils import escape

import numpy as np
import pandas as pd
import streamlit as st

try:
    import plotly.express as px

    HAS_PLOTLY = True
except Exception:
    HAS_PLOTLY = False

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

    HAS_REPORTLAB = True
except Exception:
    HAS_REPORTLAB = False


st.set_page_config(
    page_title="Credit Risk Portfolio Dashboard",
    layout="wide",
)


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data" / "processed"
REPORTS_DIR = BASE_DIR / "reports"

CORE_LOAN_FILE = DATA_DIR / "loans_with_pd_lgd_ead_v1.csv"
DEMO_LOAN_FILE = BASE_DIR / "data" / "demo" / "loans_with_pd_lgd_ead_sample_v1.csv"
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

CORE_REQUIRED_COLUMNS = [
    "predicted_pd",
    "lgd_estimate",
    "ead_proxy",
    "expected_loss_prelim",
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
}

REPORT_FILES = {
    "final_summary": REPORTS_DIR / "final_credit_risk_project_summary.md",
    "review_and_defense": REPORTS_DIR / "final_credit_risk_project_review_and_defense.md",
}

FINAL_SUMMARY_MARKDOWN = """
## Final Credit Risk Project Summary

This project builds an end-to-end analytical credit risk workflow using LendingClub accepted-loan data. The workflow defines a default target, estimates Probability of Default, prepares LGD and EAD, and combines them into preliminary Expected Loss.

The final framework is designed for portfolio analysis, segmentation, risk ranking, and project presentation. It is not a production underwriting, pricing, accounting reserve, CECL, IFRS 9, Basel, or capital model.

### Final Framework

| component | selected approach |
| --- | --- |
| Dataset | LendingClub accepted loans |
| Target | `Fully Paid = 0`; `Charged Off / Default = 1` |
| PD model | Uncalibrated L2 Logistic Regression using Feature Set A |
| Final PD column | `predicted_pd` |
| LGD | Recovery-based portfolio-average LGD from defaulted loans |
| EAD | Funded amount |
| Expected Loss | `predicted_pd x lgd_estimate x ead_proxy` |

### Headline Metrics

| metric | value |
| --- | ---: |
| Final cleaned loans | 1,345,350 |
| Defaulted loans | 268,599 |
| Observed default rate | 19.96% |
| Mean predicted PD | 0.1997 |
| Portfolio-average LGD | 0.9247 |
| Total EAD | $19.39B |
| Total preliminary Expected Loss | $3.86B |
| Expected Loss rate | 19.92% |
| Highest PD decile share of total EL | 28.31% |
| Top 10% loan-level EL concentration share | 34.15% |
| Baseline EL / gross recovery realized proxy ratio | 1.0023 |

### PD Modeling Summary

The selected PD model is an uncalibrated L2 Logistic Regression using Feature Set A. Feature Set A includes LendingClub `grade`, `sub_grade`, and `int_rate`, which provide strong risk-ranking signal but also reflect LendingClub's own embedded risk assessment and pricing.

The final model was selected after feature set comparison, borrower-only sensitivity, model family comparison, and calibration testing. Tree-based models did not materially outperform logistic regression, and calibration did not materially improve the final PD model.

Final model metrics include:

| metric | value |
| --- | ---: |
| ROC-AUC | 0.7084 |
| PR-AUC | 0.3689 |
| Brier Score | 0.1455 |
| Log Loss | 0.4553 |
| High/low decile default-rate ratio | 10.6081 |

### Expected Loss and Portfolio Risk

The project combines PD, LGD, and EAD into preliminary loan-level Expected Loss. Because LGD is constant in the main framework, variation in Expected Loss is mainly driven by predicted PD and funded amount exposure.

Key portfolio findings:

- Grade C contributes the most total Expected Loss.
- Grade G has the highest Expected Loss rate.
- Expected Loss rates increase across PD deciles.
- The highest PD decile contributes 28.31% of total Expected Loss.
- The top 10% of loans by Expected Loss contribute 34.15% of total Expected Loss.
- The highest PD and highest EAD quartile cell contributes 29.22% of total Expected Loss.

### LGD Sensitivity

The baseline LGD is recovery-based and estimated from defaulted loans. Milestone 8 tested several alternative LGD definitions to evaluate sensitivity.

| LGD scenario | mean LGD | total Expected Loss | difference vs baseline |
| --- | ---: | ---: | ---: |
| Baseline gross recovery LGD | 0.9247 | $3.86B | 0.00% |
| Net recovery fee LGD | 0.9372 | $3.91B | 1.35% |
| Principal recovery LGD | 0.6973 | $2.91B | -24.59% |
| Total payment LGD | 0.4670 | $1.95B | -49.50% |
| Net cashflow LGD | 0.4135 | $1.73B | -55.28% |

Recovery-based definitions are close to the baseline. Payment-inclusive definitions produce much lower Expected Loss because they may include borrower payments made before default.

### Realized Loss Proxy Check

Baseline Expected Loss aligns closely with the gross recovery realized loss proxy.

| metric | value |
| --- | ---: |
| Baseline Expected Loss | $3.86B |
| Gross recovery realized loss proxy | $3.85B |
| Ratio of baseline EL to gross recovery proxy | 1.0023 |

This comparison supports the reasonableness of the recovery-based baseline, while remaining a proxy comparison rather than production validation.

### Key Limitations

- The framework is project-ready, not production-ready.
- The PD model relies on LendingClub `grade`, `sub_grade`, and `int_rate`.
- Time validation showed underprediction on newer loans.
- EAD is funded amount, not actual balance at default.
- LGD is a portfolio-average recovery-based estimate.
- LGD is constant across loans in the main Expected Loss framework.
- Payment-inclusive LGD definitions may mix pre-default and post-default cashflows.
- The dataset includes accepted loans only.
- The output is not a CECL, IFRS 9, Basel, pricing, underwriting, reserve, or capital model.

### Final Conclusion

The project successfully demonstrates a complete credit risk analytics workflow from cleaned loan outcomes to PD, LGD, EAD, Expected Loss, portfolio decomposition, LGD sensitivity, and realized proxy comparison.

The final framework is transparent, interpretable, and useful for portfolio-level analysis. Its results should be understood as analytical project outputs rather than production credit decisions or accounting estimates.
"""

PROJECT_REVIEW_MARKDOWN = """
## Project Review and Defense

This project is best understood as an end-to-end analytical credit risk framework. It is designed to demonstrate the full modeling workflow from loan performance data to PD, LGD, EAD, Expected Loss, segmentation, sensitivity testing, and portfolio interpretation.

The framework is suitable for portfolio analysis and project presentation. It is not intended to be a production underwriting, pricing, accounting reserve, CECL, IFRS 9, Basel, or capital model.

### What the Project Demonstrates Well

| area | review |
| --- | --- |
| End-to-end workflow | The project connects target definition, PD modeling, LGD/EAD preparation, Expected Loss calculation, and portfolio decomposition. |
| PD model validation | The project compares feature sets, model families, calibration approaches, risk deciles, and time validation results. |
| Final PD choice | The selected model is an uncalibrated L2 Logistic Regression using Feature Set A. It is transparent, stable, and performs competitively against tested alternatives. |
| Portfolio risk interpretation | Expected Loss is decomposed by grade, sub-grade, term, purpose, issue year, PD decile, concentration group, and PD/EAD driver cells. |
| LGD sensitivity | Alternative LGD definitions show how Expected Loss changes under recovery-based and payment-inclusive assumptions. |
| Realized proxy comparison | Baseline Expected Loss is compared with realized loss proxies as a reasonableness check. |

### Key Results to Highlight

| metric | value |
| --- | ---: |
| Final cleaned loans | 1,345,350 |
| Defaulted loans | 268,599 |
| Mean predicted PD | 0.1997 |
| Portfolio-average baseline LGD | 0.9247 |
| Total EAD | $19.39B |
| Total preliminary Expected Loss | $3.86B |
| Expected Loss rate | 19.92% |
| Highest PD decile share of total EL | 28.31% |
| Top 10% loan-level EL concentration share | 34.15% |
| Baseline EL / gross recovery realized proxy ratio | 1.0023 |

### Main Limitations

| limitation | interpretation |
| --- | --- |
| Feature Set A uses LendingClub `grade`, `sub_grade`, and `int_rate`. | These fields improve predictive power, but they also reflect LendingClub's embedded risk assessment and pricing. |
| Time validation showed underprediction on newer loans. | The model should be recalibrated and monitored before any production use. |
| EAD is funded amount. | Funded amount is a transparent first proxy, but it is not the same as balance at default. |
| LGD is a portfolio-average recovery-based estimate. | This is stable and easy to explain, but it does not capture loan-level LGD variation. |
| Payment-inclusive LGD definitions produce much lower EL. | These scenarios are useful sensitivity checks, but they may include pre-default borrower payments. |
| Accepted loans only. | The project analyzes accepted-loan performance, not rejected applications or approval policy. |

### Reviewer Questions

| question | answer |
| --- | --- |
| Why use logistic regression? | Logistic regression was competitive with more complex models, easier to interpret, and stable for a project-level PD framework. |
| Why keep LendingClub grade and pricing fields? | They are predictive and useful for portfolio risk analysis. The project also includes borrower-only comparisons to show their impact. |
| Why not use a calibrated model? | Calibration methods did not materially improve the final model, so the simpler uncalibrated L2 model was retained. |
| Why is LGD high? | The recovery-based LGD reflects low observed recoveries relative to funded amount among defaulted loans. |
| Why use portfolio-average LGD? | It provides a stable first baseline and avoids overfitting thin segment-level LGD patterns. |
| What does Expected Loss represent here? | It is a project-level portfolio risk measure calculated as PD x LGD x EAD, not a booked reserve or regulatory capital estimate. |
| Is this production-ready? | No. It is a project-ready analytical framework. Production use would require stronger validation, recalibration, monitoring, governance, and better LGD/EAD inputs. |

### Final Position

The project is a coherent and defensible analytical credit risk framework. Its main value is that it demonstrates the complete risk modeling process: defining default, estimating PD, preparing LGD and EAD, calculating Expected Loss, decomposing portfolio risk, testing LGD sensitivity, and comparing results with realized loss proxies.

The final framework is transparent, interpretable, and useful for portfolio analysis. Its limitations are clearly identified, and the natural next steps are calibration improvement, stress testing, borrower-only sensitivity, segment-level LGD exploration, and better EAD measurement if balance-at-default data becomes available.
"""


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


@st.cache_data(show_spinner=False)
def read_text_cached(path_str: str) -> str:
    path = Path(path_str)
    if not existing_path(path):
        return ""
    return path.read_text(encoding="utf-8")


def markdown_to_pdf_bytes(title: str, markdown_text: str) -> bytes | None:
    if not HAS_REPORTLAB or not markdown_text:
        return None

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=48,
        leftMargin=48,
        topMargin=48,
        bottomMargin=48,
        title=title,
    )
    styles = getSampleStyleSheet()
    story = [Paragraph(escape(title), styles["Title"]), Spacer(1, 12)]

    in_code_block = False
    code_lines: list[str] = []

    def flush_code_block() -> None:
        if code_lines:
            text = "<br/>".join(escape(line) for line in code_lines)
            story.append(Paragraph(f"<font name='Courier'>{text}</font>", styles["BodyText"]))
            story.append(Spacer(1, 8))
            code_lines.clear()

    for raw_line in markdown_text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()

        if stripped.startswith("```"):
            if in_code_block:
                flush_code_block()
                in_code_block = False
            else:
                in_code_block = True
            continue

        if in_code_block:
            code_lines.append(line)
            continue

        if not stripped:
            story.append(Spacer(1, 6))
            continue

        if stripped.startswith("|"):
            if stripped.replace("|", "").replace("-", "").replace(":", "").strip():
                cells = [cell.strip().strip("`") for cell in stripped.strip("|").split("|")]
                text = " | ".join(cells)
                story.append(Paragraph(f"<font name='Courier'>{escape(text)}</font>", styles["BodyText"]))
            continue

        style = styles["BodyText"]
        text = stripped

        if stripped.startswith("### "):
            style = styles["Heading3"]
            text = stripped[4:]
        elif stripped.startswith("## "):
            style = styles["Heading2"]
            text = stripped[3:]
        elif stripped.startswith("# "):
            style = styles["Heading1"]
            text = stripped[2:]
        elif stripped.startswith("- "):
            text = "- " + stripped[2:]

        text = text.replace("**", "").replace("`", "")
        story.append(Paragraph(escape(text), style))

    flush_code_block()
    doc.build(story)
    return buffer.getvalue()


def report_pdf_download(label: str, title: str, markdown_text: str, file_name: str) -> None:
    if not HAS_REPORTLAB:
        st.warning("PDF downloads require `reportlab`. Install app requirements, then restart Streamlit.")
        return

    pdf_bytes = markdown_to_pdf_bytes(title, markdown_text)
    if not pdf_bytes:
        st.warning("PDF could not be generated because the report text is unavailable.")
        return

    st.download_button(
        label,
        data=pdf_bytes,
        file_name=file_name,
        mime="application/pdf",
    )


def validate_required_columns(df: pd.DataFrame, columns: Iterable[str], label: str) -> list[str]:
    return [col for col in columns if col not in df.columns]


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


def to_display_table(df: pd.DataFrame, display_scale: str) -> pd.DataFrame:
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
        elif any(token in lower for token in ["pd", "lgd", "ratio", "mean_", "median_", "std_", "p05", "p25", "p75", "p95"]):
            if pd.api.types.is_numeric_dtype(out[col]):
                out[col] = out[col].map(format_rate)
    return out


def chart_bar(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    display_scale: str = "Full dollars",
    y_is_currency: bool = False,
    y_is_percent: bool = False,
):
    if df.empty or x not in df.columns or y not in df.columns:
        st.info("Chart unavailable because the required columns are missing.")
        return

    chart_df = df.copy()
    y_label = y
    if y_is_currency:
        chart_df[y] = chart_df[y].map(lambda value: scale_value(value, display_scale))
        suffix = currency_suffix(display_scale)
        y_label = f"{y} ({suffix or 'dollars'})"
    elif y_is_percent:
        chart_df[y] = chart_df[y] * 100
        y_label = f"{y} (%)"

    if HAS_PLOTLY:
        fig = px.bar(chart_df, x=x, y=y, title=title)
        fig.update_layout(xaxis_title=x, yaxis_title=y_label, height=430, margin=dict(l=10, r=10, t=55, b=10))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.subheader(title)
        st.bar_chart(chart_df.set_index(x)[y])


def chart_line(
    df: pd.DataFrame,
    x: str,
    y_columns: list[str],
    title: str,
    y_is_percent: bool = False,
):
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

    if HAS_PLOTLY:
        long_df = chart_df.melt(id_vars=x, value_vars=y_columns, var_name="metric", value_name="value")
        fig = px.line(long_df, x=x, y="value", color="metric", markers=True, title=title)
        fig.update_layout(xaxis_title=x, yaxis_title=y_label, height=430, margin=dict(l=10, r=10, t=55, b=10))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.subheader(title)
        st.line_chart(chart_df.set_index(x))


def metric_card(label: str, value: str, help_text: str | None = None):
    st.metric(label=label, value=value, help=help_text)


def apply_sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    filtered = df.copy()

    st.sidebar.markdown("### Optional Filters")
    st.sidebar.caption("Leave a filter blank to keep all values. Filters apply to loan-level pages and stress testing.")

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

    return filtered


def portfolio_metrics(df: pd.DataFrame) -> dict[str, float]:
    total_ead = df["ead_proxy"].sum()
    total_el = df["expected_loss_prelim"].sum()
    metrics = {
        "loan_count": len(df),
        "default_count": df["default_flag"].sum() if "default_flag" in df.columns else np.nan,
        "observed_default_rate": df["default_flag"].mean() if "default_flag" in df.columns else np.nan,
        "total_ead": total_ead,
        "mean_predicted_pd": df["predicted_pd"].mean(),
        "portfolio_lgd": df["lgd_estimate"].mean(),
        "total_el": total_el,
        "el_rate": total_el / total_ead if total_ead else np.nan,
    }

    if "pd_risk_decile" in df.columns and total_el:
        top_decile = df["pd_risk_decile"].max()
        metrics["top_pd_decile_el_share"] = df.loc[df["pd_risk_decile"].eq(top_decile), "expected_loss_prelim"].sum() / total_el
    else:
        metrics["top_pd_decile_el_share"] = np.nan

    if total_el and len(df):
        top_n = max(1, int(np.ceil(len(df) * 0.10)))
        metrics["top_10pct_el_share"] = df.nlargest(top_n, "expected_loss_prelim")["expected_loss_prelim"].sum() / total_el
    else:
        metrics["top_10pct_el_share"] = np.nan

    return metrics


def load_optional(name: str) -> pd.DataFrame:
    return read_csv_cached(str(DATA_FILES[name]))


def render_overview(loans: pd.DataFrame, display_scale: str):
    st.title("Credit Risk Portfolio Dashboard")
    st.caption("Presentation and exploration layer over completed LendingClub credit risk project outputs.")
    st.info(
        "This dashboard visualizes final project outputs. It is a portfolio analytics tool, not a production underwriting system."
    )

    metrics = portfolio_metrics(loans)

    row1 = st.columns(4)
    with row1[0]:
        metric_card("Loans", compact_count(metrics["loan_count"]))
    with row1[1]:
        metric_card("Defaulted loans", compact_count(metrics["default_count"]))
    with row1[2]:
        metric_card("Observed default rate", format_percent(metrics["observed_default_rate"]))
    with row1[3]:
        metric_card("Total EAD", format_currency(metrics["total_ead"], display_scale))

    row2 = st.columns(4)
    with row2[0]:
        metric_card("Mean predicted PD", format_rate(metrics["mean_predicted_pd"]))
    with row2[1]:
        metric_card("Portfolio-average LGD", format_rate(metrics["portfolio_lgd"]))
    with row2[2]:
        metric_card("Total preliminary EL", format_currency(metrics["total_el"], display_scale))
    with row2[3]:
        metric_card("Expected Loss rate", format_percent(metrics["el_rate"]))

    row3 = st.columns(2)
    with row3[0]:
        metric_card("Highest PD decile EL share", format_percent(metrics["top_pd_decile_el_share"]))
    with row3[1]:
        metric_card("Top 10% loan-level EL share", format_percent(metrics["top_10pct_el_share"]))

    st.markdown("### Portfolio Distributions")
    left, right = st.columns(2)
    with left:
        if HAS_PLOTLY:
            fig = px.histogram(loans, x="predicted_pd", nbins=50, title="Predicted PD Distribution")
            fig.update_layout(xaxis_title="predicted_pd", yaxis_title="Loan count", height=420)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.subheader("Predicted PD Distribution")
            hist = pd.cut(loans["predicted_pd"], bins=50).value_counts().sort_index()
            hist.index = hist.index.astype(str)
            st.bar_chart(hist)

    with right:
        plot_df = loans[["expected_loss_prelim"]].copy()
        plot_df["expected_loss_prelim"] = plot_df["expected_loss_prelim"].map(lambda value: scale_value(value, display_scale))
        label = f"expected_loss_prelim ({currency_suffix(display_scale) or 'dollars'})"
        if HAS_PLOTLY:
            fig = px.histogram(plot_df, x="expected_loss_prelim", nbins=50, title="Expected Loss Distribution")
            fig.update_layout(xaxis_title=label, yaxis_title="Loan count", height=420)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.subheader("Expected Loss Distribution")
            hist = pd.cut(plot_df["expected_loss_prelim"], bins=50).value_counts().sort_index()
            hist.index = hist.index.astype(str)
            st.bar_chart(hist)

    summary_df = pd.DataFrame(
        {
            "metric": ["Total EAD", "Total preliminary Expected Loss"],
            "value": [metrics["total_ead"], metrics["total_el"]],
        }
    )
    chart_bar(summary_df, "metric", "value", "Total EAD vs Preliminary Expected Loss", display_scale, y_is_currency=True)


def render_segment_analysis(display_scale: str):
    st.title("Segment Analysis")
    st.caption("Precomputed full-portfolio segment outputs from Milestone 7.")
    st.write(
        "Total Expected Loss reflects both exposure volume and risk. Expected Loss rate is risk intensity per dollar of EAD."
    )

    segment_map = {
        "grade": "Grade",
        "sub_grade": "Sub-grade",
        "term": "Term",
        "purpose": "Purpose",
        "issue_year": "Issue year",
    }
    selected_key = st.selectbox("Choose segment dimension", list(segment_map.keys()), format_func=segment_map.get)
    df = load_optional(selected_key)
    if df.empty:
        st.warning(f"Segment file missing or empty: {DATA_FILES[selected_key]}")
        return

    segment_col = selected_key
    columns = [
        col
        for col in [
            segment_col,
            "loan_count",
            "default_count",
            "realized_default_rate",
            "total_ead",
            "total_expected_loss",
            "expected_loss_rate",
            "mean_predicted_pd",
        ]
        if col in df.columns
    ]
    st.dataframe(to_display_table(df[columns], display_scale), use_container_width=True, hide_index=True)

    sort_df = df.sort_values("total_expected_loss", ascending=False) if "total_expected_loss" in df.columns else df
    chart_bar(sort_df, segment_col, "total_expected_loss", "Total Expected Loss by Segment", display_scale, y_is_currency=True)

    rate_df = df.sort_values("expected_loss_rate", ascending=False) if "expected_loss_rate" in df.columns else df
    chart_bar(rate_df, segment_col, "expected_loss_rate", "Expected Loss Rate by Segment", y_is_percent=True)

    if "mean_predicted_pd" in df.columns:
        pd_df = df.sort_values("mean_predicted_pd", ascending=False)
        chart_bar(pd_df, segment_col, "mean_predicted_pd", "Mean Predicted PD by Segment")


def render_pd_deciles(display_scale: str):
    st.title("PD Deciles")
    st.write(
        "PD deciles test whether the model ranks risk. A useful ranking should show increasing realized default rates and EL rates across deciles."
    )

    df = load_optional("pd_decile")
    if df.empty:
        st.warning(f"PD decile file missing or empty: {DATA_FILES['pd_decile']}")
        return

    columns = [
        col
        for col in [
            "pd_decile",
            "loan_count",
            "default_count",
            "mean_predicted_pd",
            "realized_default_rate",
            "total_ead",
            "total_expected_loss",
            "expected_loss_rate",
            "share_of_total_expected_loss",
            "cumulative_share_of_total_expected_loss",
        ]
        if col in df.columns
    ]
    st.dataframe(to_display_table(df[columns], display_scale), use_container_width=True, hide_index=True)

    chart_line(
        df,
        "pd_decile",
        [col for col in ["mean_predicted_pd", "realized_default_rate", "expected_loss_rate"] if col in df.columns],
        "Predicted PD, Realized Default Rate, and EL Rate by Decile",
        y_is_percent=True,
    )
    chart_bar(df, "pd_decile", "share_of_total_expected_loss", "Share of Total Expected Loss by Decile", y_is_percent=True)
    if "cumulative_share_of_total_expected_loss" in df.columns:
        chart_line(
            df,
            "pd_decile",
            ["cumulative_share_of_total_expected_loss"],
            "Cumulative Share of Total Expected Loss",
            y_is_percent=True,
        )


def render_concentration(loans: pd.DataFrame, display_scale: str):
    st.title("Expected Loss Concentration")
    st.write(
        "Concentration analysis identifies whether a small share of loans drives a large share of portfolio Expected Loss."
    )

    df = load_optional("concentration")
    if not df.empty:
        st.subheader("Precomputed Concentration Groups")
        st.dataframe(to_display_table(df, display_scale), use_container_width=True, hide_index=True)
        chart_bar(df, "top_group", "share_of_total_expected_loss", "Share of Total Expected Loss by Group", y_is_percent=True)
        chart_bar(df, "top_group", "share_of_total_ead", "Share of Total EAD by Group", y_is_percent=True)

    st.subheader("Loan-Level Cumulative Concentration Curve")
    total_el = loans["expected_loss_prelim"].sum()
    if total_el <= 0 or loans.empty:
        st.info("Concentration curve unavailable because filtered Expected Loss is zero or no loans are selected.")
        return

    ordered = loans[["expected_loss_prelim"]].sort_values("expected_loss_prelim", ascending=False).reset_index(drop=True)
    n = len(ordered)
    sample_size = min(1000, n)
    sample_idx = np.unique(np.linspace(0, n - 1, sample_size).astype(int))
    curve = pd.DataFrame(
        {
            "cumulative_share_of_loans": (sample_idx + 1) / n,
            "cumulative_share_of_expected_loss": ordered["expected_loss_prelim"].cumsum().iloc[sample_idx].to_numpy() / total_el,
        }
    )
    curve = pd.concat(
        [
            pd.DataFrame({"cumulative_share_of_loans": [0.0], "cumulative_share_of_expected_loss": [0.0]}),
            curve,
        ],
        ignore_index=True,
    )
    chart_line(
        curve,
        "cumulative_share_of_loans",
        ["cumulative_share_of_expected_loss"],
        "Cumulative Share of Expected Loss by Loan Rank",
        y_is_percent=True,
    )

    matrix = load_optional("pd_ead_matrix")
    if not matrix.empty:
        st.subheader("PD x EAD Driver Matrix")
        matrix_cols = [
            col
            for col in [
                "predicted_pd_quartile",
                "ead_proxy_quartile",
                "loan_count",
                "mean_predicted_pd",
                "mean_ead",
                "total_ead",
                "mean_expected_loss",
                "total_expected_loss",
                "share_of_total_expected_loss",
            ]
            if col in matrix.columns
        ]
        st.dataframe(
            to_display_table(matrix.sort_values("total_expected_loss", ascending=False)[matrix_cols], display_scale),
            use_container_width=True,
            hide_index=True,
        )
        if HAS_PLOTLY and {"predicted_pd_quartile", "ead_proxy_quartile", "share_of_total_expected_loss"}.issubset(matrix.columns):
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


def render_lgd_sensitivity(display_scale: str):
    st.title("LGD Sensitivity")
    st.write(
        "Recovery-based LGD is the main project baseline. Payment-inclusive LGD definitions are sensitivity checks because they may include pre-default borrower payments."
    )

    lgd_df = load_optional("lgd_sensitivity")
    el_df = load_optional("el_lgd_sensitivity")
    realized_df = load_optional("realized_proxy")

    if lgd_df.empty:
        st.warning(f"LGD sensitivity file missing or empty: {DATA_FILES['lgd_sensitivity']}")
    else:
        st.subheader("LGD Definition Summary")
        lgd_cols = [
            col
            for col in [
                "lgd_definition",
                "valid_count",
                "mean_lgd",
                "median_lgd",
                "std_lgd",
                "share_lgd_eq_1",
                "share_lgd_eq_0",
                "share_clipped",
            ]
            if col in lgd_df.columns
        ]
        st.dataframe(to_display_table(lgd_df[lgd_cols], display_scale), use_container_width=True, hide_index=True)
        chart_bar(lgd_df, "lgd_definition", "mean_lgd", "Mean LGD by Definition")

    if el_df.empty:
        st.warning(f"Expected Loss LGD sensitivity file missing or empty: {DATA_FILES['el_lgd_sensitivity']}")
    else:
        st.subheader("Expected Loss by LGD Scenario")
        st.dataframe(to_display_table(el_df, display_scale), use_container_width=True, hide_index=True)
        chart_bar(el_df, "scenario_name", "total_expected_loss", "Total Expected Loss by LGD Scenario", display_scale, y_is_currency=True)
        chart_bar(
            el_df,
            "scenario_name",
            "percent_difference_vs_baseline_total_el",
            "Percent Difference vs Baseline Total EL",
            y_is_percent=True,
        )

        scenario_options = el_df["scenario_name"].tolist()
        scenario = st.selectbox("Select LGD scenario", scenario_options)
        selected = el_df.loc[el_df["scenario_name"].eq(scenario)].iloc[0]
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Portfolio average LGD", format_rate(selected.get("portfolio_avg_lgd", np.nan)))
        c2.metric("Total Expected Loss", format_currency(selected.get("total_expected_loss", np.nan), display_scale))
        c3.metric("Expected Loss rate", format_percent(selected.get("expected_loss_rate", np.nan)))
        c4.metric("Difference vs baseline", format_currency(selected.get("difference_vs_baseline_total_el", np.nan), display_scale))

    if realized_df.empty:
        st.warning(f"Realized loss proxy file missing or empty: {DATA_FILES['realized_proxy']}")
    else:
        st.subheader("Realized Loss Proxy Comparison")
        st.dataframe(to_display_table(realized_df, display_scale), use_container_width=True, hide_index=True)
        gross = realized_df.loc[realized_df["realized_loss_proxy"].eq("realized_loss_gross_recovery")]
        if not gross.empty:
            row = gross.iloc[0]
            c1, c2, c3 = st.columns(3)
            c1.metric("Baseline Expected Loss", format_currency(row["total_expected_loss_prelim"], display_scale))
            c2.metric("Gross recovery realized proxy", format_currency(row["total_realized_loss_proxy"], display_scale))
            c3.metric("EL / gross proxy ratio", format_rate(row["ratio_expected_to_realized"]))


def render_stress_testing(loans: pd.DataFrame, display_scale: str):
    st.title("Stress Testing")
    st.warning("This is a simple mechanical stress test, not a macroeconomic stress testing model.")

    c1, c2, c3 = st.columns(3)
    with c1:
        pd_multiplier = st.slider("PD multiplier", min_value=0.50, max_value=2.00, value=1.00, step=0.05)
    with c2:
        lgd_multiplier = st.slider("LGD multiplier", min_value=0.50, max_value=1.50, value=1.00, step=0.05)
    with c3:
        ead_multiplier = st.slider("EAD multiplier", min_value=0.75, max_value=1.25, value=1.00, step=0.05)

    baseline_el = loans["expected_loss_prelim"].sum()
    baseline_ead = loans["ead_proxy"].sum()

    stressed_pd = np.minimum(loans["predicted_pd"].to_numpy() * pd_multiplier, 1.0)
    stressed_lgd = np.minimum(loans["lgd_estimate"].to_numpy() * lgd_multiplier, 1.0)
    stressed_ead = loans["ead_proxy"].to_numpy() * ead_multiplier
    stressed_el = stressed_pd * stressed_lgd * stressed_ead
    stressed_total_el = float(stressed_el.sum())
    stressed_total_ead = float(stressed_ead.sum())
    diff = stressed_total_el - baseline_el
    pct_diff = diff / baseline_el if baseline_el else np.nan
    stressed_el_rate = stressed_total_el / stressed_total_ead if stressed_total_ead else np.nan

    row = st.columns(5)
    row[0].metric("Baseline total EL", format_currency(baseline_el, display_scale))
    row[1].metric("Stressed total EL", format_currency(stressed_total_el, display_scale))
    row[2].metric("Difference", format_currency(diff, display_scale))
    row[3].metric("Percent difference", format_percent(pct_diff))
    row[4].metric("Stressed EL rate", format_percent(stressed_el_rate))

    if "grade" in loans.columns:
        st.subheader("Stressed Expected Loss by Grade")
        grade_df = loans[["grade", "ead_proxy"]].copy()
        grade_df["stressed_expected_loss"] = stressed_el
        grade_df["stressed_ead"] = stressed_ead
        grouped = (
            grade_df.groupby("grade", dropna=False)
            .agg(
                loan_count=("grade", "size"),
                stressed_ead=("stressed_ead", "sum"),
                stressed_expected_loss=("stressed_expected_loss", "sum"),
            )
            .reset_index()
        )
        grouped["stressed_expected_loss_rate"] = grouped["stressed_expected_loss"] / grouped["stressed_ead"]
        st.dataframe(to_display_table(grouped, display_scale), use_container_width=True, hide_index=True)
        chart_bar(
            grouped.sort_values("stressed_expected_loss", ascending=False),
            "grade",
            "stressed_expected_loss",
            "Stressed Expected Loss by Grade",
            display_scale,
            y_is_currency=True,
        )


def render_methodology():
    st.title("Methodology and Limitations")

    st.markdown(
        """
### Final Project Framework

- **Dataset:** LendingClub accepted loans.
- **Target:** `Fully Paid = 0`; `Charged Off / Default = 1`; unresolved statuses excluded.
- **PD model:** Uncalibrated L2 Logistic Regression using Feature Set A.
- **PD field:** `predicted_pd`.
- **LGD:** Recovery-based portfolio average from defaulted loans.
- **EAD:** Funded amount.
- **Expected Loss:** `PD x LGD x EAD`.

### Key Limitations

- This dashboard is not production-ready.
- This is not CECL, IFRS 9, Basel, pricing, or underwriting.
- The PD model relies on LendingClub `grade`, `sub_grade`, and `int_rate`.
- Time validation showed underprediction on newer loans.
- LGD is high and simplified.
- EAD is funded amount, not balance at default.
- LGD is constant in the main framework.
- The project uses accepted loans only.
- Realized loss proxy comparisons are reasonableness checks, not independent accounting validation.
"""
    )

    st.subheader("Project Reports")
    for label, path in REPORT_FILES.items():
        if existing_path(path):
            st.success(f"{label}: {path.relative_to(BASE_DIR)}")
        else:
            st.warning(f"Missing optional report: {path.relative_to(BASE_DIR)}")

    final_summary = read_text_cached(str(REPORT_FILES["final_summary"]))
    defense_notes = read_text_cached(str(REPORT_FILES["review_and_defense"]))

    report_tab, defense_tab = st.tabs(["Final Project Summary", "Project Review"])

    with report_tab:
        report_pdf_download(
            "Download final project summary PDF",
            "Final Credit Risk Project Summary",
            FINAL_SUMMARY_MARKDOWN,
            "final_credit_risk_project_summary.pdf",
        )
        st.markdown(FINAL_SUMMARY_MARKDOWN)
        if not final_summary:
            st.info("The source final summary report file was not found, so the dashboard is showing the built-in presentation summary.")

    with defense_tab:
        report_pdf_download(
            "Download project review PDF",
            "Credit Risk Project Review and Defense",
            PROJECT_REVIEW_MARKDOWN,
            "credit_risk_project_review.pdf",
        )
        st.markdown(PROJECT_REVIEW_MARKDOWN)
        if defense_notes:
            with st.expander("Internal detailed review file status"):
                st.write(
                    "A more detailed review and defense report exists in the repository, but this dashboard shows the condensed presentation-facing version."
                )


def main():
    st.sidebar.title("Credit Risk Portfolio Dashboard")
    display_scale = st.sidebar.selectbox("Dollar display", ["Full dollars", "Millions", "Billions"], index=1)

    missing_optional = [name for name, path in DATA_FILES.items() if not existing_path(path)]
    missing_reports = [name for name, path in REPORT_FILES.items() if not existing_path(path)]

    active_core_file = CORE_LOAN_FILE if existing_path(CORE_LOAN_FILE) else DEMO_LOAN_FILE
    using_demo_data = active_core_file == DEMO_LOAN_FILE

    if not existing_path(active_core_file):
        st.error(
            "Required core file is missing. Add either "
            f"{CORE_LOAN_FILE.relative_to(BASE_DIR)} or {DEMO_LOAN_FILE.relative_to(BASE_DIR)}."
        )
        st.stop()

    loans = read_csv_cached(str(active_core_file), tuple(CORE_LOAN_COLUMNS))
    missing_core_cols = validate_required_columns(loans, CORE_REQUIRED_COLUMNS, "loans_with_pd_lgd_ead_v1.csv")
    if missing_core_cols:
        st.error(
            "The core loan-level file is missing required columns: "
            + ", ".join(missing_core_cols)
            + ". The dashboard cannot calculate portfolio risk without these fields."
        )
        st.stop()

    loans = ensure_issue_year(loans)
    filtered_loans = apply_sidebar_filters(loans)

    st.sidebar.markdown("### Project Navigation")
    page = st.sidebar.radio(
        "Go to",
        [
            "Overview",
            "Segment Analysis",
            "PD Deciles",
            "Expected Loss Concentration",
            "LGD Sensitivity",
            "Stress Testing",
            "Methodology and Limitations",
        ],
    )

    if missing_optional:
        st.sidebar.warning("Optional data files missing: " + ", ".join(missing_optional))
    if missing_reports:
        st.sidebar.warning("Optional report files missing: " + ", ".join(missing_reports))

    st.sidebar.markdown("### Scope")
    if using_demo_data:
        st.sidebar.warning("Using demo loan-level sample. Add the full processed core file for complete loan-level dashboard metrics.")
    st.sidebar.write(f"Selected loans: {len(filtered_loans):,} of {len(loans):,}")
    st.sidebar.caption("This app explores existing outputs. It does not retrain models or approve loans.")

    if filtered_loans.empty:
        st.error("No loans match the selected filters. Clear one or more filters to continue.")
        st.stop()

    if page == "Overview":
        render_overview(filtered_loans, display_scale)
    elif page == "Segment Analysis":
        render_segment_analysis(display_scale)
    elif page == "PD Deciles":
        render_pd_deciles(display_scale)
    elif page == "Expected Loss Concentration":
        render_concentration(filtered_loans, display_scale)
    elif page == "LGD Sensitivity":
        render_lgd_sensitivity(display_scale)
    elif page == "Stress Testing":
        render_stress_testing(filtered_loans, display_scale)
    else:
        render_methodology()


if __name__ == "__main__":
    main()
