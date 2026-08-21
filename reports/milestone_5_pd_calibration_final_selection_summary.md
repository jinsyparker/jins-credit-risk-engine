# Milestone 5 Summary: PD Calibration and Final Model Selection

## 1. Objective

Milestone 5 focuses on calibration and final Probability of Default model selection.

This matters because the PD model will later feed Expected Loss. Expected Loss uses PD as a numeric probability, not just as a ranking score. A model can rank risky borrowers above safer borrowers and still produce probabilities that are too high or too low.

```text
Expected Loss = PD x LGD x EAD
```

The purpose of this milestone is to compare uncalibrated and calibrated PD probabilities, select a final project PD model, and create the model and prediction outputs needed for later LGD, EAD, and Expected Loss work.

## 2. Candidate Model from Milestone 4

The candidate model selected after Milestone 4 was:

Model: **L2 Regularized Logistic Regression**

Feature Set: **Feature Set A: Full Risk/Pricing Model**

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

This model was selected because it had strong ranking performance, good calibration, strong risk decile separation, stable time-validation results, and high interpretability compared with tree-based alternatives.

## 3. Calibration Methods Compared

Milestone 5 compared three model versions:

- **Uncalibrated L2 Logistic Regression**: uses the logistic regression predicted probabilities directly.
- **Sigmoid / Platt calibrated L2 Logistic Regression**: applies a simple monotonic calibration layer.
- **Isotonic calibrated L2 Logistic Regression**: applies a more flexible non-parametric calibration layer.

Sigmoid calibration is usually less flexible and less likely to overfit. Isotonic calibration can improve calibration, but it may overfit if the calibration data is limited, noisy, or unstable over time.

## 4. Test-Set Calibration and Performance Results

Source: `reports/tables/pd_calibration_model_comparison_v1.csv`

| model_version | ROC-AUC | PR-AUC / Average Precision | Brier Score | Log Loss | Mean Predicted PD | Actual Default Rate | Difference Actual Minus Predicted | Lowest Decile Default Rate | Highest Decile Default Rate | Highest/Lowest Decile Ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Isotonic Calibrated L2 Logistic Regression | 0.7083 | 0.3652 | 0.1454 | 0.4550 | 0.1996 | 0.1997 | 0.0001 | 0.0421 | 0.4523 | 10.7425 |
| Uncalibrated L2 Logistic Regression | 0.7084 | 0.3689 | 0.1455 | 0.4553 | 0.1997 | 0.1997 | -0.0001 | 0.0421 | 0.4467 | 10.6081 |
| Sigmoid Calibrated L2 Logistic Regression | 0.7084 | 0.3689 | 0.1455 | 0.4553 | 0.1996 | 0.1997 | 0.0001 | 0.0421 | 0.4467 | 10.6081 |

The best ROC-AUC is from **Uncalibrated L2 Logistic Regression** and **Sigmoid Calibrated L2 Logistic Regression**, both at **0.7084**.

The best PR-AUC / Average Precision is also from **Uncalibrated L2 Logistic Regression** and **Sigmoid Calibrated L2 Logistic Regression**, both at **0.3689**.

The lowest Brier Score is from **Isotonic Calibrated L2 Logistic Regression** at **0.1454**, but the improvement over uncalibrated L2 logistic regression is extremely small.

The lowest Log Loss is also from **Isotonic Calibrated L2 Logistic Regression** at **0.4550**, compared with **0.4553** for the uncalibrated model.

All three model versions have mean predicted PD very close to the actual default rate of **0.1997**. Isotonic and sigmoid are slightly below actual, while the uncalibrated model is slightly above actual. The differences are around **0.0001**, which is very small.

Calibration did not materially improve probability quality. Isotonic slightly improves Brier Score and Log Loss, but it reduces PR-AUC from **0.3689** to **0.3652** and slightly reduces ROC-AUC from **0.7084** to **0.7083**.

Calibration did not materially hurt ranking for sigmoid, but it also did not materially improve calibration. Isotonic changes the probabilities more and improves loss metrics slightly, but the improvement is not large enough to outweigh simplicity and overfitting concerns.

## 5. Calibration Bin Analysis

Source: `reports/tables/pd_calibration_bins_v1.csv`

