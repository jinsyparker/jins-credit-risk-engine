# Milestone 1 Summary: LendingClub Credit Risk Project

## Objective

The objective of Milestone 1 was to set up a clean foundation for a LendingClub credit risk modeling project. The first model will be a Probability of Default model, so this milestone focused on understanding the raw data, defining a clear binary target, creating a first cleaned modeling dataset, identifying potential data leakage, and performing early exploratory analysis on key risk drivers.

No model training was completed in this milestone. The goal was to prepare the data carefully so that future modeling work is based on a transparent and reproducible dataset.

## Data Used

The project uses LendingClub loan data stored in:

```text
data/raw/raw_data.csv
```

The raw dataset includes borrower information, loan characteristics, credit attributes, payment fields, hardship fields, settlement fields, and loan outcome information. Because the dataset contains both origination-time fields and post-origination performance fields, special care is needed to prevent data leakage in the Probability of Default model.

## Target Variable Definition

The target variable for the first model version is `default_flag`, created from `loan_status`.

The mapping used is:

| loan_status | default_flag |
|---|---:|
| Fully Paid | 0 |
| Charged Off | 1 |
| Default | 1 |

All other `loan_status` values were excluded from the first version of the modeling dataset. This keeps the target definition simple and limits the model sample to loans with clear outcomes.

This decision is important because a Probability of Default model needs a reliable target. Including unresolved or ambiguous statuses could make the model harder to interpret and could weaken the connection between the target and true default behavior.

## Cleaning Steps

The main cleaning work was completed in `notebooks/02_data_cleaning.ipynb`.

The key steps were:

1. Loaded the raw LendingClub dataset from `data/raw/raw_data.csv`.
2. Created the binary `default_flag` target from `loan_status`.
3. Filtered the dataset to keep only loans with clear target values.
4. Converted selected text-formatted columns into numeric fields:
   - `int_rate`: removed `%` and converted to float.
   - `revol_util`: removed `%` and converted to float.
   - `term`: extracted the number of months and converted to integer.
   - `emp_length`: converted values such as `10+ years`, `< 1 year`, and `3 years` into numeric years.
5. Created `loans_clean`, the first clean modeling dataset.
6. Saved the cleaned dataset to:

```text
data/processed/loans_clean_v1.csv
```

These cleaning steps make the dataset easier to use for both EDA and future model development.

## Leakage Notes

Data leakage is a major risk in credit risk modeling. A Probability of Default model should only use information that would be available before or at the time of the lending decision. Variables that describe payment behavior, recoveries, hardship events, or settlement outcomes can reveal what happened after the loan was issued.

The following leakage columns were identified and excluded from the first PD candidate feature list:

```python
recoveries
collection_recovery_fee
last_pymnt_d
last_pymnt_amnt
total_pymnt
total_rec_prncp
total_rec_int
settlement_status
hardship_flag
debt_settlement_flag
```

The target variable `default_flag` was also excluded from the candidate feature list. This prevents the model from accidentally using the answer as an input.

The first candidate feature list is stored in the notebook as `pd_model_candidate_columns`. Additional leakage review will still be needed before final model training, because LendingClub data contains many fields that may not be available at origination.

## Key EDA Findings

Exploratory analysis was completed in `notebooks/03_eda.ipynb`. The notebook created default-rate summary tables and bar charts for:

- `grade`
- `sub_grade`
- `term`
- `purpose`
- `home_ownership`

Each summary table includes:

- number of loans
- number of defaults
- default rate

The main findings from this EDA stage are:

- `grade` and `sub_grade` are important risk indicators because they show default-rate differences across LendingClub credit quality groups.
- `term` is a useful loan-structure variable because loan duration may be related to borrower risk and repayment uncertainty.
- `purpose` may capture differences in borrower intent or financial need, but rare categories may need to be grouped later.
- `home_ownership` may provide borrower stability information, but small categories should be handled carefully.
- Summary tables should be interpreted with both default rate and loan count in mind. A high default rate based on a small number of loans may not be stable.

These EDA results are not final modeling conclusions. They are early evidence to guide feature selection and deeper analysis in the next milestone.

## Outputs Created

The following notebooks were created or updated:

```text
notebooks/01_data_understanding.ipynb
notebooks/02_data_cleaning.ipynb
notebooks/03_eda.ipynb
```

The following processed dataset was created:

```text
data/processed/loans_clean_v1.csv
```

The following tables were created:

```text
reports/tables/missing_values_v1.csv
reports/tables/default_rate_by_grade.csv
reports/tables/default_rate_by_sub_grade.csv
reports/tables/default_rate_by_term.csv
reports/tables/default_rate_by_purpose.csv
reports/tables/default_rate_by_home_ownership.csv
```

The following figures were created:

```text
reports/figures/default_rate_by_grade.png
reports/figures/default_rate_by_sub_grade.png
reports/figures/default_rate_by_term.png
reports/figures/default_rate_by_purpose.png
reports/figures/default_rate_by_home_ownership.png
```

## Decisions Made

The main Milestone 1 decisions were:

1. Use `raw_data.csv` as the raw LendingClub source file.
2. Define the first target variable as `default_flag`.
3. Use only `Fully Paid`, `Charged Off`, and `Default` loans for the first model version.
4. Exclude unresolved or ambiguous loan statuses from version 1.
5. Clean key numeric fields before EDA and modeling.
6. Save a stable cleaned dataset as `loans_clean_v1.csv`.
7. Exclude obvious leakage variables from the first PD candidate feature list.
8. Use default-rate summaries to identify early candidate risk drivers.

## Next Milestone

The next milestone should focus on preparing the first modeling dataset and training a baseline Probability of Default model.

Recommended next steps:

1. Review `pd_model_candidate_columns` for additional leakage or unavailable-at-origination fields.
2. Select a small beginner-friendly feature set.
3. Handle missing values for selected features.
4. Encode categorical variables.
5. Split the data into training and test sets.
6. Train a baseline model, such as logistic regression.
7. Evaluate the model using metrics such as ROC AUC, confusion matrix, recall, precision, and default-rate separation.
8. Document model performance and limitations.

Milestone 1 created the data foundation. Milestone 2 should turn that foundation into the first working Probability of Default model.
