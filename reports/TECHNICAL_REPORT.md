# Technical Report

## 1. Problem Definition

This project evaluates probability-of-default modeling for LendingClub accepted loans and translates the selected PD estimates into a portfolio expected-loss framework. The central modeling question is whether an interpretable model remains robust when the strongest available predictors partially embed the lender's own underwriting and pricing signal.

The project therefore emphasizes validation and modeling judgment rather than model complexity. The analysis compares borrower-only and platform-informed feature sets, evaluates linear and nonlinear model families, distinguishes discrimination from calibration, and tests temporal robustness through Out-of-Time (OOT) validation.

## 2. Data

The analysis uses LendingClub accepted-loan data with resolved loan outcomes. The cleaned modeling sample contains `1,345,350` loans, including `268,599` defaulted loans and `1,076,751` non-defaulted loans. The observed default rate is `19.96%`.

Large raw and full loan-level generated files are excluded from the public repository because they exceed GitHub's normal file-size limits. The repository includes summary tables, figures, model metadata, and a small dashboard demo sample.

The public notebooks are executable analysis notebooks. They consume selected committed analytical artifacts from the full modeling workflow and are intended to make the modeling decisions and results transparent; they are not presented as a raw-data-to-final-output production pipeline.

## 3. Target Definition

The binary default target is defined from final loan status:

| Loan Status | Target |
| --- | ---: |
| Fully Paid | 0 |
| Charged Off | 1 |
| Default | 1 |

Unresolved statuses are excluded from the modeling sample so that the target represents resolved performance outcomes.

## 4. Feature Engineering

The model uses borrower, loan, and application attributes available in the cleaned LendingClub dataset. Numeric fields include loan amount, term, interest rate, annual income, debt-to-income ratio, delinquency count, revolving utilization, total accounts, open accounts, and employment length. Categorical fields include grade, sub-grade, home ownership, verification status, purpose, and borrower state.

Post-origination payment, recovery, hardship, settlement, and outcome fields are excluded from the PD feature set.

## 5. Embedded Underwriting Signal Ablation

The project treats LendingClub `grade`, `sub_grade`, and `int_rate` as a methodological issue rather than simply a caveat. These variables are known at origination, but they also embed LendingClub's own credit assessment and pricing.

Two feature specifications are therefore compared:

| Specification | Description |
| --- | --- |
| Platform-informed | Includes borrower variables plus LendingClub grade, sub-grade, and interest rate |
| Borrower-only | Excludes LendingClub grade, sub-grade, and interest rate |

Removing platform-generated underwriting variables reduced ROC-AUC from `0.7094` to `0.6747`, and reduced Average Precision (AP) from `0.3701` to `0.3388`. Borrower information retained meaningful predictive value, while platform-generated risk and pricing features added substantial incremental discrimination.

## 6. PD Model Development

The project compares logistic regression, L2-regularized logistic regression, gradient boosting, and random forest models. Model comparison is based on ROC-AUC, Average Precision (AP), Brier score, calibration, decile separation, temporal validation, and interpretability. AP is computed using `sklearn.metrics.average_precision_score`.

| Model / Feature Set | ROC-AUC | Average Precision (AP) | Brier Score | Interpretation |
| --- | ---: | ---: | ---: | --- |
| Platform-informed logistic regression | 0.7094 | 0.3701 | 0.1453 | Strongest baseline specification |
| Borrower-only logistic regression | 0.6747 | 0.3388 | 0.1495 | Borrower/loan signal without platform grades/pricing |
| L2 logistic regression | 0.7093 | 0.3701 | 0.1453 | Similar performance with regularization |
| Gradient boosting | 0.7068 | 0.3700 | 0.1456 | No material nonlinear improvement |
| Random forest | 0.7050 | 0.3676 | 0.1463 | No material improvement over logistic alternatives |

## 7. Model Selection

The selected PD model is an uncalibrated L2 logistic regression using the platform-informed feature specification. It was retained because nonlinear alternatives did not materially improve predictive discrimination, while logistic regression preserved interpretability, stability, and a clear path to coefficient-level interpretation.

The final random-holdout metrics are:

| Metric | Value |
| --- | ---: |
| ROC-AUC | 0.7084 |
| 95% bootstrap ROC-AUC interval | [0.7063, 0.7108] |
| Average Precision (AP) | 0.3689 |
| Brier Score | 0.1455 |
| Log Loss | 0.4553 |
| Gini | 0.4169 |
| KS Statistic | 0.3027 |
| High/low decile default-rate ratio | 10.6081 |

The ROC-AUC interval is a 95% percentile bootstrap interval using 500 replacement resamples, a fixed random seed, and skipped bootstrap samples that contain only one target class. The KS statistic ranks loans from highest to lowest PD and measures the maximum separation between cumulative default and non-default distributions.

## 8. Probability Calibration

Calibration methods compared include uncalibrated probabilities, sigmoid calibration, and isotonic calibration. Calibration did not materially improve probability quality on the random holdout sample. Isotonic calibration slightly improved Brier score and log loss, but reduced Average Precision (AP) and introduced more flexibility without addressing the larger temporal calibration issue.

The uncalibrated L2 model had mean predicted PD of `19.97%` versus observed default rate of `19.97%` on the random holdout sample.

## 9. Out-of-Time Validation Design

Out-of-time validation is the principal model-risk finding.

For the final temporal test, loans are segmented by origination date using an OOT cutoff of `2016-10-01`. Loans originated before `2016-10-01` form the pre-cutoff development sample. Loans originated on or after `2016-10-01` form the OOT evaluation sample. The date-based split is applied after excluding unresolved loan-status outcomes.

