# Milestone 4 Summary: PD Model Family Comparison

## 1. Objective

Milestone 4 compares the baseline logistic regression Probability of Default model against regularized logistic regression and tree-based models.

The goal is not just to maximize ROC-AUC. For credit risk and Expected Loss, the selected PD model should be judged on:

- ROC-AUC
- PR-AUC / Average Precision
- Brier Score
- calibration
- risk decile separation
- time validation
- interpretability
- suitability for Expected Loss

This matters because the selected PD model may later feed:

```text
Expected Loss = PD x LGD x EAD
```

A model with strong ranking but poor probability calibration can still create misleading Expected Loss estimates.

## 2. Models Compared

The following models were actually run in Milestone 4:

- Logistic Regression Baseline
- Regularized Logistic Regression L2
- Random Forest
- Gradient Boosting

The following models were skipped:

- XGBoost: skipped because `xgboost` was not installed in the current environment.
- LightGBM: skipped because `lightgbm` was not installed in the current environment.

They can be added later with:

```bash
pip install xgboost lightgbm
```

## 3. Feature Sets Compared

### Feature Set A: Full Risk/Pricing Model

Feature Set A includes:

- `grade`
- `sub_grade`
- `int_rate`
- borrower variables
- loan variables

This feature set is expected to perform better because it includes LendingClub risk and pricing information. These variables likely summarize part of LendingClub's own underwriting and pricing view.

### Feature Set D: Borrower-Only Model

Feature Set D excludes:

- `grade`
- `sub_grade`
- `int_rate`

This feature set tests whether borrower and loan characteristics alone can predict default. It is more independent from LendingClub's internal risk labels, but it is expected to be less predictive.

## 4. Overall Model Performance

Source: `reports/tables/pd_model_family_comparison_v1.csv`

| feature_set | model_name | ROC-AUC | PR-AUC / Average Precision | Brier Score | Accuracy | Precision | Recall | Highest/Lowest Decile Ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Feature Set A | Logistic Regression Baseline | 0.7094 | 0.3701 | 0.1453 | 0.8019 | 0.5435 | 0.0481 | 10.5170 |
| Feature Set A | Regularized Logistic Regression L2 | 0.7093 | 0.3701 | 0.1453 | 0.8019 | 0.5432 | 0.0474 | 10.5414 |
| Feature Set A | Gradient Boosting | 0.7068 | 0.3700 | 0.1456 | 0.8022 | 0.5684 | 0.0389 | 10.5690 |
| Feature Set A | Random Forest | 0.7050 | 0.3676 | 0.1463 | 0.8008 | 0.6444 | 0.0054 | 10.6109 |
| Feature Set D | Logistic Regression Baseline | 0.6747 | 0.3388 | 0.1495 | 0.8008 | 0.5268 | 0.0244 | 6.0774 |
| Feature Set D | Regularized Logistic Regression L2 | 0.6747 | 0.3388 | 0.1495 | 0.8008 | 0.5266 | 0.0243 | 6.0839 |
| Feature Set D | Gradient Boosting | 0.6732 | 0.3397 | 0.1497 | 0.8011 | 0.5612 | 0.0167 | 6.2710 |
| Feature Set D | Random Forest | 0.6725 | 0.3393 | 0.1504 | 0.8003 | 0.0000 | 0.0000 | 6.0188 |

The best ROC-AUC is from **Feature Set A - Logistic Regression Baseline** at **0.7094**.

The best PR-AUC / Average Precision is from **Feature Set A - Regularized Logistic Regression L2** at **0.3701**. This is only marginally higher than the baseline logistic regression value of **0.3701**.

The best, meaning lowest, Brier Score is from **Feature Set A - Logistic Regression Baseline** at **0.1453**.

Tree-based models did **not** beat logistic regression overall. Gradient Boosting with Feature Set A came close, with ROC-AUC of **0.7068**, PR-AUC of **0.3700**, and Brier Score of **0.1456**, but it did not materially improve on logistic regression.

The best model differs only slightly by metric. On Feature Set A, logistic regression and L2 logistic regression are effectively tied. On Feature Set D, logistic regression has the best ROC-AUC, while Gradient Boosting has the best PR-AUC and decile ratio, but its Brier Score is slightly worse.

Overall, the improvement from tree-based models is small to negative in this milestone.

## 5. Risk Decile Analysis

Source: `reports/tables/pd_model_family_deciles_v1.csv`