| model_version | lowest-risk bin average predicted PD | lowest-risk bin actual default rate | highest-risk bin average predicted PD | highest-risk bin actual default rate | largest absolute calibration gap |
| --- | --- | --- | --- | --- | --- |
| Uncalibrated L2 Logistic Regression | 0.0425 | 0.0421 | 0.4455 | 0.4467 | 0.0038 |
| Sigmoid Calibrated L2 Logistic Regression | 0.0425 | 0.0421 | 0.4451 | 0.4467 | 0.0040 |
| Isotonic Calibrated L2 Logistic Regression | 0.0422 | 0.0421 | 0.4590 | 0.4523 | 0.0067 |

The uncalibrated model is already well aligned in both low-risk and high-risk bins. In the lowest-risk bin, it predicts **0.0425** versus an actual default rate of **0.0421**. In the highest-risk bin, it predicts **0.4455** versus an actual default rate of **0.4467**.

Sigmoid calibration is very similar to the uncalibrated model. It slightly underpredicts in the highest-risk bin, with predicted PD of **0.4451** versus actual default rate of **0.4467**.

Isotonic calibration has the largest absolute bin gap at **0.0067**, and this occurs in the highest-risk bin. It predicts **0.4590** while the actual default rate is **0.4523**, meaning it overpredicts risk in that bin.

The most reliable probability alignment by calibration bins appears to be the **Uncalibrated L2 Logistic Regression**. It has the smallest largest absolute calibration gap and keeps the high-risk bin close to actual performance.

## 6. Risk Decile Results

Source: `reports/tables/pd_calibration_deciles_v1.csv`

| model_version | lowest decile default rate | highest decile default rate | highest/lowest decile ratio | default rates increase smoothly |
| --- | --- | --- | --- | --- |
| Isotonic Calibrated L2 Logistic Regression | 0.0421 | 0.4523 | 10.7425 | Yes |
| Sigmoid Calibrated L2 Logistic Regression | 0.0421 | 0.4467 | 10.6081 | Yes |
| Uncalibrated L2 Logistic Regression | 0.0421 | 0.4467 | 10.6081 | Yes |

All three model versions separate low-risk and high-risk loans clearly. Default rates increase smoothly across deciles for all versions.

Isotonic calibration has the strongest decile ratio at **10.7425**, compared with **10.6081** for both uncalibrated and sigmoid versions. However, the difference is small and should not by itself determine final model selection.

Calibration did not materially change the risk ranking. The uncalibrated and sigmoid versions have identical decile separation, and isotonic is only slightly stronger.

The chosen final model is useful for portfolio risk bands because the highest-risk decile defaults at more than **10x** the rate of the lowest-risk decile.

## 7. Time-Based Calibration Validation

Source: `reports/tables/pd_calibration_time_validation_v1.csv`

| model_version | time ROC-AUC | time PR-AUC / Average Precision | time Brier Score | time Log Loss | time Mean Predicted PD | time Actual Default Rate | time Difference Actual Minus Predicted | time Decile Ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Isotonic Calibrated L2 Logistic Regression | 0.6952 | 0.3650 | 0.1578 | 0.4854 | 0.1937 | 0.2182 | 0.0245 | 9.7726 |
| Sigmoid Calibrated L2 Logistic Regression | 0.6953 | 0.3681 | 0.1579 | 0.4874 | 0.1941 | 0.2182 | 0.0241 | 9.7700 |
| Uncalibrated L2 Logistic Regression | 0.6953 | 0.3681 | 0.1579 | 0.4875 | 0.1937 | 0.2182 | 0.0245 | 9.7700 |

The best time ROC-AUC is from **Sigmoid Calibrated L2 Logistic Regression** and **Uncalibrated L2 Logistic Regression**, both at **0.6953**.

The best time PR-AUC is also from **Sigmoid Calibrated L2 Logistic Regression** and **Uncalibrated L2 Logistic Regression**, both at **0.3681**.

The best time Brier Score is from **Isotonic Calibrated L2 Logistic Regression** at **0.1578**, but the improvement versus uncalibrated L2 logistic regression at **0.1579** is very small.

All three methods underpredict the actual default rate on newer loans. The actual default rate is **0.2182**, while mean predicted PD is about **0.1937** to **0.1941**. This means the time-period calibration issue is larger than the test-set calibration issue.