The pre-cutoff development sample contains `1,062,380` rows and is further split into `796,785` time-training rows and `265,595` time-calibration rows for calibration testing. The OOT set contains `282,970` rows with observed default rate of `21.82%`. This cutoff creates a large post-cutoff OOT cohort while retaining a substantial historical development sample.

The random-holdout metrics below are separate from the date-based OOT design and come from a random split of the resolved modeling sample.

| Metric | Random Holdout | Out-of-Time |
| --- | ---: | ---: |
| ROC-AUC | 0.7084 | 0.6953 |
| Average Precision (AP) | 0.3689 | 0.3681 |
| Brier Score | 0.1455 | 0.1579 |
| Log Loss | 0.4553 | 0.4875 |
| Gini | 0.4169 | 0.3906 |
| Mean Predicted PD | 19.97% | 19.37% |
| Observed Default Rate | 19.97% | 21.82% |

The ranking performance declines but does not collapse. The larger concern is temporal calibration: the model underestimates the default rate in the OOT cohort.

## 10. Model Interpretation

The logistic model supports coefficient-level interpretation, but the final platform-informed specification includes correlated underwriting variables such as grade, sub-grade, and interest rate. Coefficients should be read as conditional regularized associations with estimated default probability, not causal effects.

| Feature | Coefficient | Exp(Coefficient) | Association |
| --- | ---: | ---: | --- |
| `categorical__grade_G` | 0.6723 | 1.9587 | associated with higher estimated default probability |
| `categorical__grade_F` | 0.5418 | 1.7191 | associated with higher estimated default probability |
| `categorical__addr_state_MS` | 0.4325 | 1.5411 | associated with higher estimated default probability |
| `categorical__grade_E` | 0.3343 | 1.3969 | associated with higher estimated default probability |
| `categorical__addr_state_AR` | 0.3164 | 1.3722 | associated with higher estimated default probability |

**Interpretation note:** Coefficients represent conditional associations within the regularized multivariate specification. Several underwriting variables are correlated, particularly grade, sub-grade, and interest rate, so individual coefficient signs and magnitudes should not be interpreted in isolation or as causal effects.

Full coefficient output is available in `models/pd_coefficients.csv`.

## 11. LGD Methodology

LGD is estimated on defaulted loans because LGD is loss severity conditional on default. The baseline definition is:

```text
LGD = 1 - recoveries / funded amount
```

The value is clipped to `[0, 1]`. The baseline mean LGD is `92.47%`, and the median LGD is `93.79%`. This high severity is consistent with low observed recoveries relative to funded amount in the defaulted-loan population.

## 12. EAD Methodology

EAD is proxied by funded amount:

```text
EAD = funded amount
```

This is transparent and available for all loans, but it is not a true balance-at-default calculation.

## 13. Expected Loss Framework

Loan-level expected loss is calculated as:

```text
Expected Loss = PD x LGD x EAD
```

The baseline portfolio has total EAD of `$19.39B` and baseline Expected Loss of `$3.86B`, corresponding to an expected-loss rate of `19.92%`.

## 14. Portfolio Risk Decomposition

Expected Loss is decomposed by grade, sub-grade, term, purpose, issue year, PD decile, loan-level concentration group, and PD x EAD driver cell.

Key observations:

- Expected-loss rate increases from grade A to grade G.
- Grade C contributes the largest total Expected Loss because it combines material risk with large exposure volume.
- The highest PD decile contributes `28.31%` of total Expected Loss.
- The top 10% of loans by loan-level Expected Loss contribute `34.15%` of total Expected Loss.
- The highest-PD/highest-EAD quartile cell contributes `29.22%` of total Expected Loss.

## 15. LGD Sensitivity

| LGD Definition | Mean LGD | Portfolio Expected Loss | Difference vs Baseline |
| --- | ---: | ---: | ---: |
| Gross recovery | 92.47% | $3.86B | 0.00% |
| Recovery net of fees | 93.72% | $3.91B | 1.35% |
| Principal recovery | 69.73% | $2.91B | -24.59% |
| Total payment | 46.70% | $1.95B | -49.50% |
| Net cashflow | 41.35% | $1.73B | -55.28% |

Expected-loss estimates are highly sensitive to the definition of economic recovery and LGD. The project therefore treats LGD definition as a sensitivity study rather than assuming a universally correct severity measure.

## 16. Scenario Analysis

The dashboard includes deterministic expected-loss scenario analysis. Users can apply controlled multipliers to PD, LGD, and EAD and observe the resulting effect on total Expected Loss and expected-loss rate.

This is a deterministic sensitivity framework rather than an estimated macroeconomic stress-testing model.

## 17. Expected Loss Reasonableness Check

The baseline Expected Loss estimate is close to the gross-recovery realized-loss proxy, with an EL / realized-loss ratio of `1.0023`. This comparison is useful as an internal consistency check, but it is not independent external validation because both values rely on related recovery and exposure information.

## 18. Assumptions and Limitations

1. LendingClub `grade`, `sub_grade`, and `int_rate` partially embed the lender's existing underwriting and pricing signal.
2. The accepted-loan sample does not represent the full population of loan applicants.
3. EAD is approximated using funded amount rather than a full exposure-at-default model.
4. Baseline LGD is simplified and sensitive to recovery-definition assumptions.
5. Out-of-time validation indicates temporal calibration drift.
6. Scenario analysis applies deterministic shocks and is not an econometrically estimated macro stress-testing model.
7. The project is an analytical research framework rather than a regulatory capital or accounting provisioning system.

## 19. Potential Extensions

- Recalibrate PD estimates by vintage or recent origination period.
- Estimate loan-level or segment-level LGD with minimum-count and validation controls.
- Improve EAD using balance-at-default or amortization information where available.
- Add an economically motivated scenario layer only if assumptions can be explicitly defended.
- Compare results on a different credit portfolio to evaluate external validity.
