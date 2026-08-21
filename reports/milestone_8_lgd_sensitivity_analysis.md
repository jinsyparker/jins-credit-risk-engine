# Milestone 8: LGD Sensitivity and Realized Loss Proxy Comparison

## 1. Objective

Milestone 8 tests whether the preliminary Expected Loss framework is sensitive to the definition of Loss Given Default (LGD), and compares expected loss against realized loss proxies where possible.

Milestone 6 used a simple baseline LGD based on recoveries relative to funded amount. Milestone 7 showed that Expected Loss (EL) variation was mainly driven by `predicted_pd` and `ead_proxy`, because LGD was held constant across loans. Milestone 8 tests alternative LGD definitions and evaluates how much portfolio Expected Loss changes under those definitions.

This is a robustness and reasonableness check. It is not a production LGD model, accounting loss model, pricing model, or capital model.

## 2. Inputs and Outputs

The analysis references the Milestone 8 notebook at `notebooks/10_lgd_sensitivity_and_realized_loss.ipynb`.

Project context used:

- Final PD model from Milestone 5: Uncalibrated L2 Logistic Regression using Feature Set A.
- Final PD column: `predicted_pd`.
- Milestone 6 baseline EAD: `ead_proxy = funded_amnt`.
- Milestone 6 baseline LGD: `1 - recoveries / funded_amnt`, clipped to `[0, 1]`.
- Milestone 6 baseline `lgd_estimate`: portfolio-average LGD from defaulted loans.
- Milestone 7 preliminary Expected Loss: `predicted_pd x lgd_estimate x ead_proxy`.
- Milestone 7 caveat: because LGD was constant across loans, EL variation mainly came from PD and EAD.

Tabular inputs and outputs reviewed:

| file | role | rows | columns |
| --- | --- | --- | --- |
| `loans_clean_v1.csv` | Input | 1,345,350 | 152 |
| `defaulted_loans_lgd_v1.csv` | Input | 268,599 | 17 |
| `loans_with_pd_lgd_ead_v1.csv` | Input | 1,345,350 | 158 |
| `lgd_sensitivity_defaulted_loans_v1.csv` | Milestone 8 output | 268,599 | 44 |
| `lgd_sensitivity_summary_v1.csv` | Milestone 8 output | 5 | 15 |
| `expected_loss_lgd_sensitivity_summary_v1.csv` | Milestone 8 output | 6 | 8 |
| `realized_vs_expected_loss_summary_v1.csv` | Milestone 8 output | 4 | 7 |
| `realized_loss_proxy_by_grade_v1.csv` | Milestone 8 output | 7 | 12 |
| `realized_loss_proxy_by_pd_decile_v1.csv` | Milestone 8 output | 10 | 12 |
| `lgd_sensitivity_by_vintage_v1.csv` | Milestone 8 output | 12 | 17 |

## 3. LGD Definitions Tested

The following LGD definitions appear in `lgd_sensitivity_summary_v1.csv`:

| LGD definition | Interpretation |
| --- | --- |
| `lgd_baseline` | Baseline or gross recovery LGD: `1 - recoveries / EAD`. |
| `lgd_net_recovery_fee` | Net recovery fee LGD: `1 - (recoveries - collection_recovery_fee) / EAD`. |
| `lgd_principal_recovery` | Principal recovery LGD: `1 - total_rec_prncp / EAD`. |
| `lgd_total_payment` | Total payment LGD: `1 - total_pymnt / EAD`. |
| `lgd_net_cashflow` | Net cashflow LGD: `1 - (total_pymnt + recoveries - collection_recovery_fee) / EAD`. |

No candidate definition in this set was skipped. The required fields for these definitions were present in the Milestone 8 output files.

## 4. LGD Sensitivity Results

