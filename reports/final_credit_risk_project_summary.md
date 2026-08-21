# Final Credit Risk Project Summary

## 1. Executive Summary

This project built an end-to-end credit risk workflow using LendingClub accepted-loan data. The workflow defines a binary default target, estimates Probability of Default (PD), prepares Loss Given Default (LGD) and Exposure at Default (EAD), and combines them into loan-level preliminary Expected Loss.

The selected PD model is an uncalibrated L2 Logistic Regression using Feature Set A, which includes LendingClub `grade`, `sub_grade`, and `int_rate`. The final Expected Loss framework uses `predicted_pd` from that model, a portfolio-average recovery-based LGD, and funded amount as the EAD proxy.

The framework is useful for risk ranking, segmentation, portfolio decomposition, and sensitivity analysis. It is project-ready, but not production-ready.

| headline metric | value |
| --- | ---: |
| Loans | 1,345,350 |
| Defaulted loans | 268,599 |
| Observed default rate | 19.96% |
| Mean predicted PD | 0.1997 |
| Portfolio-average LGD | 0.9247 |
| Total EAD | $19,388,585,275.00 |
| Total preliminary Expected Loss | $3,862,623,502.47 |
| Expected Loss rate | 19.92% |
| Highest PD decile share of Expected Loss | 28.31% |
| Top 10% loan-level EL concentration share | 34.15% |
| Baseline EL / gross recovery realized loss proxy ratio | 1.0023 |

## 2. Project Objective

The project objective was to build a complete analytical credit risk modeling workflow:

- Estimate Probability of Default.
- Prepare Loss Given Default.
- Prepare Exposure at Default.
- Combine PD, LGD, and EAD into Expected Loss:

```text
Expected Loss = PD x LGD x EAD
```

This project is analytical and educational. It is not a production underwriting system, accounting reserve model, pricing system, CECL/IFRS 9 process, or regulatory capital framework.

## 3. Data and Target Definition

The source data is LendingClub accepted-loan data. Milestone 1 created the binary `default_flag` target:

- `Fully Paid = 0`
- `Charged Off / Default = 1`
- Unresolved loan statuses were excluded.

The cleaned dataset is `data/processed/loans_clean_v1.csv`.

| metric | value |
| --- | ---: |
| Final cleaned loan count | 1,345,350 |
| Defaulted loan count | 268,599 |
| Non-defaulted loan count | 1,076,751 |
| Default rate | 19.96% |

## 4. PD Modeling Summary

The PD workflow began with a baseline logistic regression model and then tested feature sets, model families, calibration approaches, decile separation, and time validation.

Feature Set A, which includes LendingClub `grade`, `sub_grade`, and `int_rate`, performed strongest. Feature Set D, the borrower-only feature set that excludes those fields, still had signal but was weaker. In the feature set comparison output, Feature Set A had ROC-AUC of 0.7094 and PR-AUC of 0.3701, while Feature Set D had ROC-AUC of 0.6747 and PR-AUC of 0.3388.

| feature set version | ROC-AUC | PR-AUC | Brier Score | lowest decile default rate | highest decile default rate | high/low decile ratio |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `A_baseline` | 0.7094 | 0.3701 | 0.1453 | 4.27% | 44.91% | 10.5170 |
| `B_remove_sub_grade` | 0.7074 | 0.3686 | 0.1455 | 4.63% | 44.77% | 9.6608 |
| `C_remove_grade_and_sub_grade` | 0.7051 | 0.3647 | 0.1462 | 4.66% | 44.34% | 9.5068 |
| `D_borrower_only` | 0.6747 | 0.3388 | 0.1495 | 6.92% | 42.03% | 6.0774 |

The model family comparison showed that tree models did not materially beat logistic regression. L2 Logistic Regression was selected because it provided similar performance to the baseline logistic model while retaining stability and interpretability.

| feature set | model | ROC-AUC | PR-AUC | Brier Score | high/low decile ratio |
| --- | --- | ---: | ---: | ---: | ---: |
| Feature Set A | Logistic Regression Baseline | 0.7094 | 0.3701 | 0.1453 | 10.5170 |
| Feature Set A | Regularized Logistic Regression L2 | 0.7093 | 0.3701 | 0.1453 | 10.5414 |
| Feature Set A | Gradient Boosting | 0.7068 | 0.3700 | 0.1456 | 10.5690 |
| Feature Set A | Random Forest | 0.7050 | 0.3676 | 0.1463 | 10.6109 |
| Feature Set D | Logistic Regression Baseline | 0.6747 | 0.3388 | 0.1495 | 6.0774 |
| Feature Set D | Regularized Logistic Regression L2 | 0.6747 | 0.3388 | 0.1495 | 6.0839 |
| Feature Set D | Gradient Boosting | 0.6732 | 0.3397 | 0.1497 | 6.2710 |
| Feature Set D | Random Forest | 0.6725 | 0.3393 | 0.1504 | 6.0188 |