| feature_set | model_name | lowest_decile_default_rate | highest_decile_default_rate | highest_lowest_ratio | decile_pattern_assessment |
| --- | --- | --- | --- | --- | --- |
| Feature Set A | Random Forest | 0.0417 | 0.4429 | 10.6109 | Strong |
| Feature Set A | Gradient Boosting | 0.0423 | 0.4466 | 10.5690 | Strong |
| Feature Set A | Regularized Logistic Regression L2 | 0.0426 | 0.4494 | 10.5414 | Strong |
| Feature Set A | Logistic Regression Baseline | 0.0427 | 0.4491 | 10.5170 | Strong |
| Feature Set D | Gradient Boosting | 0.0668 | 0.4188 | 6.2710 | Moderate |
| Feature Set D | Regularized Logistic Regression L2 | 0.0691 | 0.4203 | 6.0839 | Moderate |
| Feature Set D | Logistic Regression Baseline | 0.0692 | 0.4203 | 6.0774 | Moderate |
| Feature Set D | Random Forest | 0.0691 | 0.4156 | 6.0188 | Moderate |

All Feature Set A models show strong risk decile separation. The highest-risk decile defaults at roughly **10.5x** the rate of the lowest-risk decile.

Feature Set D models also separate risk, but less strongly. Their highest/lowest decile ratios are around **6.0x to 6.3x**, which is useful but clearly weaker than Feature Set A.

Random Forest with Feature Set A has the highest decile ratio at **10.6109**, followed by Gradient Boosting at **10.5690**. However, this does not automatically make Random Forest the best PD model because its ROC-AUC, PR-AUC, Brier Score, and recall are weaker than the best logistic regression models.

No model shows an obviously unstable decile pattern in this output. The main distinction is strength: Feature Set A is strong, while Feature Set D is moderate.

Risk decile separation matters because credit risk teams often use PD bands for portfolio monitoring, risk appetite, pricing, cutoff analysis, and Expected Loss segmentation.

## 6. Calibration Analysis

Source figure: `reports/figures/pd_model_family_calibration_comparison_v1.png`

Calibration is assessed using the calibration chart and Brier Scores from the model comparison table.

The best Brier Score is **0.1453** for **Feature Set A - Logistic Regression Baseline**. Regularized Logistic Regression L2 is almost identical at **0.1453**. Gradient Boosting with Feature Set A is slightly worse at **0.1456**, and Random Forest with Feature Set A is worse at **0.1463**.

For Feature Set D, Brier Scores are weaker:

- Logistic Regression Baseline: **0.1495**
- Regularized Logistic Regression L2: **0.1495**
- Gradient Boosting: **0.1497**
- Random Forest: **0.1504**

The tree-based models do not show better probability accuracy in this milestone. Random Forest in particular has weaker Brier Scores and very low recall at the 0.5 threshold. Tree models may still be useful later, but they may need probability calibration before being used for Expected Loss.

Brier Score and calibration are more important than raw classification accuracy here because PD is a probability input. Accuracy near **0.80** appears similar across models, but accuracy at a fixed 0.5 threshold does not tell us whether predicted PDs are numerically reliable.

Based on this milestone, calibration appears strongest for Feature Set A logistic regression models.

## 7. Time-Based Validation Analysis

Source: `reports/tables/pd_model_family_time_validation_v1.csv`

| feature_set | model_name | time ROC-AUC | time PR-AUC | time Brier Score | time decile ratio |
| --- | --- | --- | --- | --- | --- |
| Feature Set A | Logistic Regression Baseline | 0.6953 | 0.3680 | 0.1579 | 9.7283 |
| Feature Set A | Regularized Logistic Regression L2 | 0.6953 | 0.3680 | 0.1579 | 9.7058 |
| Feature Set A | Gradient Boosting | 0.6924 | 0.3682 | 0.1578 | 9.7569 |
| Feature Set A | Random Forest | 0.6909 | 0.3676 | 0.1582 | 9.6277 |
| Feature Set D | Logistic Regression Baseline | 0.6621 | 0.3386 | 0.1627 | 5.5863 |
| Feature Set D | Regularized Logistic Regression L2 | 0.6621 | 0.3386 | 0.1628 | 5.5854 |
| Feature Set D | Random Forest | 0.6589 | 0.3398 | 0.1630 | 5.7657 |
| Feature Set D | Gradient Boosting | 0.6553 | 0.3351 | 0.1632 | 5.8002 |

Time validation was performed. The notebook trained on older loans and tested on newer loans. The time-validation file shows **1,062,380** training rows, **282,970** test rows, and a time-test default rate of **21.82%**.