| LGD definition | valid count | mean LGD | median LGD | std dev | p05 | p25 | p75 | p95 | share LGD = 1 | share LGD = 0 | share clipped |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `lgd_baseline` | 268,599 | 0.9247 | 0.9379 | 0.0947 | 0.7766 | 0.8875 | 1.0000 | 1.0000 | 31.24% | 0.04% | 0.04% |
| `lgd_net_recovery_fee` | 268,599 | 0.9372 | 0.9478 | 0.0786 | 0.8157 | 0.9058 | 1.0000 | 1.0000 | 31.24% | 0.02% | 0.02% |
| `lgd_principal_recovery` | 268,599 | 0.6973 | 0.7473 | 0.2188 | 0.2560 | 0.5666 | 0.8719 | 0.9617 | 0.92% | 0.01% | 0.00% |
| `lgd_total_payment` | 268,599 | 0.4670 | 0.4944 | 0.2632 | 0.0000 | 0.2648 | 0.6765 | 0.8611 | 0.31% | 7.03% | 7.03% |
| `lgd_net_cashflow` | 268,599 | 0.4135 | 0.4309 | 0.2652 | 0.0000 | 0.1985 | 0.6149 | 0.8452 | 0.31% | 11.29% | 11.29% |

`lgd_net_recovery_fee` is the most severe definition, with mean LGD of 0.9372. `lgd_net_cashflow` is the least severe, with mean LGD of 0.4135.

The recovery-based baseline and net recovery fee LGDs are close: mean LGD moves from 0.9247 to 0.9372. Payment-inclusive definitions are materially lower. `lgd_total_payment` has mean LGD of 0.4670, while `lgd_net_cashflow` has mean LGD of 0.4135. `lgd_principal_recovery` is also materially lower than the baseline, at 0.6973.

Clipping is negligible for the baseline, net recovery fee, and principal recovery definitions. It is meaningful for payment-inclusive definitions: `lgd_total_payment` has 7.03% clipped and `lgd_net_cashflow` has 11.29% clipped. Relative to the payment-inclusive alternatives, the baseline LGD is conservative.

## 5. Expected Loss Sensitivity to LGD Definition

| scenario name | portfolio avg LGD | total Expected Loss | mean Expected Loss | Expected Loss rate | diff vs baseline total EL | % diff vs baseline total EL |
| --- | --- | --- | --- | --- | --- | --- |
| `milestone_6_baseline_expected_loss_prelim` | 0.9247 | $3,862,623,502.47 | $2,871.09 | 0.1992 | $0.00 | 0.00% |
| `lgd_baseline` | 0.9247 | $3,862,623,502.47 | $2,871.09 | 0.1992 | $0.00 | 0.00% |
| `lgd_net_recovery_fee` | 0.9372 | $3,914,882,291.95 | $2,909.94 | 0.2019 | $52,258,789.48 | 1.35% |
| `lgd_principal_recovery` | 0.6973 | $2,912,666,275.63 | $2,164.99 | 0.1502 | $-949,957,226.85 | -24.59% |
| `lgd_total_payment` | 0.4670 | $1,950,784,167.68 | $1,450.02 | 0.1006 | $-1,911,839,334.79 | -49.50% |
| `lgd_net_cashflow` | 0.4135 | $1,727,361,404.08 | $1,283.95 | 0.0891 | $-2,135,262,098.39 | -55.28% |

Total Expected Loss is stable under the two post-default recovery definitions: the net recovery fee scenario is only 1.35% above the baseline. It is much more sensitive to definitions that include borrower payments or principal repayment. `lgd_principal_recovery` lowers total EL by 24.59%, `lgd_total_payment` lowers it by 49.50%, and `lgd_net_cashflow` lowers it by 55.28%.

The highest Expected Loss scenario is `lgd_net_recovery_fee`, at $3,914,882,291.95. The lowest is `lgd_net_cashflow`, at $1,727,361,404.08. The baseline is slightly less severe than the net recovery fee scenario, but conservative relative to the principal recovery and payment-inclusive alternatives.

## 6. Realized Loss Proxy Comparison

