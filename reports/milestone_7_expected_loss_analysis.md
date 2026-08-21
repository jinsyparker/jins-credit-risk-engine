# Milestone 7: Expected Loss Analysis and Portfolio Risk Decomposition

## 1. Objective

Milestone 7 analyzes preliminary Expected Loss using:

Expected Loss = PD x LGD x EAD

PD comes from the final Milestone 5 model: uncalibrated L2 Logistic Regression using Feature Set A. The final PD column is `predicted_pd`. LGD and EAD come from Milestone 6, where `ead_proxy = funded_amnt` and `lgd_estimate` is the portfolio-average LGD from defaulted loans, approximately 0.9247 in the combined dataset.

The purpose of this milestone is to decompose Expected Loss across portfolio segments, risk bands, loan size, and PD/EAD drivers. This is portfolio risk analysis, not production capital, accounting, or pricing measurement.

## 2. Inputs and Outputs

Inputs reviewed:

- `data/processed/loans_with_pd_lgd_ead_v1.csv`
- Milestone 7 expected loss segment output files in `data/processed/`
- `notebooks/09_expected_loss_analysis.ipynb`

Outputs reviewed:

| file | rows | columns |
| --- | --- | --- |
| loans_with_pd_lgd_ead_v1.csv | 1,345,350 | 158 |
| expected_loss_by_grade_v1.csv | 7 | 13 |
| expected_loss_by_sub_grade_v1.csv | 35 | 13 |
| expected_loss_by_term_v1.csv | 2 | 13 |
| expected_loss_by_purpose_v1.csv | 14 | 13 |
| expected_loss_by_issue_year_v1.csv | 12 | 13 |
| expected_loss_by_pd_decile_v1.csv | 10 | 14 |
| expected_loss_top_concentration_v1.csv | 4 | 10 |
| expected_loss_pd_ead_matrix_v1.csv | 16 | 9 |

## 3. Portfolio-Level Expected Loss Summary

| metric | value |
| --- | --- |
| Loan count | 1,345,350 |
| Total EAD | $19,388,585,275.00 |
| Mean EAD | $14,411.55 |
| Median EAD | $12,000.00 |
| Total preliminary Expected Loss | $3,862,623,502.47 |
| Mean preliminary Expected Loss | $2,871.09 |
| Median preliminary Expected Loss | $1,782.36 |
| Expected Loss rate | 19.92% |
| Mean predicted PD | 0.1997 |
| Median predicted PD | 0.1787 |
| Mean LGD estimate | 0.9247 |
| Realized default rate | 19.96% |

The portfolio has 1,345,350 loans and total EAD of $19,388,585,275.00. Preliminary Expected Loss totals $3,862,623,502.47, equal to an Expected Loss rate of 19.92%. Because LGD is currently constant across loans, this portfolio-level Expected Loss is mainly driven by the final PD estimates and funded amount exposure.

## 4. Expected Loss by Grade

| grade | loan_count | realized_default_rate | total_ead | total_expected_loss | expected_loss_rate | mean_predicted_pd | mean_lgd_estimate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A | 235,095 | 6.04% | $3,263,735,050.00 | $184,528,056.64 | 5.65% | 0.0604 | 0.9247 |
| B | 392,748 | 13.39% | $5,195,857,925.00 | $659,333,895.19 | 12.69% | 0.1336 | 0.9247 |
| C | 381,694 | 22.44% | $5,413,717,400.00 | $1,166,734,030.75 | 21.55% | 0.2240 | 0.9247 |
| D | 200,966 | 30.39% | $3,068,057,125.00 | $897,613,439.87 | 29.26% | 0.3047 | 0.9247 |
| E | 93,656 | 38.48% | $1,648,265,625.00 | $606,083,840.35 | 36.77% | 0.3865 | 0.9247 |
| F | 32,059 | 45.20% | $611,075,025.00 | $260,557,662.87 | 42.64% | 0.4519 | 0.9247 |
| G | 9,132 | 49.93% | $187,877,125.00 | $87,772,576.81 | 46.72% | 0.5015 | 0.9247 |

Grade C contributes the most total Expected Loss at $1,166,734,030.75, while grade G has the highest Expected Loss rate at 46.72%. Expected Loss rate increases as credit grade worsens, from 5.65% for grade A to 46.72% for grade G.

