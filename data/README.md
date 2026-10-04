# Data

This repository does not commit the full raw or full loan-level generated LendingClub datasets because several files exceed GitHub's normal file-size limits.

## Included

The public repository includes:

- small summary tables used by the README, technical report, tests, and dashboard;
- generated figures;
- model metadata and coefficient exports;
- a 100,000-row demo sample for Streamlit deployment.

The demo sample is:

```text
data/demo/loans_with_pd_lgd_ead_sample_v1.csv
```

## Excluded Large Files

The following files are generated locally and intentionally excluded from Git:

| file | approximate size | purpose |
| --- | ---: | --- |
| `data/raw/raw_data.csv` | 1.6 GB | raw LendingClub accepted-loan data |
| `data/processed/loans_clean_v1.csv` | 925 MB | full cleaned modeling dataset |
| `data/processed/loans_with_pd_v1.csv` | 953 MB | full scored PD dataset |
| `data/processed/loans_with_pd_lgd_ead_v1.csv` | 1.0 GB | full loan-level PD/LGD/EAD/EL dataset |
| `data/processed/lgd_ead_dataset_v1.csv` | 158 MB | full LGD/EAD preparation dataset |
| `data/processed/lgd_sensitivity_defaulted_loans_v1.csv` | 111 MB | defaulted-loan sensitivity dataset |

## Reproduction

Place the LendingClub accepted-loan source file at:

```text
data/raw/raw_data.csv
```

Then run the cleaned notebooks in order:

```text
notebooks/01_data_and_target.ipynb
notebooks/02_pd_modeling_and_validation.ipynb
notebooks/03_lgd_ead_expected_loss.ipynb
notebooks/04_portfolio_risk_and_scenarios.ipynb
```

The Streamlit app automatically uses the full processed loan-level file if available. Otherwise, it falls back to the included demo sample.