| realized loss proxy | total Expected Loss | total realized loss proxy | expected minus realized | ratio expected/realized | Expected Loss rate | realized proxy rate |
| --- | --- | --- | --- | --- | --- | --- |
| `realized_loss_gross_recovery` | $3,862,623,502.47 | $3,853,836,506.13 | $8,786,996.34 | 1.0023 | 0.1992 | 0.1988 |
| `realized_loss_net_recovery_fee` | $3,862,623,502.47 | $3,907,925,062.07 | $-45,301,559.60 | 0.9884 | 0.1992 | 0.2016 |
| `realized_loss_principal` | $3,862,623,502.47 | $2,999,967,360.24 | $862,656,142.23 | 1.2876 | 0.1992 | 0.1547 |
| `realized_loss_total_payment` | $3,862,623,502.47 | $1,988,465,537.23 | $1,874,157,965.25 | 1.9425 | 0.1992 | 0.1026 |

Preliminary Expected Loss is very close to the gross recovery realized loss proxy: expected loss is $8,786,996.34 higher, with a ratio of 1.0023. The net recovery fee proxy is slightly higher than preliminary Expected Loss, with a ratio of 0.9884. The principal and total payment proxies are much lower than preliminary Expected Loss.

The closest realized proxy is `realized_loss_gross_recovery`. The most conservative realized proxy by total loss is `realized_loss_net_recovery_fee`, at $3,907,925,062.07. The least conservative is `realized_loss_total_payment`, at $1,988,465,537.23.

These proxies differ because they measure different cashflow concepts. Gross and net recovery proxies focus on recoveries after default or charge-off. Principal and total payment proxies include borrower payments that may have occurred before default, which can reduce measured loss but does not necessarily isolate severity at default. None of these proxies should be interpreted as true accounting or discounted economic loss.

## 7. Realized Loss Proxy by Grade

| grade | loan count | default count | total EAD | total Expected Loss | total realized loss proxy | Expected Loss rate | realized proxy rate | expected minus realized | ratio expected/realized |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 235,095 | 14,206 | $3,263,735,050.00 | $184,528,056.64 | $183,549,199.48 | 0.0565 | 0.0562 | $978,857.15 | 1.0053 |
| B | 392,748 | 52,576 | $5,195,857,925.00 | $659,333,895.19 | $665,047,658.79 | 0.1269 | 0.1280 | $-5,713,763.60 | 0.9914 |
| C | 381,694 | 85,657 | $5,413,717,400.00 | $1,166,734,030.75 | $1,168,949,635.09 | 0.2155 | 0.2159 | $-2,215,604.34 | 0.9981 |
| D | 200,966 | 61,067 | $3,068,057,125.00 | $897,613,439.87 | $899,382,800.34 | 0.2926 | 0.2931 | $-1,769,360.47 | 0.9980 |
| E | 93,656 | 36,041 | $1,648,265,625.00 | $606,083,840.35 | $596,062,453.27 | 0.3677 | 0.3616 | $10,021,387.08 | 1.0168 |
| F | 32,059 | 14,492 | $611,075,025.00 | $260,557,662.87 | $256,485,552.81 | 0.4264 | 0.4197 | $4,072,110.06 | 1.0159 |
| G | 9,132 | 4,560 | $187,877,125.00 | $87,772,576.81 | $84,359,206.36 | 0.4672 | 0.4490 | $3,413,370.45 | 1.0405 |

Expected Loss and realized loss proxy rates move consistently by grade. Expected Loss rate rises from 0.0565 in grade A to 0.4672 in grade G. Realized loss proxy rate rises from 0.0562 in grade A to 0.4490 in grade G.

The largest absolute gaps between expected and realized proxy loss are in grades E, B, F, G, and C. Grade E has the largest positive gap, with Expected Loss $10,021,387.08 above the realized proxy. Grade B has the largest negative gap, with Expected Loss $5,713,763.60 below the realized proxy.

Total loss and loss rate tell different stories. Grade C has the largest total Expected Loss and total realized loss proxy because it has a large EAD base and many defaults. Grade G has the highest loss rates, but much smaller total EAD.

## 8. Realized Loss Proxy by PD Decile