Time validation does not change the final recommendation. Isotonic slightly improves Brier Score and Log Loss, but it has lower PR-AUC and does not fix the time-period underprediction. The uncalibrated model remains simple, stable, and competitive.

## 8. Final Model Selection

Source: `reports/tables/pd_final_model_selection_v1.csv`

### Final Selected PD Model

Model version: **Uncalibrated L2 Logistic Regression**  
Calibration method: **None / uncalibrated**  
Feature set: **Feature Set A: Full Risk/Pricing Model**  
Reason: **Uncalibrated L2 logistic regression is retained because calibration did not materially improve probability quality.**

The model was selected because the uncalibrated probabilities were already well aligned on the random test set, calibration did not materially improve Brier Score or Log Loss, and sigmoid calibration produced almost identical performance. Isotonic calibration slightly improved Brier Score and Log Loss, but the improvement was very small and came with lower PR-AUC and higher flexibility.

The other calibration methods were not selected because:

- **Sigmoid calibration** did not materially improve Brier Score, Log Loss, ROC-AUC, PR-AUC, or decile separation.
- **Isotonic calibration** slightly improved Brier Score and Log Loss, but it reduced PR-AUC from **0.3689** to **0.3652** and had a larger largest calibration-bin gap in the highest-risk bin.

The final choice prioritizes simplicity, stability, interpretability, and sufficient calibration rather than chasing a tiny test-set Brier Score improvement.

The final PD model is suitable to move into LGD, EAD, and Expected Loss preparation for this project. It is not production-ready and should continue to be monitored, especially for time-based calibration drift.

## 9. Final PD Outputs Created

The following outputs were created:

- `models/final_pd_model_v1.pkl`: saved final PD model object.
- `data/processed/final_pd_test_predictions_v1.csv`: out-of-sample test-set predictions used to evaluate PD quality.
- `data/processed/loans_with_pd_v1.csv`: full cleaned dataset scored with predicted PD and PD risk decile.

The test prediction file is the cleaner evaluation artifact because it is based on the held-out test set.

The full scored dataset contains predicted PD for all cleaned loans and can support LGD, EAD, and Expected Loss preparation later. However, some full-dataset predictions are in-sample because the model was trained and calibrated using portions of the same dataset. These predictions should be used carefully for analysis and project preparation, not as a pure out-of-sample validation result.

## 10. Where the Final PD Model May Still Be Wrong

The final PD model still relies on LendingClub `grade`, `sub_grade`, and `int_rate`. This was intentional because Feature Set A was selected, but it means the model depends partly on LendingClub's own risk assessment and pricing.

The model is based only on accepted LendingClub loans. It may not generalize to rejected applicants, a bank's current applicant population, or a future macroeconomic environment.

Calibration can shift over time. In time validation, the actual default rate is **0.2182**, while mean predicted PD is only about **0.1937** for the selected uncalibrated model. This is the most important remaining concern from Milestone 5.

Logistic regression may miss nonlinear interactions. It is interpretable and stable, but it may not capture more complex risk patterns that tree-based or gradient boosting models could detect.

Full-dataset scored predictions are not fully out-of-sample. They are useful for preparing the next project stage, but they should not be treated as final validation evidence.

Calibration results are project-level evidence, not production validation. A production PD model would require stronger monitoring, out-of-time validation, governance, and possibly external validation.

## 11. Final Milestone 5 Conclusion

The PD model is finalized for project use, but it is not production-ready.

Calibration did **not** materially improve the PD model. The uncalibrated L2 logistic regression model already had strong calibration on the test set, with mean predicted PD very close to the actual default rate.

The selected calibration method is **no additional calibration**. The final selected model is **Uncalibrated L2 Logistic Regression using Feature Set A**.

The final PD model is ready to support LGD, EAD, and Expected Loss work for this project. It should still be monitored for calibration drift, especially over time, because the time-validation results show underprediction on newer loans.

The next milestone should begin LGD and EAD preparation while preserving the PD outputs from Milestone 5.

## 12. Recommended Next Milestone

The recommended next milestone is:

```text
Milestone 6: LGD and EAD Preparation
```

The next stage should:

- use defaulted loans to estimate Loss Given Default
- use funded amount or outstanding exposure as the first EAD proxy
- combine final PD with LGD and EAD
- prepare for Expected Loss calculations

The final PD model outputs from Milestone 5 will be used in later Expected Loss work.