The best time ROC-AUC is **0.6953** from **Feature Set A - Logistic Regression Baseline**. Regularized Logistic Regression L2 is almost tied at **0.6953**.

The best time PR-AUC is **0.3682** from **Feature Set A - Gradient Boosting**. The difference versus logistic regression is very small.

The best time Brier Score is **0.1578** from **Feature Set A - Gradient Boosting**, again only slightly better than logistic regression at **0.1579**.

Performance drops compared with random train-test split results. For example, Feature Set A Logistic Regression Baseline drops from random ROC-AUC **0.7094** to time ROC-AUC **0.6953**, and Brier Score worsens from **0.1453** to **0.1579**.

The best random-split model is still one of the best models under time validation. Feature Set A logistic regression remains highly competitive and more interpretable than the tree models.

There is no severe evidence of tree-model overfitting in the saved time-validation table, but tree models also do not produce a meaningful improvement over logistic regression.

Time validation matters because credit risk changes across origination periods. A model that only works on a random split may fail when applied to newer loans.

## 8. Feature Importance Interpretation

Source: `reports/tables/pd_tree_model_feature_importance_v1.csv`

Top Feature Set A Gradient Boosting features:

| feature | importance |
| --- | --- |
| numeric__int_rate | 0.6845 |
| numeric__term | 0.0982 |
| numeric__dti | 0.0473 |
| categorical__home_ownership_MORTGAGE | 0.0281 |
| categorical__home_ownership_RENT | 0.0266 |
| numeric__annual_inc | 0.0238 |
| numeric__loan_amnt | 0.0219 |
| categorical__grade_A | 0.0183 |

Top Feature Set A Random Forest features:

| feature | importance |
| --- | --- |
| numeric__int_rate | 0.2376 |
| categorical__grade_A | 0.1292 |
| numeric__term | 0.1179 |
| categorical__grade_B | 0.0633 |
| categorical__grade_E | 0.0523 |
| categorical__grade_D | 0.0502 |
| categorical__grade_F | 0.0422 |
| numeric__dti | 0.0394 |

Top Feature Set D Gradient Boosting features:

| feature | importance |
| --- | --- |
| numeric__term | 0.4846 |
| numeric__dti | 0.1316 |
| numeric__annual_inc | 0.0832 |
| categorical__home_ownership_MORTGAGE | 0.0665 |
| categorical__home_ownership_RENT | 0.0565 |
| categorical__verification_status_Not Verified | 0.0560 |
| numeric__revol_util | 0.0272 |
| numeric__loan_amnt | 0.0203 |

Top Feature Set D Random Forest features:

| feature | importance |
| --- | --- |
| numeric__term | 0.4268 |
| numeric__dti | 0.1286 |
| categorical__verification_status_Not Verified | 0.0651 |
| numeric__annual_inc | 0.0622 |
| numeric__loan_amnt | 0.0563 |
| categorical__home_ownership_MORTGAGE | 0.0558 |
| categorical__home_ownership_RENT | 0.0480 |
| numeric__revol_util | 0.0341 |

Feature importance confirms that `int_rate` dominates Feature Set A tree models, especially Gradient Boosting where `numeric__int_rate` has importance **0.6845**. Random Forest also relies heavily on `int_rate` and grade indicators.

When `grade`, `sub_grade`, and `int_rate` are removed in Feature Set D, the most important variables become `term`, `dti`, `annual_inc`, `home_ownership`, `verification_status`, `revol_util`, and `loan_amnt`. These are consistent with credit risk intuition.

The tree models rely mainly on LendingClub risk/pricing variables when those variables are available, but borrower characteristics still carry signal in the borrower-only setup.

## 9. Best Candidate PD Model

### Recommended Candidate Model

Model: **Regularized Logistic Regression L2**  
Feature Set: **Feature Set A: Full Risk/Pricing Model**  
Reason: It performs essentially the same as the baseline logistic regression while adding regularization, preserving interpretability, maintaining strong decile separation, and remaining stable in time validation.

### Why this model is preferred

The recommended model is not selected only because of ROC-AUC. Feature Set A Regularized Logistic Regression L2 has:

- ROC-AUC: **0.7093**
- PR-AUC / Average Precision: **0.3701**
- Brier Score: **0.1453**
- Decile ratio: **10.5414**
- Time ROC-AUC: **0.6953**
- Time PR-AUC: **0.3680**
- Time Brier Score: **0.1579**
- Time decile ratio: **9.7058**