Total Expected Loss and Expected Loss rate answer different questions. Total Expected Loss reflects both risk and exposure volume, while Expected Loss rate is a cleaner measure of risk intensity per dollar of EAD.

## 5. Expected Loss by Sub-Grade

Top sub-grades by total Expected Loss:

| sub_grade | loan_count | total_ead | total_expected_loss | expected_loss_rate | mean_predicted_pd |
| --- | --- | --- | --- | --- | --- |
| C4 | 74,422 | $1,105,582,825.00 | $264,053,658.81 | 23.88% | 0.2498 |
| C5 | 67,561 | $1,002,882,300.00 | $249,844,222.27 | 24.91% | 0.2597 |
| C3 | 75,000 | $1,075,043,525.00 | $230,748,361.50 | 21.46% | 0.2241 |
| C2 | 79,215 | $1,082,660,275.00 | $215,128,595.57 | 19.87% | 0.2071 |
| C1 | 85,496 | $1,147,548,475.00 | $206,959,192.60 | 18.03% | 0.1889 |
| D1 | 51,323 | $752,555,300.00 | $203,390,984.10 | 27.03% | 0.2821 |
| D2 | 44,851 | $663,380,075.00 | $188,311,377.37 | 28.39% | 0.2962 |
| D3 | 39,322 | $597,286,250.00 | $176,388,646.15 | 29.53% | 0.3083 |

Highest-risk sub-grades by Expected Loss rate:

| sub_grade | loan_count | total_ead | total_expected_loss | expected_loss_rate | mean_predicted_pd |
| --- | --- | --- | --- | --- | --- |
| G5 | 1,110 | $23,538,100.00 | $11,171,686.79 | 47.46% | 0.5104 |
| G1 | 2,997 | $60,821,675.00 | $28,515,756.96 | 46.88% | 0.5028 |
| G3 | 1,614 | $33,959,575.00 | $15,808,945.02 | 46.55% | 0.5013 |
| G2 | 2,131 | $42,556,950.00 | $19,787,354.09 | 46.50% | 0.4978 |
| G4 | 1,280 | $27,000,825.00 | $12,488,833.95 | 46.25% | 0.4969 |
| F4 | 4,859 | $94,021,700.00 | $41,517,693.07 | 44.16% | 0.4700 |
| F5 | 3,944 | $79,640,750.00 | $35,115,392.75 | 44.09% | 0.4718 |
| F2 | 7,198 | $137,709,825.00 | $59,495,055.04 | 43.20% | 0.4591 |

The highest total Expected Loss sub-grades are concentrated in large, middle-to-weaker risk bands where both volume and risk are meaningful. The highest Expected Loss rates occur in the weakest sub-grades. The pattern is near-monotonic across sub-grades, which is consistent with the PD model relying on LendingClub grade, sub-grade, and interest rate. Higher total Expected Loss should not be read as pure risk because it also reflects exposure volume.

## 6. Expected Loss by Term

| term | loan_count | total_ead | total_expected_loss | expected_loss_rate | mean_predicted_pd | mean_ead |
| --- | --- | --- | --- | --- | --- | --- |
| 36.0 | 1,020,768 | $12,804,486,175.00 | $1,873,145,006.87 | 14.63% | 0.1600 | $12,543.97 |
| 60.0 | 324,582 | $6,584,099,100.00 | $1,989,478,495.60 | 30.22% | 0.3246 | $20,284.86 |

The 60-month term contributes more total Expected Loss at $1,989,478,495.60. The 60-month term has the higher Expected Loss rate at 30.22%. The 60-month loans have both higher mean predicted PD and higher mean EAD than 36-month loans, so their Expected Loss is driven by both risk and loan size.

## 7. Expected Loss by Purpose

Top purposes by total Expected Loss:

