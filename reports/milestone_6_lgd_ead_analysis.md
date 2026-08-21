# Milestone 6: LGD and EAD Analysis

## 1. Objective

Milestone 6 prepares the non-PD components of Expected Loss:

```text
Expected Loss = PD x LGD x EAD
```

PD was finalized in Milestone 5 using the uncalibrated L2 Logistic Regression model with Feature Set A. Milestone 6 estimates LGD using defaulted loans and uses funded amount as the first EAD proxy.

These LGD and EAD values are preliminary, transparent, project-level estimates. They are suitable for building the first Expected Loss framework, but they are not production-grade LGD/EAD models.

## 2. Inputs and Outputs

Inputs used or referenced:

- `data/processed/loans_clean_v1.csv`
- `data/processed/loans_with_pd_v1.csv`
- `data/processed/defaulted_loans_lgd_v1.csv`
- `data/processed/lgd_ead_dataset_v1.csv`
- `data/processed/loans_with_pd_lgd_ead_v1.csv`

Outputs reviewed:

| output file | rows | columns |
| --- | ---: | ---: |
| `defaulted_loans_lgd_v1.csv` | 268,599 | 17 |
| `lgd_ead_dataset_v1.csv` | 1,345,350 | 12 |
| `loans_with_pd_lgd_ead_v1.csv` | 1,345,350 | 158 |

The all-loan LGD/EAD dataset and the combined PD/LGD/EAD dataset have the same row count as the final PD-scored dataset, which also has **1,345,350** rows.

## 3. Defaulted Loan Population

The LGD population contains **268,599** defaulted loans. This population uses:

```text
default_flag == 1
```

Defaulted loan status distribution:

| loan_status | count |
| --- | ---: |
| Charged Off | 268,559 |
| Default | 40 |

LGD is estimated only on defaulted loans because LGD measures loss severity **conditional on default**. Non-defaulted loans do not have an observed default loss outcome in this project setup.

## 4. EAD Proxy Analysis

Milestone 6 defines:

```text
ead_proxy = funded_amnt
```

EAD proxy summary across all loans:

| metric | value |
| --- | ---: |
| count | 1,345,350 |
| mean | $14,411.55 |
| median | $12,000.00 |
| min | $500.00 |
| 1st percentile | $1,500.00 |
| 5th percentile | $3,200.00 |
| 25th percentile | $8,000.00 |
| 75th percentile | $20,000.00 |
| 95th percentile | $32,825.00 |
| 99th percentile | $35,000.00 |
| max | $40,000.00 |

EAD data quality checks:

| check | count |
| --- | ---: |
| missing `ead_proxy` | 0 |
| zero or negative `ead_proxy` | 0 |

Funded amount is a reasonable first EAD proxy because it represents the original amount funded to the borrower and is available for all loans. The limitation is that funded amount is not the true outstanding balance at default. A production EAD model would usually estimate exposure at the time of default rather than using original funded amount.

## 5. LGD Construction

For defaulted loans, LGD was calculated as:

- `recoveries_filled = recoveries`, with missing values filled as implemented in the notebook
- `recovery_rate = recoveries_filled / ead_proxy`
- `lgd_raw = 1 - recovery_rate`
- `lgd = lgd_raw` clipped to `[0, 1]`

LGD and recovery summary:

| metric | value |
| --- | ---: |
| mean LGD | 0.9247 |
| median LGD | 0.9379 |
| standard deviation LGD | 0.0947 |
| 5th percentile LGD | 0.7766 |
| 25th percentile LGD | 0.8875 |
| 75th percentile LGD | 1.0000 |
| 95th percentile LGD | 1.0000 |
| portfolio average LGD | 0.9247 |
| mean recovery rate | 0.0754 |
| median recovery rate | 0.0621 |

LGD quality and boundary checks:

| metric | value |
| --- | ---: |
| zero recovery share | 31.24% |
| LGD = 1 share | 31.24% |
| LGD = 0 share | 0.04% |
| clipped LGD share | 0.04% |
| missing recoveries before fill | 0 |

These results imply high loss severity conditional on default. The average LGD is **0.9247**, meaning observed recoveries are low relative to funded amount. The median LGD is also high at **0.9379**, and the 75th and 95th percentiles are both **1.0000**, meaning many defaulted loans have little or no recovery.

## 6. LGD Segmentation

### LGD by Grade

| grade | default count | mean LGD | median LGD | mean recovery rate | mean EAD |
| --- | ---: | ---: | ---: | ---: | ---: |
| A | 14,206 | 0.9404 | 0.9783 | 0.0597 | $13,731.43 |
| B | 52,576 | 0.9341 | 0.9516 | 0.0659 | $13,548.77 |
| C | 85,657 | 0.9269 | 0.9365 | 0.0732 | $14,745.17 |
| D | 61,067 | 0.9221 | 0.9321 | 0.0780 | $16,004.51 |
| E | 36,041 | 0.9138 | 0.9216 | 0.0862 | $18,140.76 |
| F | 14,492 | 0.9068 | 0.9096 | 0.0933 | $19,564.98 |
| G | 4,560 | 0.9031 | 0.9034 | 0.0969 | $20,489.57 |