Calibration methods did not materially improve the model. The final selected model is:

- PD model: Uncalibrated L2 Logistic Regression using Feature Set A.
- Model artifact: `models/final_pd_model_v1.pkl`.
- Scored dataset: `data/processed/loans_with_pd_v1.csv`.
- Final PD column: `predicted_pd`.

| calibration model | ROC-AUC | PR-AUC | Brier Score | Log Loss | mean PD - actual | calibration slope | high/low decile ratio |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Isotonic Calibrated L2 Logistic Regression | 0.7083 | 0.3652 | 0.1454 | 0.4550 | -0.0001 | 0.9905 | 10.7425 |
| Uncalibrated L2 Logistic Regression | 0.7084 | 0.3689 | 0.1455 | 0.4553 | 0.0001 | 0.9968 | 10.6081 |
| Sigmoid Calibrated L2 Logistic Regression | 0.7084 | 0.3689 | 0.1455 | 0.4553 | -0.0001 | 0.9972 | 10.6081 |

The selected model's final-selection table reports ROC-AUC of 0.7084, PR-AUC of 0.3689, Brier Score of 0.1455, Log Loss of 0.4553, and a high/low decile default-rate ratio of 10.6081.

## 5. PD Model Interpretation and Limitations

The PD model ranks risk well. On the final calibration comparison, the lowest decile default rate was 4.21% and the highest decile default rate was 44.67% for the selected uncalibrated L2 Logistic Regression. The model's decile separation is strong enough for project-level risk ranking and segmentation.

The main interpretation caveat is that Feature Set A relies heavily on LendingClub `grade`, `sub_grade`, and `int_rate`. These variables improve predictive power, but they also embed LendingClub's own underwriting and risk-pricing assessment. As a result, the model is not a purely borrower-characteristics model.

Time validation remains the most important PD limitation. In the calibration time-validation output for the uncalibrated L2 model, the time test set had 282,970 loans, mean predicted PD of 0.1937, actual default rate of 0.2182, and mean PD minus actual default rate of -0.0245. ROC-AUC was 0.6953 and Brier Score was 0.1579. This indicates underprediction on newer loans and performance degradation versus the random-split validation.

The PD model is suitable for project analysis, but production deployment would require stronger out-of-time validation, monitoring, recalibration, and governance.

## 6. LGD and EAD Framework

Milestone 6 estimated LGD only on defaulted loans because LGD measures loss severity conditional on default. The EAD proxy is funded amount:

```text
ead_proxy = funded_amnt
```

The baseline LGD definition is:

```text
LGD = 1 - recoveries / funded amount
```

The result is clipped to `[0, 1]`. A single portfolio-average LGD is assigned to all loans in the preliminary Expected Loss framework. This is transparent, stable, and easy to audit, but simplified.

| LGD/EAD metric | value |
| --- | ---: |
| Defaulted loans used for LGD | 268,599 |
| Mean LGD | 0.9247 |
| Median LGD | 0.9379 |
| Mean recovery rate | 0.0754 |
| Zero recovery share | 31.24% |
| Mean EAD | $14,411.55 |
| Median EAD | $12,000.00 |
| Total EAD | $19,388,585,275.00 |

The baseline LGD is high, but it is consistent with low observed recoveries relative to funded amount in the defaulted-loan population. The main simplification is that funded amount is not balance at default, and the baseline LGD is a constant portfolio average rather than a segment-specific or loan-level severity model.

## 7. Expected Loss Framework

Milestone 7 combined PD, LGD, and EAD into loan-level preliminary Expected Loss:

```text
expected_loss_prelim = predicted_pd x lgd_estimate x ead_proxy
```

Because `lgd_estimate` is constant across loans in the main framework, cross-sectional Expected Loss variation mainly comes from `predicted_pd` and `ead_proxy`.

| Expected Loss metric | value |
| --- | ---: |
| Loan count | 1,345,350 |
| Total EAD | $19,388,585,275.00 |
| Total preliminary Expected Loss | $3,862,623,502.47 |
| Mean preliminary Expected Loss | $2,871.09 |
| Median preliminary Expected Loss | $1,782.36 |
| Expected Loss rate | 19.92% |
| Mean predicted PD | 0.1997 |
| Median predicted PD | 0.1787 |
| Mean LGD estimate | 0.9247 |

## 8. Portfolio Risk Decomposition

Expected Loss increases as LendingClub grade worsens, but total EL also depends on exposure volume. Grade C contributes the most total EL, while grade G has the highest EL rate.