| purpose | loan_count | total_ead | total_expected_loss | expected_loss_rate | mean_predicted_pd |
| --- | --- | --- | --- | --- | --- |
| debt_consolidation | 780,342 | $11,880,395,625.00 | $2,498,777,975.60 | 21.03% | 0.2117 |
| credit_card | 295,285 | $4,372,026,350.00 | $733,688,639.29 | 16.78% | 0.1696 |
| home_improvement | 87,507 | $1,236,808,100.00 | $223,704,666.07 | 18.09% | 0.1758 |
| other | 77,877 | $764,771,775.00 | $162,497,975.83 | 21.25% | 0.2108 |
| major_purchase | 29,427 | $347,952,700.00 | $68,659,235.04 | 19.73% | 0.1865 |
| small_business | 15,416 | $240,101,250.00 | $68,046,409.68 | 28.34% | 0.2916 |
| medical | 15,556 | $139,923,475.00 | $30,181,229.99 | 21.57% | 0.2141 |
| house | 7,254 | $111,572,125.00 | $23,954,005.16 | 21.47% | 0.2220 |

Highest purposes by Expected Loss rate:

| purpose | loan_count | total_ead | total_expected_loss | expected_loss_rate | mean_predicted_pd |
| --- | --- | --- | --- | --- | --- |
| small_business | 15,416 | $240,101,250.00 | $68,046,409.68 | 28.34% | 0.2916 |
| moving | 9,480 | $74,462,025.00 | $16,915,784.28 | 22.72% | 0.2315 |
| renewable_energy | 933 | $9,325,600.00 | $2,067,254.78 | 22.17% | 0.2215 |
| medical | 15,556 | $139,923,475.00 | $30,181,229.99 | 21.57% | 0.2141 |
| house | 7,254 | $111,572,125.00 | $23,954,005.16 | 21.47% | 0.2220 |
| other | 77,877 | $764,771,775.00 | $162,497,975.83 | 21.25% | 0.2108 |
| debt_consolidation | 780,342 | $11,880,395,625.00 | $2,498,777,975.60 | 21.03% | 0.2117 |
| major_purchase | 29,427 | $347,952,700.00 | $68,659,235.04 | 19.73% | 0.1865 |

The purpose with the largest total Expected Loss is `debt_consolidation` at $2,498,777,975.60. The highest Expected Loss rate appears in `small_business` at 28.34%. Large categories such as debt consolidation dominate total Expected Loss because they combine substantial exposure with meaningful credit risk. Smaller categories should be interpreted cautiously because their rates can be more sensitive to sample size.

## 8. Expected Loss by Issue Year

| issue_year | loan_count | realized_default_rate | total_ead | total_expected_loss | expected_loss_rate | mean_predicted_pd |
| --- | --- | --- | --- | --- | --- | --- |
| 2007.0 | 251 | 17.93% | $2,152,175.00 | $359,588.82 | 16.71% | 0.1608 |
| 2008.0 | 1,562 | 15.81% | $13,457,075.00 | $2,106,189.21 | 15.65% | 0.1553 |
| 2009.0 | 4,716 | 12.60% | $46,324,425.00 | $7,092,003.03 | 15.31% | 0.1553 |
| 2010.0 | 11,536 | 12.89% | $116,706,400.00 | $20,515,907.45 | 17.58% | 0.1759 |
| 2011.0 | 21,721 | 15.18% | $257,363,650.00 | $51,906,912.63 | 20.17% | 0.1862 |
| 2012.0 | 53,367 | 16.20% | $717,942,625.00 | $137,942,881.11 | 19.21% | 0.1794 |
| 2013.0 | 134,804 | 15.60% | $1,982,607,275.00 | $391,600,656.57 | 19.75% | 0.1988 |
| 2014.0 | 223,103 | 18.45% | $3,253,489,500.00 | $668,455,225.70 | 20.55% | 0.2081 |
| 2015.0 | 375,546 | 20.19% | $5,498,601,150.00 | $1,096,989,763.40 | 19.95% | 0.2022 |
| 2016.0 | 293,105 | 23.29% | $4,240,361,600.00 | $831,221,683.20 | 19.60% | 0.1981 |
| 2017.0 | 169,321 | 23.13% | $2,421,502,475.00 | $494,840,950.26 | 20.44% | 0.2018 |
| 2018.0 | 56,318 | 15.76% | $838,076,925.00 | $159,591,741.11 | 19.04% | 0.1884 |