| PD decile | loan count | default count | mean predicted PD | realized default rate | total EAD | total Expected Loss | total realized loss proxy | Expected Loss rate | realized proxy rate | ratio expected/realized |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 134,535 | 5,720 | 0.0424 | 0.0425 | $1,832,126,975.00 | $71,682,920.16 | $73,859,541.98 | 0.0391 | 0.0403 | 0.9705 |
| 2 | 134,535 | 10,362 | 0.0764 | 0.0770 | $1,779,778,200.00 | $125,428,436.87 | $125,115,412.18 | 0.0705 | 0.0703 | 1.0025 |
| 3 | 134,535 | 14,157 | 0.1058 | 0.1052 | $1,721,490,025.00 | $168,344,101.75 | $170,474,692.69 | 0.0978 | 0.0990 | 0.9875 |
| 4 | 134,535 | 17,767 | 0.1339 | 0.1321 | $1,725,148,900.00 | $213,553,874.09 | $211,437,532.90 | 0.1238 | 0.1226 | 1.0100 |
| 5 | 134,535 | 22,001 | 0.1632 | 0.1635 | $1,750,654,600.00 | $264,283,539.70 | $267,667,613.99 | 0.1510 | 0.1529 | 0.9874 |
| 6 | 134,535 | 26,346 | 0.1950 | 0.1958 | $1,792,173,825.00 | $323,295,928.66 | $328,484,023.30 | 0.1804 | 0.1833 | 0.9842 |
| 7 | 134,535 | 30,904 | 0.2306 | 0.2297 | $1,876,739,750.00 | $400,448,904.42 | $403,142,402.43 | 0.2134 | 0.2148 | 0.9933 |
| 8 | 134,535 | 36,417 | 0.2730 | 0.2707 | $2,017,046,000.00 | $509,817,687.57 | $508,123,235.83 | 0.2528 | 0.2519 | 1.0033 |
| 9 | 134,535 | 44,482 | 0.3312 | 0.3306 | $2,254,311,875.00 | $692,333,373.50 | $687,100,105.05 | 0.3071 | 0.3048 | 1.0076 |
| 10 | 134,535 | 60,443 | 0.4456 | 0.4493 | $2,639,115,125.00 | $1,093,434,735.74 | $1,078,431,945.79 | 0.4143 | 0.4086 | 1.0139 |

Realized loss proxy rate increases across PD deciles, from 0.0403 in decile 1 to 0.4086 in decile 10. Expected Loss rate also increases across deciles, from 0.0391 to 0.4143.

The PD ranking is useful for realized loss proxy separation: both realized default rate and realized proxy loss rate rise strongly across deciles. Expected Loss is below the realized proxy in deciles 1, 3, 5, 6, and 7, and above the realized proxy in deciles 2, 4, 8, 9, and 10. The ratios are close to 1.0000 across all deciles, with the largest ratio in decile 10 at 1.0139 and the lowest in decile 1 at 0.9705.

## 9. Vintage LGD Sensitivity

| issue year | default count | mean baseline LGD | mean net recovery fee LGD | mean principal recovery LGD | mean total payment LGD | mean net cashflow LGD | median baseline LGD |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2007 | 45 | 0.9132 | 0.9387 | 0.5617 | 0.3592 | 0.3379 | 0.9751 |
| 2008 | 247 | 0.9426 | 0.9558 | 0.6132 | 0.4530 | 0.4400 | 0.9949 |
| 2009 | 594 | 0.9402 | 0.9545 | 0.6350 | 0.4653 | 0.4454 | 0.9849 |
| 2010 | 1,487 | 0.9469 | 0.9555 | 0.6262 | 0.4257 | 0.4007 | 0.9743 |
| 2011 | 3,297 | 0.9436 | 0.9490 | 0.6510 | 0.4318 | 0.3979 | 0.9627 |
| 2012 | 8,644 | 0.9360 | 0.9411 | 0.6256 | 0.3953 | 0.3489 | 0.9491 |
| 2013 | 21,024 | 0.9203 | 0.9299 | 0.6242 | 0.3556 | 0.3000 | 0.9287 |
| 2014 | 41,162 | 0.9168 | 0.9304 | 0.6350 | 0.3652 | 0.3097 | 0.9317 |
| 2015 | 75,804 | 0.9198 | 0.9341 | 0.6635 | 0.4169 | 0.3632 | 0.9351 |
| 2016 | 68,252 | 0.9228 | 0.9363 | 0.7102 | 0.4839 | 0.4261 | 0.9253 |
| 2017 | 39,169 | 0.9329 | 0.9444 | 0.8179 | 0.6379 | 0.5842 | 0.9646 |
| 2018 | 8,874 | 0.9676 | 0.9733 | 0.9219 | 0.8376 | 0.8120 | 1.0000 |