| grade | loan count | default rate | total EAD | total EL | EL rate | mean PD |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| A | 235,095 | 6.04% | $3,263,735,050.00 | $184,528,056.64 | 5.65% | 0.0604 |
| B | 392,748 | 13.39% | $5,195,857,925.00 | $659,333,895.19 | 12.69% | 0.1336 |
| C | 381,694 | 22.44% | $5,413,717,400.00 | $1,166,734,030.75 | 21.55% | 0.2240 |
| D | 200,966 | 30.39% | $3,068,057,125.00 | $897,613,439.87 | 29.26% | 0.3047 |
| E | 93,656 | 38.48% | $1,648,265,625.00 | $606,083,840.35 | 36.77% | 0.3865 |
| F | 32,059 | 45.20% | $611,075,025.00 | $260,557,662.87 | 42.64% | 0.4519 |
| G | 9,132 | 49.93% | $187,877,125.00 | $87,772,576.81 | 46.72% | 0.5015 |

Sub-grade decomposition showed that C4 had the largest total Expected Loss at $264,053,658.81, while G5 had the highest Expected Loss rate at 47.46%. Term decomposition showed that 60-month loans had higher total EL and higher EL rate than 36-month loans. Purpose decomposition showed `debt_consolidation` had the largest total EL at $2,498,777,975.60, while `small_business` had the highest purpose EL rate at 28.34%. Issue-year decomposition showed the highest issue-year EL rate in 2014 at 20.55% and the lowest in 2009 at 15.31%.

PD deciles show strong separation in both realized default rates and Expected Loss rates:

| PD decile | mean PD | realized default rate | total EL | EL rate | share of total EL |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.0424 | 4.25% | $71,682,920.16 | 3.91% | 1.86% |
| 2 | 0.0764 | 7.70% | $125,428,436.87 | 7.05% | 3.25% |
| 3 | 0.1058 | 10.52% | $168,344,101.75 | 9.78% | 4.36% |
| 4 | 0.1339 | 13.21% | $213,553,874.09 | 12.38% | 5.53% |
| 5 | 0.1632 | 16.35% | $264,283,539.70 | 15.10% | 6.84% |
| 6 | 0.1950 | 19.58% | $323,295,928.66 | 18.04% | 8.37% |
| 7 | 0.2306 | 22.97% | $400,448,904.42 | 21.34% | 10.37% |
| 8 | 0.2730 | 27.07% | $509,817,687.57 | 25.28% | 13.20% |
| 9 | 0.3312 | 33.06% | $692,333,373.50 | 30.71% | 17.92% |
| 10 | 0.4456 | 44.93% | $1,093,434,735.74 | 41.43% | 28.31% |

Loan-level EL concentration is meaningful. The top 10% of loans by Expected Loss account for 34.15% of total EL and 19.28% of total EAD.

| concentration group | share of loans | total EL | share of total EL | share of total EAD | mean PD | mean EAD |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Top 1% by EL | 1.00% | $206,385,813.29 | 5.34% | 2.31% | 0.5026 | $33,271.04 |
| Top 5% by EL | 5.00% | $787,059,997.86 | 20.38% | 10.45% | 0.4282 | $30,130.97 |
| Top 10% by EL | 10.00% | $1,319,202,883.65 | 34.15% | 19.28% | 0.3926 | $27,780.53 |
| Top 20% by EL | 20.00% | $2,081,276,990.48 | 53.88% | 34.22% | 0.3517 | $24,657.80 |

The correlation between `predicted_pd` and `expected_loss_prelim` is 0.7581. The correlation between `ead_proxy` and `expected_loss_prelim` is 0.7152. The highest PD x highest EAD driver cell, `Q4_highest_pd` and `Q4_highest_ead`, contributes $1,128,828,729.55, or 29.22% of total Expected Loss.

## 9. LGD Sensitivity and Realized Loss Proxy Checks

Milestone 8 tested five LGD definitions:

- Baseline gross recovery LGD.
- Net recovery fee LGD.
- Principal recovery LGD.
- Total payment LGD.
- Net cashflow LGD.

Recovery-based definitions were close to the baseline. Payment-inclusive definitions produced much lower LGD and total Expected Loss.

| LGD definition | mean LGD | median LGD | total EL | percent difference from baseline |
| --- | ---: | ---: | ---: | ---: |
| `lgd_baseline` | 0.9247 | 0.9379 | $3,862,623,502.47 | 0.00% |
| `lgd_net_recovery_fee` | 0.9372 | 0.9478 | $3,914,882,291.95 | 1.35% |
| `lgd_principal_recovery` | 0.6973 | 0.7473 | $2,912,666,275.63 | -24.59% |
| `lgd_total_payment` | 0.4670 | 0.4944 | $1,950,784,167.68 | -49.50% |
| `lgd_net_cashflow` | 0.4135 | 0.4309 | $1,727,361,404.08 | -55.28% |

