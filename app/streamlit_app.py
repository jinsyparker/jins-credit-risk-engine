from __future__ import annotations

import streamlit as st

from utils.data_loader import load_loans, portfolio_metrics
from utils.formatting import compact_count, format_currency, format_percent


st.set_page_config(
    page_title="Credit Risk Modeling and Expected Loss Engine",
    layout="wide",
)


def main() -> None:
    loans, using_demo_data = load_loans()
    metrics = portfolio_metrics(loans)

    st.title("Credit Risk Modeling and Expected Loss Engine")
    st.caption("PD validation, LGD/EAD estimation, portfolio expected-loss analysis, and deterministic scenario testing.")

    if using_demo_data:
        st.warning(
            "This hosted dashboard is using a 100,000-row demo sample. "
            "Use the full processed loan-level file locally for complete portfolio metrics."
        )

    st.markdown(
        """
This project evaluates whether an interpretable probability-of-default model remains useful when strong predictors partially embed LendingClub's own underwriting and pricing signal. The selected PD model is then connected to LGD and EAD assumptions to analyze baseline Expected Loss and portfolio concentration.
        """
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Loans", compact_count(metrics["loan_count"]))
    c2.metric("Total EAD", format_currency(metrics["total_ead"], "Billions"))
    c3.metric("Mean predicted PD", format_percent(metrics["mean_predicted_pd"]))
    c4.metric("Baseline EL rate", format_percent(metrics["expected_loss_rate"]))

    c5, c6, c7 = st.columns(3)
    c5.metric("Portfolio LGD", format_percent(metrics["portfolio_lgd"]))
    c6.metric("Baseline Expected Loss", format_currency(metrics["total_expected_loss"], "Billions"))
    c7.metric("Observed default rate", format_percent(metrics["observed_default_rate"]))

    st.markdown(
        """
### Dashboard Sections

- **Portfolio Overview:** portfolio metrics, PD distribution, and baseline Expected Loss distribution.
- **PD Validation:** model comparison, borrower-only ablation, calibration, decile separation, and Out-of-Time validation.
- **Expected Loss:** segment decomposition, concentration, PD x EAD drivers, and LGD sensitivity.
- **Scenario Analysis:** deterministic PD/LGD/EAD shocks applied to baseline Expected Loss.

The dashboard is an analytical presentation layer over saved project outputs. It does not approve loans or retrain models.
        """
    )


if __name__ == "__main__":
    main()