Expected Loss rate varies by vintage. The highest issue-year Expected Loss rate is 20.55% in 2014, while the lowest is 15.31% in 2009. The issue-year view should be interpreted alongside the earlier PD validation caveat: time validation showed calibration drift and underprediction on newer loans, so vintage-level Expected Loss may inherit PD calibration issues.

## 9. PD Decile Analysis

| pd_decile | loan_count | mean_predicted_pd | realized_default_rate | total_ead | total_expected_loss | expected_loss_rate | share_of_total_expected_loss | cumulative_share_of_total_expected_loss |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1.0 | 134,535 | 0.0424 | 4.25% | $1,832,126,975.00 | $71,682,920.16 | 3.91% | 1.86% | 1.86% |
| 2.0 | 134,535 | 0.0764 | 7.70% | $1,779,778,200.00 | $125,428,436.87 | 7.05% | 3.25% | 5.10% |
| 3.0 | 134,535 | 0.1058 | 10.52% | $1,721,490,025.00 | $168,344,101.75 | 9.78% | 4.36% | 9.46% |
| 4.0 | 134,535 | 0.1339 | 13.21% | $1,725,148,900.00 | $213,553,874.09 | 12.38% | 5.53% | 14.99% |
| 5.0 | 134,535 | 0.1632 | 16.35% | $1,750,654,600.00 | $264,283,539.70 | 15.10% | 6.84% | 21.83% |
| 6.0 | 134,535 | 0.1950 | 19.58% | $1,792,173,825.00 | $323,295,928.66 | 18.04% | 8.37% | 30.20% |
| 7.0 | 134,535 | 0.2306 | 22.97% | $1,876,739,750.00 | $400,448,904.42 | 21.34% | 10.37% | 40.57% |
| 8.0 | 134,535 | 0.2730 | 27.07% | $2,017,046,000.00 | $509,817,687.57 | 25.28% | 13.20% | 53.77% |
| 9.0 | 134,535 | 0.3312 | 33.06% | $2,254,311,875.00 | $692,333,373.50 | 30.71% | 17.92% | 71.69% |
| 10.0 | 134,535 | 0.4456 | 44.93% | $2,639,115,125.00 | $1,093,434,735.74 | 41.43% | 28.31% | 100.00% |

Expected Loss rate increases across PD deciles, from 3.91% in decile 1 to 41.43% in decile 10. Realized default rate also rises from 4.25% to 44.93%. The highest PD decile accounts for 28.31% of total Expected Loss, and the top two PD deciles together account for 46.23%. This shows that the PD ranking remains useful for Expected Loss prioritization.

## 10. Loan-Level Expected Loss Concentration

| top_group | loan_count | share_of_loans | total_expected_loss | share_of_total_expected_loss | total_ead | share_of_total_ead | mean_predicted_pd | mean_ead | mean_expected_loss |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| top_1pct_loans_by_expected_loss | 13,454 | 1.00% | $206,385,813.29 | 5.34% | $447,628,550.00 | 2.31% | 0.5026 | $33,271.04 | $15,340.11 |
| top_5pct_loans_by_expected_loss | 67,268 | 5.00% | $787,059,997.86 | 20.38% | $2,026,850,025.00 | 10.45% | 0.4282 | $30,130.97 | $11,700.36 |
| top_10pct_loans_by_expected_loss | 134,535 | 10.00% | $1,319,202,883.65 | 34.15% | $3,737,453,500.00 | 19.28% | 0.3926 | $27,780.53 | $9,805.65 |
| top_20pct_loans_by_expected_loss | 269,070 | 20.00% | $2,081,276,990.48 | 53.88% | $6,634,673,675.00 | 34.22% | 0.3517 | $24,657.80 | $7,735.08 |

Expected Loss is meaningfully concentrated. The top 10% of loans by loan-level Expected Loss account for 34.15% of total Expected Loss and 19.28% of total EAD. These high-EL loans have higher average PD and larger average EAD than the portfolio overall, so concentration is driven by both probability of default and loan size. This type of concentration view is useful for portfolio monitoring and prioritizing deeper reviews.

## 11. PD and EAD Driver Decomposition

Correlation summary:

| pair | correlation |
| --- | --- |
| predicted_pd vs expected_loss_prelim | 0.7581 |
| ead_proxy vs expected_loss_prelim | 0.7152 |
| predicted_pd vs ead_proxy | 0.2175 |

Top PD quartile x EAD quartile combinations by total Expected Loss:

| predicted_pd_quartile | ead_proxy_quartile | loan_count | mean_predicted_pd | mean_ead | mean_expected_loss | total_expected_loss | share_of_total_expected_loss |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Q4_highest_pd | Q4_highest_ead | 113,643 | 0.3830 | $28,054.10 | $9,933.11 | $1,128,828,729.55 | 29.22% |
| Q4_highest_pd | Q3 | 110,540 | 0.3749 | $16,480.75 | $5,713.58 | $631,579,132.41 | 16.35% |
| Q3 | Q4_highest_ead | 67,257 | 0.2251 | $28,153.45 | $5,860.49 | $394,159,262.90 | 10.20% |
| Q3 | Q3 | 87,156 | 0.2236 | $16,453.26 | $3,402.10 | $296,513,177.41 | 7.68% |
| Q4_highest_pd | Q2 | 61,751 | 0.3596 | $10,613.54 | $3,540.16 | $218,608,289.26 | 5.66% |
| Q2 | Q4_highest_ead | 53,088 | 0.1424 | $27,754.78 | $3,656.14 | $194,096,954.68 | 5.03% |

The highest mean Expected Loss occurs in `Q4_highest_pd` and `Q4_highest_ead`, with mean Expected Loss of $9,933.11. The same combination also contributes the highest total Expected Loss at $1,128,828,729.55, or 29.22% of total Expected Loss.

The correlation between predicted PD and Expected Loss is 0.7581, while the correlation between EAD and Expected Loss is 0.7152. Both are important drivers. Since LGD is constant, cross-sectional variation in Expected Loss mainly comes from predicted PD and EAD.

## 12. Key Findings

- Portfolio preliminary Expected Loss is $3,862,623,502.47, with an Expected Loss rate of 19.92%.
- Grade C contributes the most total Expected Loss, while grade G has the highest Expected Loss rate.
- Expected Loss rates increase across grades and PD deciles, supporting the usefulness of the PD ranking for portfolio risk prioritization.
- The highest PD decile contributes 28.31% of total Expected Loss.
- The top 10% of loans by Expected Loss contribute 34.15% of total Expected Loss.
- Loan-level Expected Loss is driven by both predicted PD and EAD because LGD is currently constant.
- The largest PD x EAD driver cell is `Q4_highest_pd` and `Q4_highest_ead`.

## 13. Limitations

- Expected Loss is preliminary and project-level.
- LGD is constant across loans and based on portfolio-average LGD from defaulted loans.
- EAD is funded amount, not balance at default.
- The PD model relies on LendingClub grade, sub-grade, and interest rate.
- Prior time validation showed PD calibration drift and underprediction on newer loans.
- Expected Loss rate may inherit PD calibration issues.
- Segment results can reflect exposure mix as well as risk.
- Small segments should not be overinterpreted.
- This is not production capital, CECL, IFRS 9, or pricing-ready Expected Loss.

## 14. Recommended Next Steps

1. Add realized loss comparison where possible.
2. Test alternative LGD definitions: gross recovery LGD, net recovery LGD after collection recovery fees, principal-recovery-based LGD, and total-cashflow-based LGD.
3. Consider segment-level LGD only after minimum-count thresholds and validation.
4. Revisit PD calibration drift, especially by issue year.
5. Create a final project summary tying together PD, LGD, EAD, and Expected Loss.
6. Consider stress/scenario analysis by increasing PD, LGD, or both.
7. Consider a borrower-only Expected Loss sensitivity excluding LendingClub grade, sub-grade, and interest rate.

## 15. Final Milestone 7 Conclusion

Milestone 7 successfully decomposed preliminary Expected Loss across the LendingClub portfolio. The project now has loan-level and segment-level Expected Loss views by grade, sub-grade, term, purpose, issue year, PD decile, concentration group, and PD/EAD driver band.

Expected Loss is useful for ranking, aggregation, and portfolio monitoring in this project. The framework remains project-ready but not production-ready because LGD and EAD are simplified and the PD model has known calibration drift over time.