The gross recovery realized loss proxy is $3,853,836,506.13. Baseline Expected Loss is $3,862,623,502.47, giving a baseline EL / gross recovery realized proxy ratio of 1.0023. This close alignment supports the recovery-based LGD as the preferred main project baseline.

Vintage LGD sensitivity showed higher LGDs in newer vintages. Mean baseline LGD was 0.9329 in 2017 and 0.9676 in 2018, compared with 0.9168 in 2014 and 0.9198 in 2015. This may reflect recovery seasoning, especially because newer defaults may have less time to accumulate recoveries and post-origination payments. It also links back to the PD time-validation concern around newer loans.

Recovery-based LGD remains the preferred project baseline because it is closest to conditional default severity and aligns closely with the gross recovery realized loss proxy.

## 10. Final Model and Framework Choice

The final recommended project framework is:

| component | selected approach |
| --- | --- |
| PD | Uncalibrated L2 Logistic Regression using Feature Set A |
| PD field | `predicted_pd` |
| LGD | Recovery-based portfolio-average LGD from defaulted loans |
| LGD definition | `1 - recoveries / funded amount` |
| EAD | Funded amount |
| Expected Loss | `predicted_pd x baseline portfolio-average LGD x funded amount` |

This framework is preferred because it is transparent, interpretable, stable, and empirically reasonable against the gross recovery realized loss proxy. It supports portfolio segmentation, risk ranking, concentration analysis, and sensitivity testing. LGD sensitivity scenarios should be retained for transparency.

## 11. Key Findings

- The PD model ranks risk well, with strong PD decile separation.
- Feature Set A dominates borrower-only features, but that strength depends partly on LendingClub grade, sub-grade, and interest rate.
- Tree models did not materially improve over regularized logistic regression.
- Calibration did not materially improve the final PD model.
- Time drift is the main PD concern: the uncalibrated L2 model underpredicted the time-test default rate by 0.0245.
- Baseline LGD is high at 0.9247, but defensible under a recovery-based conditional-default severity definition.
- Expected Loss is concentrated in weaker grades, higher PD deciles, and high PD/high EAD loans.
- The highest PD decile contributes 28.31% of total Expected Loss.
- The top 10% of loans by Expected Loss contribute 34.15% of total Expected Loss.
- LGD sensitivity shows large differences depending on whether pre-default payments are included.
- Baseline Expected Loss aligns closely with the gross recovery realized loss proxy, with a ratio of 1.0023.
- The current framework is suitable for project analysis, but not production deployment.

## 12. Limitations

- LendingClub data may not generalize to other portfolios.
- The target definition excludes unresolved loans.
- The PD model relies heavily on `grade`, `sub_grade`, and `int_rate`.
- Those fields embed LendingClub's own risk assessment and pricing.
- PD calibration drift was observed over time.
- LGD uses recoveries relative to funded amount, not discounted economic loss.
- Recovery timing is ignored.
- EAD is funded amount, not balance at default.
- LGD is assigned as a constant portfolio average in the main framework.
- Segment-level LGD is not yet used in the main EL calculation.
- Payment-inclusive LGD definitions may mix pre-default and post-default cashflows.
- This is not CECL, IFRS 9, Basel capital, pricing, or production underwriting.

## 13. Recommendations

1. Use the current framework as the final project baseline.
2. Present recovery-based LGD as the main LGD, with alternative LGD scenarios as sensitivity checks.
3. Treat Expected Loss as a risk ranking and portfolio analysis measure, not a production reserve or capital estimate.
4. Revisit PD calibration drift before any production use.
5. Add out-of-time monitoring and recalibration.
6. Consider borrower-only sensitivity if the goal is to model risk without LendingClub grades or pricing fields.
7. Consider segment-level LGD only after minimum-count thresholds and validation.
8. Develop a better EAD proxy based on balance at default if available.
9. Add stress testing by increasing PD, LGD, or both.
10. Create a presentation-ready summary for stakeholders if needed.

## 14. Final Conclusion

The project successfully built an end-to-end credit risk workflow from cleaned loan data to PD, LGD, EAD, and Expected Loss. The final framework is transparent, interpretable, and empirically reasonable for project analysis.

The project demonstrates risk ranking, portfolio decomposition, sensitivity testing, and realized proxy comparison. It should not be considered production-ready because PD calibration drift remains unresolved and LGD/EAD are simplified.

The recommended final baseline is:

- PD: uncalibrated L2 Logistic Regression with Feature Set A.
- LGD: recovery-based portfolio-average LGD.
- EAD: funded amount.
- EL: `PD x LGD x EAD`.