LGD sensitivity changes by vintage. Mean baseline LGD is lowest in 2007 at 0.9132 and highest in 2018 at 0.9676, though 2007 has only 45 defaults. The newer 2017 and 2018 vintages show higher LGDs across the principal recovery, total payment, and net cashflow definitions.

Recovery seasoning may explain part of the vintage pattern. Newer defaults may have less time to accumulate recoveries or post-origination payments in the dataset, especially for payment-inclusive definitions. This reinforces the prior PD time-validation caveat: newer loans were already an area of concern because time validation showed underprediction on newer loans.

## 10. Key Findings

- Baseline LGD is severe at 0.9247 and close to the net recovery fee LGD of 0.9372.
- The net recovery fee definition is the most severe LGD definition tested; the net cashflow definition is the least severe.
- Recovery-based gross and net LGDs produce similar total Expected Loss, with net recovery fee EL only 1.35% above baseline.
- Payment-inclusive definitions produce much lower EL: total payment EL is 49.50% below baseline and net cashflow EL is 55.28% below baseline.
- Preliminary Expected Loss is very close to the gross recovery realized loss proxy, with a ratio of 1.0023.
- Grade-level realized loss proxy rates rise from grade A to grade G, and PD-decile realized proxy rates rise from decile 1 to decile 10.
- Vintage analysis shows higher LGDs in newer vintages, especially 2017 and 2018, which may reflect recovery seasoning as well as the prior time-validation caveat.

## 11. Implications for the Project

If the project keeps the baseline LGD, Expected Loss remains conservative relative to principal recovery and payment-inclusive alternatives, and very close to the gross recovery realized loss proxy. The baseline is also only slightly less conservative than the net recovery fee scenario.

If a payment-based LGD is used, Expected Loss may be much lower. However, those definitions may mix pre-default borrower payments with post-default recoveries, so they are less clean as conditional-default severity measures.

Recovery-based LGD is closer to default severity conditional on charged-off or defaulted loans. Realized loss proxy comparisons help test reasonableness, but they are not a substitute for production validation. The next project step should be either final project synthesis or deeper PD calibration and vintage robustness work, depending on whether the project prioritizes presentation readiness or model refinement.

## 12. Limitations

- Alternative LGD definitions are proxies and depend on LendingClub field meanings.
- Payment-based LGD may not isolate loss at default because it includes borrower payments before default.
- Net cashflow LGD may double-count depending on how LendingClub reports total payments and recoveries.
- Realized loss proxies are not discounted economic losses.
- Recovery timing is ignored.
- EAD remains funded amount, not balance at default.
- PD calibration drift remains unresolved.
- The model still relies heavily on LendingClub `grade`, `sub_grade`, and `int_rate`.
- This is project-ready analysis, not production LGD, accounting loss, pricing, or capital modeling.

## 13. Recommended Next Steps

1. Decide which LGD definition should be used as the main project baseline.
2. If keeping recovery-based LGD, document that it is the cleanest conditional-default severity measure because it focuses on recoveries relative to EAD for defaulted loans.
3. If adding sensitivity scenarios, carry multiple EL scenarios into the final project summary.
4. Revisit PD calibration drift, especially by vintage.
5. Consider a borrower-only Expected Loss sensitivity excluding LendingClub `grade`, `sub_grade`, and `int_rate`.
6. Create a final project summary tying together PD, LGD, EAD, Expected Loss, limitations, and recommendations.
7. Optionally add stress scenarios by increasing PD, LGD, or both.

## 14. Final Milestone 8 Conclusion

Milestone 8 tested LGD definition sensitivity and realized loss proxy alignment. The milestone clarifies how much Expected Loss depends on the LGD assumption: the framework is stable under gross and net recovery LGD definitions, but materially lower under principal recovery and payment-inclusive definitions.

The project now has a stronger understanding of the robustness and limitations of the preliminary Expected Loss framework. The framework remains project-ready, but not production-ready.
