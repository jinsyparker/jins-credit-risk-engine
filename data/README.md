# Data

This repository does not commit the full raw or full loan-level generated LendingClub datasets because several files exceed GitHub's normal file-size limits.

## Raw Source Data

The original source is LendingClub accepted-loan data. A local copy, when available, should be stored outside Git or at:

```text
data/raw/raw_data.csv
```

The original LendingClub dataset is not committed to the repository. Generated summary files should not be treated as raw input data.

## Generated Analytical Artifacts

The full modeling workflow generated cleaned loan-level datasets, PD scores, LGD/EAD fields, Expected Loss outputs, summary tables, model metadata, and figures. The largest loan-level files are excluded from Git.

## Demo and Committed Files

The public repository includes selected processed outputs and summary artifacts required for the public analysis notebooks and Streamlit application:

- summary tables used by the README, technical report, tests, notebooks, and dashboard;
- generated figures;
- model metadata and coefficient exports;
- a 100,000-row demo sample for Streamlit deployment.

The demo sample is:

```text
data/demo/loans_with_pd_lgd_ead_sample_v1.csv
```

## Excluded Large Generated Files

The following files are generated locally and intentionally excluded from Git:

| file | approximate size | purpose |
| --- | ---: | --- |
| `data/raw/raw_data.csv` | 1.6 GB | raw LendingClub accepted-loan source data |
| `data/processed/loans_clean_v1.csv` | 925 MB | full cleaned modeling dataset |
| `data/processed/loans_with_pd_v1.csv` | 953 MB | full scored PD dataset |
| `data/processed/loans_with_pd_lgd_ead_v1.csv` | 1.0 GB | full loan-level PD/LGD/EAD/EL dataset |
| `data/processed/lgd_ead_dataset_v1.csv` | 158 MB | full LGD/EAD preparation dataset |
| `data/processed/lgd_sensitivity_defaulted_loans_v1.csv` | 111 MB | defaulted-loan sensitivity dataset |

## Analysis Notebooks

The four public notebooks provide a cleaned, executable walkthrough of the project's main analytical stages and consume selected intermediate/result artifacts generated during the full modeling workflow. They are designed for transparency and review rather than as a raw-data-to-final-output production pipeline.

Run the cleaned notebooks in order:

```text
notebooks/01_data_and_target.ipynb
notebooks/02_pd_modeling_and_validation.ipynb
notebooks/03_lgd_ead_expected_loss.ipynb
notebooks/04_portfolio_risk_and_scenarios.ipynb
```

The Streamlit app automatically uses the full processed loan-level file if available. Otherwise, it falls back to the included demo sample.
