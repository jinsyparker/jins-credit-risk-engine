# Data Guide

This repository intentionally does not commit the full raw and loan-level LendingClub data files because several files exceed GitHub's normal file-size limits.

## Included Data

The GitHub version includes small portfolio summary outputs needed for review and dashboard pages:

- Expected Loss segment summaries by grade, sub-grade, term, purpose, issue year, and PD decile.
- Expected Loss concentration and PD x EAD driver matrix.
- LGD sensitivity summaries.
- Realized-loss proxy summaries.
- A small demo loan-level sample for the Streamlit app.

## Excluded Large Files

These files are generated locally and are excluded from Git:

| file | approximate size | reason |
| --- | ---: | --- |
| `data/raw/raw_data.csv` | 1.6 GB | raw source data |
| `data/processed/loans_clean_v1.csv` | 925 MB | full cleaned loan-level dataset |
| `data/processed/loans_with_pd_v1.csv` | 953 MB | full scored PD dataset |
| `data/processed/loans_with_pd_lgd_ead_v1.csv` | 1.0 GB | full loan-level PD/LGD/EAD/EL dataset |
| `data/processed/lgd_ead_dataset_v1.csv` | 158 MB | full LGD/EAD preparation dataset |
| `data/processed/lgd_sensitivity_defaulted_loans_v1.csv` | 111 MB | full defaulted-loan sensitivity dataset |

## Reproducing The Full Outputs

Place the raw LendingClub accepted-loan CSV at:

```text
data/raw/raw_data.csv
```

Then run the notebooks in order:

```text
01_data_understanding.ipynb
02_data_cleaning.ipynb
03_eda.ipynb
04_baseline_pd_model.ipynb
05_pd_model_validation_and_improvement.ipynb
06_pd_model_family_comparison.ipynb
07_pd_calibration_and_final_selection.ipynb
08_lgd_ead_preparation.ipynb
09_expected_loss_analysis.ipynb
10_lgd_sensitivity_and_realized_loss.ipynb
```

The full Streamlit dashboard will use `data/processed/loans_with_pd_lgd_ead_v1.csv` when present. If that file is not present, it falls back to `data/demo/loans_with_pd_lgd_ead_sample_v1.csv`.