It is nearly tied with the unregularized logistic regression baseline on all major metrics. It has the best random PR-AUC by a very small margin and a slightly stronger random decile ratio than the baseline. It also remains simple and explainable.

Gradient Boosting is competitive, especially in time PR-AUC and time Brier Score, but the improvement is very small and does not offset the loss of interpretability at this stage.

### Why other models were not selected

**Logistic Regression Baseline** was not selected as the final recommendation because the L2 version offers similar performance with regularization, which is usually preferable for a candidate model that may later be refined.

**Gradient Boosting** was not selected because it does not materially beat logistic regression on random-split performance. Its Feature Set A ROC-AUC is **0.7068**, below logistic regression, and its Brier Score is slightly worse at **0.1456**.

**Random Forest** was not selected because it has weaker ROC-AUC and Brier Score than logistic regression. For Feature Set A, Random Forest has ROC-AUC **0.7050** and Brier Score **0.1463**. Its recall at 0.5 is also very low at **0.0054**.

**Feature Set D models** were not selected because they are less predictive. The best Feature Set D ROC-AUC is **0.6747**, materially lower than Feature Set A. However, Feature Set D remains useful as a benchmark for borrower-only signal.

**XGBoost and LightGBM** were not selected because they were not installed and were not run in this milestone.

### Important caution

The recommended model is still not final. It needs calibration review, additional time-validation checks, feature review, and possibly comparison against calibrated tree-based models before it is used as the final PD input for Expected Loss.

## 10. Where the Models May Be Wrong

The main weaknesses found in Milestone 4 are:

- Feature Set A relies heavily on LendingClub `grade`, `sub_grade`, and especially `int_rate`. Tree feature importance confirms that `int_rate` dominates the Feature Set A tree models.
- Feature Set D is more independent but less predictive. Its best ROC-AUC is **0.6747**, compared with **0.7094** for the best Feature Set A model.
- Tree-based models did not clearly improve performance. They may still help after tuning, but in this milestone they were not stronger than logistic regression.
- Random Forest appears weak at the 0.5 threshold, with Feature Set A recall of only **0.0054** and Feature Set D precision/recall of **0.0000** at the 0.5 cutoff.
- Time validation shows weaker probability performance. For Feature Set A logistic regression, Brier Score worsens from **0.1453** to **0.1579** on newer loans.
- High ROC-AUC does not guarantee good PD calibration. Calibration must still be reviewed before Expected Loss.
- LendingClub accepted-loans-only data may not generalize to a bank's full applicant population.

The most serious issues are dependence on LendingClub risk/pricing fields and weaker time-validation Brier Scores. Tree-model overfitting is not the main issue in the saved results because the tree models did not outperform logistic regression.

## 11. Final Milestone 4 Conclusion

The model is stronger than the initial baseline, but it is not production-ready.

1. **Did model comparison improve the PD model?**  
   It improved understanding more than raw performance. The comparison showed that regularized logistic regression is a strong candidate and that tree models do not materially beat logistic regression in this version.

2. **Did tree-based models help?**  
   Not materially. Gradient Boosting was competitive, but it did not clearly outperform logistic regression across ROC-AUC, Brier Score, decile separation, time validation, and interpretability.

3. **Which model is the best candidate right now?**  
   Feature Set A with Regularized Logistic Regression L2 is the best candidate because it balances strong performance, stability, interpretability, and suitability for Expected Loss.

4. **Is the PD model ready to feed Expected Loss?**  
   Not yet. It is close enough to move into calibration and final selection, but it should not be treated as final until calibration is reviewed and final PD outputs are prepared.

5. **What still needs to be checked before finalizing PD?**  
   Calibration, time stability, feature overlap, the role of `int_rate`, and whether calibrated tree-based models can improve performance without sacrificing probability quality.

## 12. Recommended Next Steps

The recommended next milestone is:

```text
Milestone 5: PD Calibration and Final PD Model Selection
```

Milestone 5 should include:

- calibrating the best candidate model if needed
- comparing calibrated versus uncalibrated probabilities
- finalizing the PD model
- saving final PD predictions
- preparing outputs needed for LGD, EAD, and Expected Loss

Additional useful checks include:

- hyperparameter tuning for Gradient Boosting and Random Forest
- optional XGBoost and LightGBM comparison after installation
- more detailed time-validation by issue year
- simplified feature set testing if independence from LendingClub risk labels is important

The next step should focus on making the selected PD model reliable as a probability model, not only as a risk-ranking model.