Average LGD is highest for grade A and lowest for grade G in this dataset. This does not mean grade A loans are riskier overall; PD and LGD answer different questions. Grade A loans default less often, but when they do default, observed recoveries relative to funded amount are still low. Grade G has higher PD risk, but conditional LGD is slightly lower in this recovery-based calculation.

### Highest Mean LGD Sub-Grades

| sub_grade | default count | mean LGD | median LGD | mean recovery rate | mean EAD |
| --- | ---: | ---: | ---: | ---: | ---: |
| A1 | 1,409 | 0.9437 | 0.9999 | 0.0563 | $14,249.13 |
| A4 | 3,588 | 0.9411 | 0.9751 | 0.0589 | $13,644.93 |
| A3 | 2,094 | 0.9401 | 0.9786 | 0.0600 | $13,359.90 |
| A2 | 1,734 | 0.9397 | 0.9879 | 0.0604 | $13,138.00 |
| A5 | 5,381 | 0.9393 | 0.9715 | 0.0608 | $13,989.34 |
| B1 | 7,416 | 0.9376 | 0.9615 | 0.0625 | $13,478.29 |
| B2 | 8,410 | 0.9360 | 0.9561 | 0.0641 | $13,432.69 |
| B3 | 10,625 | 0.9347 | 0.9519 | 0.0653 | $13,836.89 |
| B4 | 12,337 | 0.9342 | 0.9490 | 0.0658 | $13,680.75 |
| B5 | 13,788 | 0.9306 | 0.9454 | 0.0694 | $13,317.36 |
| C1 | 16,232 | 0.9300 | 0.9405 | 0.0700 | $13,857.69 |
| C2 | 16,414 | 0.9276 | 0.9394 | 0.0724 | $14,134.31 |

Sub-grade LGD patterns are consistent with the grade-level finding: the highest average LGD values are concentrated in stronger grades among the loans that defaulted. These segment estimates should be treated carefully, especially where default counts are smaller.

### LGD by Term

| term | default count | mean LGD | median LGD | mean recovery rate | mean EAD |
| --- | ---: | ---: | ---: | ---: | ---: |
| 36 months | 163,277 | 0.9298 | 0.9455 | 0.0703 | $12,598.90 |
| 60 months | 105,322 | 0.9168 | 0.9219 | 0.0833 | $20,142.53 |

LGD varies by term. The 36-month defaulted loans have a higher average LGD (**0.9298**) than 60-month defaulted loans (**0.9168**), while 60-month loans have much higher average EAD.

### LGD by Top Purposes

The table below shows the largest purpose categories by default count.

| purpose | default count | mean LGD | median LGD | mean recovery rate | mean EAD |
| --- | ---: | ---: | ---: | ---: | ---: |
| debt_consolidation | 165,035 | 0.9235 | 0.9354 | 0.0765 | $16,216.80 |
| credit_card | 49,988 | 0.9284 | 0.9438 | 0.0716 | $15,679.63 |
| other | 16,387 | 0.9233 | 0.9383 | 0.0768 | $11,429.80 |
| home_improvement | 15,505 | 0.9245 | 0.9359 | 0.0757 | $15,992.75 |
| major_purchase | 5,475 | 0.9274 | 0.9402 | 0.0727 | $15,034.95 |
| small_business | 4,580 | 0.9275 | 0.9448 | 0.0725 | $17,009.48 |
| medical | 3,389 | 0.9235 | 0.9409 | 0.0766 | $10,246.02 |
| moving | 2,214 | 0.9216 | 0.9352 | 0.0784 | $8,976.86 |
| car | 2,144 | 0.9311 | 0.9534 | 0.0690 | $10,433.83 |
| vacation | 1,738 | 0.9243 | 0.9402 | 0.0757 | $8,196.50 |

Among the largest purpose categories, average LGD is generally high and clustered around **0.92 to 0.93**. `car` has the highest average LGD among the top purposes shown, but its default count is much smaller than `debt_consolidation` or `credit_card`. Segment-level conclusions should not be overstated without minimum-count thresholds and validation.

### LGD by Issue Year

| issue year | default count | mean LGD | median LGD | mean recovery rate | mean EAD |
| --- | ---: | ---: | ---: | ---: | ---: |
| 2007 | 45 | 0.9132 | 0.9751 | 0.0868 | $10,293.33 |
| 2008 | 247 | 0.9426 | 0.9949 | 0.0575 | $10,178.44 |
| 2009 | 594 | 0.9402 | 0.9849 | 0.0599 | $10,485.98 |
| 2010 | 1,487 | 0.9469 | 0.9743 | 0.0531 | $10,291.88 |
| 2011 | 3,297 | 0.9436 | 0.9627 | 0.0564 | $12,847.58 |
| 2012 | 8,644 | 0.9360 | 0.9491 | 0.0641 | $14,704.24 |
| 2013 | 21,024 | 0.9203 | 0.9287 | 0.0798 | $15,690.15 |
| 2014 | 41,162 | 0.9168 | 0.9317 | 0.0832 | $15,572.75 |
| 2015 | 75,804 | 0.9198 | 0.9351 | 0.0802 | $15,726.51 |
| 2016 | 68,252 | 0.9228 | 0.9253 | 0.0772 | $15,403.88 |
| 2017 | 39,169 | 0.9329 | 0.9646 | 0.0672 | $15,806.31 |
| 2018 | 8,874 | 0.9676 | 1.0000 | 0.0324 | $17,029.57 |

