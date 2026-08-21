# Milestone 2 Summary: Baseline Probability of Default Model

## Objective

The objective of Milestone 2 was to build the first baseline Probability of Default model for the LendingClub credit risk project. The purpose of this milestone was not to create the most powerful model possible, but to establish a clear, reproducible modeling workflow using logistic regression.

This baseline model provides a benchmark that future models can be compared against. It also confirms that the project can move from a cleaned dataset to model training, probability prediction, model evaluation, risk ranking, and saved outputs.

## Dataset Used

The model uses the cleaned dataset created in Milestone 1:

```text
data/processed/loans_clean_v1.csv
```

This dataset includes the binary default target, cleaned numeric fields, and the filtered modeling population. The model does not train directly on the raw LendingClub file.

## Target Variable

The target variable is:

```text
default_flag
```

The target was defined in Milestone 1 as:

| loan_status | default_flag |
|---|---:|
| Fully Paid | 0 |
| Charged Off | 1 |
| Default | 1 |

Rows with missing `default_flag` are dropped before modeling. This keeps the first model focused on loans with clear observed outcomes.

## Features Used

The baseline model uses a small, beginner-friendly set of numeric and categorical variables.

Numeric features:

- `loan_amnt`
- `term`
- `int_rate`
- `annual_inc`
- `dti`
- `delinq_2yrs`
- `revol_util`
- `total_acc`
- `open_acc`
- `emp_length`

Categorical features:

- `grade`
- `sub_grade`
- `home_ownership`
- `verification_status`
- `purpose`
- `addr_state`

The notebook includes a leakage check to make sure the model does not use `loan_status`, payment fields, recovery fields, hardship fields, settlement fields, or other post-outcome variables.

## Preprocessing Steps

The model uses a scikit-learn preprocessing pipeline.

For numeric variables:

- missing values are filled using median imputation
- variables are standardized using `StandardScaler`

For categorical variables:

- missing values are filled using the most frequent category
- categories are converted into model-ready columns using one-hot encoding
- unknown categories are ignored during transformation so the pipeline can handle new categories more safely

The preprocessing steps are included inside the modeling pipeline. This is important because the imputers, scaler, and encoder are fit only on the training data, which helps avoid preprocessing leakage from the test set.

## Model Used

The baseline model is logistic regression:

```text
LogisticRegression
```

Logistic regression is a good first model for credit risk because it is transparent, widely used, and produces predicted probabilities. In this project, those probabilities represent estimated Probability of Default values.

The trained pipeline is saved as:

```text
models/pd_logistic_regression_v1.pkl
```

## Evaluation Metrics

The model is evaluated on a held-out test set created with `train_test_split` and `stratify=y`. Stratification helps keep the default rate similar between the training and test samples.

The following metrics are calculated:

- ROC-AUC
- Average Precision / PR-AUC
- Brier Score
- Accuracy at a 0.5 threshold
- Precision at a 0.5 threshold
- Recall at a 0.5 threshold

The metrics are saved to:

```text
reports/tables/pd_model_metrics_v1.csv
```

ROC-AUC measures how well the model ranks loans from lower risk to higher risk. Average Precision is useful because default is usually the minority class. Brier Score measures the quality of the predicted probabilities. Accuracy, precision, and recall at 0.5 provide a simple classification view, but they should not be the only basis for judging a credit risk model.

## Risk Decile Analysis

The notebook creates 10 risk deciles using predicted default probabilities on the test set. Decile 1 represents the lowest predicted risk group, and decile 10 represents the highest predicted risk group.

For each decile, the table reports:

- number of loans
- average predicted Probability of Default
- actual default rate
- number of actual defaults
- minimum predicted Probability of Default
- maximum predicted Probability of Default

The decile table is saved to:

```text
reports/tables/pd_risk_deciles_v1.csv
```

The decile chart is saved to:

```text
reports/figures/default_rate_by_decile_v1.png
```

The key question in the decile analysis is whether actual default rates generally increase from low-risk deciles to high-risk deciles. If they do, the model is separating risk in a useful way. Small reversals can occur because of sample variation, but the overall pattern should trend upward.

## Calibration Analysis

The notebook also creates a calibration curve:

```text
reports/figures/pd_model_calibration_curve_v1.png
```

Calibration compares predicted default probabilities with actual observed default rates. A well-calibrated model should produce predicted probabilities that are close to observed outcomes across risk bands.

For a credit risk model, calibration matters because the output is not just a class label. The predicted probability may be used for risk ranking, cutoff analysis, pricing, portfolio monitoring, and capital planning. A model can rank loans well but still produce probabilities that are too high or too low, so calibration should be reviewed separately from ROC-AUC.

## Key Limitations

This is a baseline model, so it has several important limitations:

1. The feature set is intentionally simple and may not capture all useful credit risk information.
2. Logistic regression assumes a relatively simple relationship between features and default risk.
3. No advanced feature engineering has been performed yet.
4. Categorical variables may contain rare categories that could be grouped in future versions.
5. The model has not yet been tuned.
6. The 0.5 classification threshold may not be appropriate for credit risk decisions.
7. Additional leakage review is still needed before treating the feature set as final.
8. Model fairness, stability, and out-of-time validation have not been assessed yet.

These limitations are acceptable for Milestone 2 because the goal is to create a first working benchmark, not a final model.

## Outputs Created

Milestone 2 created or uses the following main artifacts:

```text
notebooks/04_baseline_pd_model.ipynb
models/pd_logistic_regression_v1.pkl
reports/tables/pd_model_metrics_v1.csv
reports/tables/pd_risk_deciles_v1.csv
reports/figures/pd_model_roc_curve_v1.png
reports/figures/pd_model_precision_recall_curve_v1.png
reports/figures/pd_model_calibration_curve_v1.png
reports/figures/default_rate_by_decile_v1.png
```

## Next Milestone

The next milestone should focus on improving and validating the baseline model.

Recommended next steps:

1. Review model metrics and decide which evaluation metric matters most for the project goal.
2. Inspect the risk decile table to confirm whether observed default rates increase across deciles.
3. Review the calibration curve and decide whether calibration improvement is needed.
4. Perform deeper feature selection and remove any remaining leakage or unavailable-at-origination fields.
5. Add more feature engineering, such as grouped categories, missingness indicators, and transformed financial ratios.
6. Compare logistic regression with another simple model only after the baseline is fully understood.
7. Consider threshold analysis for lending decision cutoffs.
8. Add stronger validation, such as out-of-time testing if issue dates are used.

Milestone 2 establishes the first working Probability of Default model. The next milestone should focus on understanding model behavior, improving feature quality, and validating whether the model is reliable enough for credit risk analysis.
