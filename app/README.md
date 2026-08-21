# Credit Risk Portfolio Dashboard

This Streamlit app is an interactive presentation layer over the completed Credit Risk Project outputs. It does not retrain models, score new borrower applications, or make loan approval decisions.

The app is intended for portfolio review, project presentation, and exploratory analysis of the final PD/LGD/EAD/Expected Loss framework.

## How to Run

From the project root:

```bash
python3 -m streamlit run app/streamlit_app.py
```

If Streamlit or Plotly is not installed, install the dashboard requirements first:

```bash
python3 -m pip install -r app/requirements_streamlit.txt
python3 -m streamlit run app/streamlit_app.py
```

If you prefer an isolated environment, use a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r app/requirements_streamlit.txt
python -m streamlit run app/streamlit_app.py
```

## Required Data Files

For full local analysis, the app expects this loan-level project output:

- `data/processed/loans_with_pd_lgd_ead_v1.csv`

For GitHub and Streamlit Community Cloud deployment, the app can also run from the committed demo sample:

- `data/demo/loans_with_pd_lgd_ead_sample_v1.csv`

The demo sample is used automatically when the full processed loan-level file is absent.

The app also uses these small project summary outputs:

- `data/processed/expected_loss_by_grade_v1.csv`
- `data/processed/expected_loss_by_sub_grade_v1.csv`
- `data/processed/expected_loss_by_term_v1.csv`
- `data/processed/expected_loss_by_purpose_v1.csv`
- `data/processed/expected_loss_by_issue_year_v1.csv`
- `data/processed/expected_loss_by_pd_decile_v1.csv`
- `data/processed/expected_loss_top_concentration_v1.csv`
- `data/processed/expected_loss_pd_ead_matrix_v1.csv`
- `data/processed/lgd_sensitivity_summary_v1.csv`
- `data/processed/expected_loss_lgd_sensitivity_summary_v1.csv`
- `data/processed/realized_vs_expected_loss_summary_v1.csv`

The methodology page also references:

- `reports/final_credit_risk_project_summary.md`
- `reports/final_credit_risk_project_review_and_defense.md`

## Pages

- **Overview:** Portfolio KPIs, PD distribution, Expected Loss distribution, and EAD versus EL summary.
- **Segment Analysis:** Expected Loss by grade, sub-grade, term, purpose, or issue year.
- **PD Deciles:** PD ranking, realized default rate, EL rate, and EL share by decile.
- **Expected Loss Concentration:** Top 1%, 5%, 10%, and 20% concentration views, a loan-level cumulative EL curve, and the PD x EAD driver matrix.
- **LGD Sensitivity:** Alternative LGD definitions, Expected Loss scenarios, and realized loss proxy comparison.
- **Stress Testing:** Simple mechanical PD/LGD/EAD multiplier stress test.
- **Methodology and Limitations:** Final framework choice, caveats, and project report references.

The Methodology page includes PDF downloads for the final project summary and the presentation-facing project review.

## Limitations

- This is a project dashboard, not a production underwriting tool.
- It is not a CECL, IFRS 9, Basel, pricing, or capital model.
- The app uses persisted project outputs and does not retrain models.
- The PD model relies on LendingClub `grade`, `sub_grade`, and `int_rate`.
- Time validation showed underprediction on newer loans.
- EAD is funded amount, not balance at default.
- LGD is a recovery-based portfolio average and is constant in the main framework.
- Stress testing is mechanical and not a macroeconomic scenario model.
