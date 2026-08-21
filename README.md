# Jin's Credit Risk Engine

An end-to-end credit risk analytics project using LendingClub accepted-loan data. The project builds a Probability of Default model, prepares LGD and EAD proxies, calculates preliminary Expected Loss, decomposes portfolio risk, tests LGD sensitivity, and presents the results in a Streamlit dashboard.

This is a portfolio and academic-style credit risk project. It is not a production underwriting, pricing, CECL, IFRS 9, Basel, reserve, or capital model.

## Project Highlights

| area | output |
| --- | --- |
| Dataset | LendingClub accepted loans with resolved outcomes |
| Target | `Fully Paid = 0`; `Charged Off / Default = 1` |
| PD model | Uncalibrated L2 Logistic Regression |
| LGD | Recovery-based portfolio-average LGD |
| EAD | Funded amount proxy |
| Expected Loss | `PD x LGD x EAD` |
| Dashboard | Streamlit portfolio risk dashboard |

## Headline Results

| metric | value |
| --- | ---: |
| Loans | 1,345,350 |
| Defaulted loans | 268,599 |
| Observed default rate | 19.96% |
| Final PD ROC-AUC | 0.7084 |
| Final PD PR-AUC | 0.3689 |
| Portfolio-average LGD | 0.9247 |
| Total EAD | $19.39B |
| Total preliminary Expected Loss | $3.86B |
| Expected Loss rate | 19.92% |
| Highest PD decile EL share | 28.31% |
| Top 10% loan-level EL share | 34.15% |

## Repository Structure

```text
.
├── app/                 # Streamlit dashboard
├── data/
│   ├── demo/            # Small dashboard sample committed for deployment
│   ├── processed/       # Small committed summaries; large generated files ignored
│   └── raw/             # Raw source file placeholder only
├── docs/                # Data, deployment, and project documentation
├── models/              # Saved PD model artifacts
├── notebooks/           # Milestone notebooks
├── reports/
│   ├── figures/         # Generated charts
│   └── tables/          # Generated metric tables
└── requirements.txt
```

## Run The Dashboard

Install the dashboard dependencies:

```bash
python3 -m pip install -r app/requirements_streamlit.txt
```

Run locally:

```bash
python3 -m streamlit run app/streamlit_app.py
```

The dashboard uses the full loan-level file when available:

```text
data/processed/loans_with_pd_lgd_ead_v1.csv
```

If the full file is not available, it falls back to the included demo sample:

```text
data/demo/loans_with_pd_lgd_ead_sample_v1.csv
```

## Reproduce The Analysis

Place the LendingClub raw accepted-loan CSV at:

```text
data/raw/raw_data.csv
```

Then run the notebooks in order from `notebooks/01_data_understanding.ipynb` through `notebooks/10_lgd_sensitivity_and_realized_loss.ipynb`.

See [docs/DATA.md](docs/DATA.md) for data-size notes and excluded generated files.

## Deployment

The app can be deployed on Streamlit Community Cloud using:

```text
app/streamlit_app.py
```

See [docs/DEPLOY_STREAMLIT.md](docs/DEPLOY_STREAMLIT.md).

## Important Limitations

- The final PD model uses LendingClub `grade`, `sub_grade`, and `int_rate`, which embed platform underwriting and pricing information.
- The borrower-only model has weaker but still meaningful signal.
- Time validation shows underprediction on newer loans.
- LGD is a constant portfolio average in the main Expected Loss framework.
- EAD is funded amount, not actual balance at default.
- Realized-loss proxy checks are not independent accounting validation.
- This is a project-ready analytical framework, not a production credit risk system.

## Key Reports

- [Final project summary](reports/final_credit_risk_project_summary.md)
- [Project review and defense notes](reports/final_credit_risk_project_review_and_defense.md)
- [Concise project summary](docs/PROJECT_SUMMARY.md)