LGD varies by issue year. The earliest years have small default counts, so their estimates are less stable. The 2018 cohort has a high average LGD of **0.9676**, but this may reflect shorter recovery seasoning or incomplete recovery observation rather than true long-run loss severity.

Overall, the portfolio-average LGD is more stable than thin segment-level estimates. Segment-level LGD may be useful later, but only after applying minimum default-count thresholds and validation.

## 7. Baseline LGD Estimate Choice

The current main LGD estimate is:

```text
portfolio-average LGD from defaulted loans = 0.9247
```

This is reasonable for the first Expected Loss implementation because it is:

- transparent
- stable
- easy to audit
- based only on observed defaulted loans
- less likely to overfit thin segment-level LGD patterns

Segment-level LGD tables can be used later if sample sizes and validation support them. For now, the portfolio-average LGD is the primary estimate.

## 8. PD + LGD + EAD Combined Dataset

The combined dataset is:

```text
data/processed/loans_with_pd_lgd_ead_v1.csv
```

Combined dataset summary:

| metric | value |
| --- | ---: |
| row count | 1,345,350 |
| expected PD output row count | 1,345,350 |
| PD column used | `predicted_pd` |
| mean predicted PD | 0.1997 |
| median predicted PD | 0.1787 |
| min predicted PD | 0.0000 |
| max predicted PD | 0.9999 |
| mean EAD | $14,411.55 |
| mean LGD estimate | 0.9247 |
| mean preliminary Expected Loss | $2,871.09 |
| median preliminary Expected Loss | $1,782.36 |
| total preliminary Expected Loss | $3,862,623,502.47 |

Validation checks:

| check | result |
| --- | --- |
| `predicted_pd` between 0 and 1 | Pass |
| `lgd_estimate` between 0 and 1 | Pass |
| `ead_proxy` non-negative | Pass |
| `expected_loss_prelim` non-negative | Pass |
| `expected_loss_prelim <= ead_proxy` | Pass |

## 9. Expected Loss Interpretation

The preliminary Expected Loss field is a loan-level expected credit loss under the current simplified framework:

```text
expected_loss_prelim = predicted_pd x lgd_estimate x ead_proxy
```

This is useful for project-level risk ranking and portfolio aggregation. It combines:

- final PD ranking from Milestone 5
- portfolio-average LGD from defaulted loans
- funded amount as the first EAD proxy

Because LGD is currently constant across loans, cross-sectional variation in preliminary Expected Loss mainly comes from:

- `predicted_pd`
- `funded_amnt` / `ead_proxy`

Richer LGD and EAD modeling would add more variation later, especially if segment-level LGD or balance-at-default estimates become reliable.

This Expected Loss output is not yet a production capital or accounting estimate.

## 10. Limitations

Key limitations:

- LGD is based on recoveries relative to funded amount, not a fully discounted economic loss.
- Recovery timing is ignored.
- Collection costs and recovery fees are not fully incorporated into economic LGD unless explicitly analyzed.
- EAD is proxied by funded amount, not actual balance at default.
- The PD model relies heavily on LendingClub `grade`, `sub_grade`, and `int_rate`.
- Prior time validation showed PD calibration drift and underprediction on newer loans.
- Therefore Expected Loss is project-ready but not production-ready.
- Segment-level LGD patterns may be unstable where default counts are small.
- The 2018 issue-year LGD may be affected by recovery seasoning or incomplete recovery observation.

## 11. Recommended Next Steps

Recommended next milestone steps:

1. Create final Expected Loss summary tables by grade, sub-grade, term, purpose, and vintage.
2. Analyze Expected Loss concentration by loan size and PD decile.
3. Compare realized losses against preliminary expected losses where possible.
4. Consider alternative LGD definitions, including:
   - incorporating `collection_recovery_fee`
   - using total payments or principal recovered
   - estimating net loss
5. Consider segment-level LGD only after enforcing minimum default-count thresholds.
6. Revisit PD calibration drift before treating Expected Loss as production-grade.

## 12. Final Milestone 6 Conclusion

Milestone 6 successfully created the LGD and EAD bridge needed for Expected Loss.

EAD uses funded amount. LGD uses recoveries on defaulted loans. The project now has loan-level PD, LGD estimate, EAD proxy, and preliminary Expected Loss.

The framework is suitable for project analysis and future refinement, but it is not suitable for production deployment without stronger LGD/EAD modeling, time validation, calibration monitoring, and economic loss adjustments.
