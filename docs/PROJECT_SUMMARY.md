# Project Summary

This project builds an end-to-end analytical credit risk workflow using LendingClub accepted-loan data.

The workflow:

1. Defines a binary default target.
2. Trains and validates Probability of Default models.
3. Compares feature sets, model families, calibration approaches, and time validation.
4. Prepares LGD and EAD proxies.
5. Calculates preliminary loan-level Expected Loss.
6. Decomposes portfolio risk by segment, PD decile, and concentration group.
7. Tests LGD sensitivity and realized-loss proxy alignment.
8. Presents the results in a Streamlit dashboard.

## Final Framework

| component | selected approach |
| --- | --- |
| Dataset | LendingClub accepted loans |
| Target | `Fully Paid = 0`; `Charged Off / Default = 1` |
| PD model | Uncalibrated L2 Logistic Regression using Feature Set A |
| LGD | Recovery-based portfolio-average LGD |
| EAD | Funded amount |
| Expected Loss | `PD x LGD x EAD` |

## Headline Metrics

| metric | value |
| --- | ---: |
| Loans | 1,345,350 |
| Defaulted loans | 268,599 |
| Observed default rate | 19.96% |
| Mean predicted PD | 0.1997 |
| Portfolio-average LGD | 0.9247 |
| Total EAD | $19.39B |
| Total preliminary Expected Loss | $3.86B |
| Expected Loss rate | 19.92% |
| Highest PD decile share of EL | 28.31% |
| Top 10% loan-level EL concentration share | 34.15% |

## Key Limitations

- The final PD model uses LendingClub `grade`, `sub_grade`, and `int_rate`, which embed platform underwriting and pricing information.
- The borrower-only model has weaker but still meaningful signal.
- Time validation shows underprediction on newer loans.
- LGD is a constant portfolio average in the main Expected Loss framework.
- EAD is funded amount, not balance at default.
- Realized-loss proxy comparisons are reasonableness checks, not independent accounting validation.
- This is not a CECL, IFRS 9, Basel, pricing, capital, or production underwriting model.
