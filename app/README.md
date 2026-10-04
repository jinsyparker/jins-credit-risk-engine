# Streamlit Dashboard

This dashboard presents the Credit Risk Modeling and Expected Loss Engine as an interactive research artifact.

## Run Locally

From the project root:

```bash
python3 -m pip install -r requirements.txt
python3 -m streamlit run app/streamlit_app.py
```

## Dashboard Sections

- **Portfolio Overview:** portfolio-level exposure, PD, LGD, and baseline Expected Loss metrics.
- **PD Validation:** model comparison, embedded underwriting signal ablation, calibration, PD decile separation, and out-of-time validation.
- **Expected Loss:** segment-level risk decomposition, concentration, PD x EAD drivers, LGD sensitivity, and reasonableness checks.
- **Scenario Analysis:** deterministic PD/LGD/EAD shocks applied to baseline Expected Loss.

## Data Behavior

For full local analysis, the app uses:

```text
data/processed/loans_with_pd_lgd_ead_v1.csv
```

For GitHub and Streamlit Community Cloud deployment, the app can also run from:

```text
data/demo/loans_with_pd_lgd_ead_sample_v1.csv
```

The demo sample is used automatically when the full processed loan-level file is absent.

## Scope

The dashboard visualizes saved analytical outputs. It does not retrain models, approve loans, or implement a regulatory capital/accounting framework.
