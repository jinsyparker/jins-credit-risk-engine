# Final Credit Risk Project Review and Defense Notes

## 1. Purpose of This Review

This document pressure-tests the full Credit Risk Project narrative and prepares defense notes for peer review, interviews, academic review, and portfolio presentation.

The goal is to answer five questions:

- Does the story add up?
- Are the modeling choices defensible?
- What are the weak points?
- What questions are likely to come up?
- How should those questions be answered honestly?

This is not another project summary. It is a critical review of the project as a complete analytical credit risk workflow.

## 2. Project Story in One Page

The project starts with LendingClub accepted-loan data and defines a clear binary credit outcome: `Fully Paid = 0`, while `Charged Off` and `Default = 1`. Unresolved loan statuses are excluded so that the target represents loans with resolved performance outcomes. The final cleaned dataset contains 1,345,350 loans, including 268,599 defaulted loans, for an observed default rate of 19.96%.

The first modeling objective is Probability of Default. The project builds and validates logistic regression PD models, compares feature sets, tests borrower-only features, compares model families, and evaluates calibration. Feature Set A, which includes LendingClub `grade`, `sub_grade`, and `int_rate`, is the strongest feature set. The borrower-only Feature Set D still has signal, but is weaker. Tree-based models do not materially outperform logistic regression. Calibration does not materially improve probability quality. The final selected PD model is an uncalibrated L2 Logistic Regression using Feature Set A, saved as `models/final_pd_model_v1.pkl`, with final predictions stored in `predicted_pd`.

The final PD model ranks risk well, but it is not production-ready. The final-selection output reports ROC-AUC of 0.7084, PR-AUC of 0.3689, Brier Score of 0.1455, Log Loss of 0.4553, and a high/low decile default-rate ratio of 10.6081. Time validation is the main concern: for the uncalibrated L2 model, the time-test mean predicted PD is 0.1937 while the actual default rate is 0.2182, an underprediction of 0.0245.

After PD, the project builds the LGD and EAD pieces. EAD is proxied with funded amount. Baseline LGD is estimated only on defaulted loans using `1 - recoveries / funded amount`, clipped to `[0, 1]`. The portfolio-average baseline LGD is 0.9247, with median LGD of 0.9379 and zero recovery share of 31.24%. This LGD is high, but it is transparent and consistent with low observed recoveries relative to funded amount.

The project then calculates preliminary Expected Loss:

```text
expected_loss_prelim = predicted_pd x lgd_estimate x ead_proxy
```

The portfolio has total EAD of $19,388,585,275.00 and total preliminary Expected Loss of $3,862,623,502.47, giving an Expected Loss rate of 19.92%. Because LGD is constant in the main framework, loan-level EL variation is driven mainly by PD and EAD.

Milestone 7 decomposes Expected Loss by grade, sub-grade, term, purpose, issue year, PD decile, loan-level concentration, and PD/EAD quartile cells. Grade C contributes the most total Expected Loss, while grade G has the highest Expected Loss rate. The highest PD decile contributes 28.31% of total Expected Loss, and the top 10% of loans by Expected Loss contribute 34.15%.

Milestone 8 tests LGD sensitivity and realized loss proxy alignment. Recovery-based LGDs are close to the baseline: net recovery fee LGD is 0.9372 and produces total EL of $3,914,882,291.95, only 1.35% above baseline. Payment-inclusive definitions produce much lower EL: total payment LGD produces $1,950,784,167.68, 49.50% below baseline, and net cashflow LGD produces $1,727,361,404.08, 55.28% below baseline. Baseline EL aligns closely with the gross recovery realized loss proxy: $3,862,623,502.47 versus $3,853,836,506.13, a ratio of 1.0023.

The final output is an analytical, project-ready credit risk framework. It is useful for ranking, segmentation, portfolio decomposition, scenario analysis, and explaining the PD x LGD x EAD workflow. It is not a production underwriting, pricing, reserve, or capital model.

## 3. Does the Story Add Up?

| check | assessment |
| --- | --- |
| Target definition vs LGD population | The story is consistent. `default_flag = 1` is used for Charged Off / Default loans, and LGD is estimated on the defaulted-loan population of 268,599 loans. |
| PD output into Expected Loss | The connection is clean. The final PD column is `predicted_pd`, and the combined PD/LGD/EAD dataset has 1,345,350 rows. |
| LGD definition support | The baseline LGD is appropriate for a first conditional-default severity proxy because it uses recoveries relative to funded amount for defaulted loans. |
| EAD proxy support | Funded amount is defensible for an initial EAD proxy because it is available for all loans and transparent, but it is not balance at default. |
| Milestone 7 support | Expected Loss decomposition behaves as expected: EL rate rises by grade and PD decile, and concentration appears in high-PD/high-EAD loans. |
| Milestone 8 support | LGD sensitivity supports the baseline as stable under recovery-based definitions and exposes the impact of payment-inclusive alternatives. |
| Contradictions between reports | No material contradictions were found across the accepted reports and output CSVs. |
| Suspicious metrics needing explanation | Three metrics need careful explanation: baseline LGD is very high, time validation underpredicts newer loans, and baseline EL is close to the gross recovery realized proxy partly because both use related recovery logic. |
| Notebook auditability | The notebooks are structured by milestone, but the saved notebook files do not preserve execution counts or cell outputs. The defensible audit trail is therefore the persisted CSV outputs and accepted reports. |

**Overall story coherence: strong.**

The story is strong because each stage feeds the next stage cleanly: target design supports PD modeling, PD outputs feed the EL dataset, LGD is estimated on defaulted loans, EAD is available for all loans, and Expected Loss decompositions behave in a credit-risk-intuitive way.

The main caveats are not contradictions. They are modeling limitations: Feature Set A relies on LendingClub embedded risk signals, the PD model underpredicts newer loans, LGD/EAD are simplified, and the realized loss proxy comparison is not fully independent validation.

## 4. Strongest Parts of the Project

| strength | why it is defensible |
| --- | --- |
| End-to-end workflow | The project covers the full path from cleaned loan data to PD, LGD, EAD, Expected Loss, decomposition, sensitivity, and final synthesis. |
| Clear target definition | `Fully Paid = 0` and `Charged Off / Default = 1` is transparent and maps naturally to credit default modeling. |
| Feature set comparison | The project does not blindly accept all variables. It compares Feature Set A against weaker variants and borrower-only Feature Set D. |
| Borrower-only sensitivity | Feature Set D shows that borrower/loan fields still have signal, but also quantifies how much predictive power comes from LendingClub grades and pricing fields. |
| Model family comparison | Logistic Regression, L2 Logistic Regression, Random Forest, and Gradient Boosting were compared. Tree models did not materially beat the linear baseline, supporting the simpler final choice. |
| Calibration comparison | The project explicitly tested uncalibrated, sigmoid calibrated, and isotonic calibrated L2 models. Calibration did not materially improve the final model. |
| Time validation | The project did not stop at random split metrics. It identified calibration drift and underprediction on newer loans, which is one of the most important production-readiness concerns. |
| Transparent LGD/EAD setup | Funded amount and recovery-based LGD are simple, auditable, and easy to explain. |
| Expected Loss decomposition | Milestone 7 connects model outputs to portfolio risk: grade, sub-grade, term, purpose, issue year, PD decile, concentration, and PD/EAD driver cells. |
| LGD sensitivity analysis | Milestone 8 tests whether the EL conclusion depends on the LGD definition, which is exactly the right challenge for a simplified LGD framework. |
| Realized proxy comparison | Baseline EL is compared with realized loss proxies. The gross recovery proxy ratio of 1.0023 supports reasonableness while still requiring caveats. |
| Transparent limitations | The reports repeatedly state that the framework is project-ready but not production-ready. This honesty makes the project more defensible. |

## 5. Weakest Parts of the Project

| weakness | issue | seriousness | honest defense | future work |
| --- | --- | --- | --- | --- |
| Reliance on `grade`, `sub_grade`, and `int_rate` | Feature Set A uses LendingClub's embedded risk assessment and pricing. | High for claims of independent underwriting. | The project is transparent about this and includes borrower-only Feature Set D. Feature Set A is acceptable for a project-level portfolio risk model, but not as proof of independently discovered borrower risk. | Add borrower-only EL sensitivity and consider separate models with and without platform risk grades. |
| Borrower-only model is weaker | Feature Set D has ROC-AUC 0.6747 versus 0.7094 for Feature Set A. | Moderate. | It still has signal, but the result honestly shows that platform grades and rates carry important predictive information. | Improve borrower-only features, add macro/vintage variables, and test richer feature engineering. |
| Time validation underprediction | Time-test actual default rate is 0.2182 versus mean predicted PD of 0.1937 for the uncalibrated L2 model. | High for production use. | The project found the issue rather than hiding it. The framework is explicitly not production-ready. | Add vintage calibration, out-of-time monitoring, and recalibration. |
| LGD is very high | Baseline LGD is 0.9247, with 31.24% zero recovery share. | Moderate to high. | It is high but grounded in observed recoveries relative to funded amount for defaulted loans. It is a conservative conditional-default severity proxy. | Use discounted cashflows, recovery timing, and balance at default if available. |
| EAD is funded amount | Funded amount is not actual balance at default. | High for production EL. | It is available for all loans and transparent as a first proxy. The limitation is repeatedly stated. | Build EAD using outstanding balance at default or estimated exposure at default. |
| Constant portfolio-average LGD | The main EL model assigns the same LGD to every loan. | Moderate. | It avoids overfitting thin segment-level LGD estimates and keeps the first EL framework stable. | Introduce segment-level LGD only with minimum default-count thresholds and validation. |
| Recovery seasoning | Newer vintages, especially 2017 and 2018, show higher LGDs. | Moderate. | The report identifies seasoning as a possible explanation rather than treating vintage LGD as final truth. | Add recovery windows, maturity filters, and vintage-specific LGD monitoring. |
| Excluding unresolved loans | Removing unresolved outcomes can bias the sample toward resolved loans. | Moderate. | It is common for supervised default modeling to train on resolved outcomes, but the bias should be acknowledged. | Add censoring-aware methods or performance windows. |
| No external validation | Results are from LendingClub data only. | Moderate. | This is a portfolio project, not a production deployment across institutions. | Validate on a different time period, platform, or held-out cohort. |
| Realized proxy comparison may be partly mechanical | Baseline LGD and gross recovery proxy both rely on recoveries and funded amount. | Moderate. | It is a reasonableness check, not independent validation. The report says this clearly. | Add independent realized loss definitions and cashflow-timing validation. |
| Notebooks saved without execution outputs | Notebook structure exists, but execution counts/outputs are not preserved in the saved notebook files reviewed here. | Low to moderate for presentation auditability. | The generated CSVs and accepted Markdown reports are present and internally consistent. | Re-run notebooks in order and save executed notebooks or add reproducible run logs. |
| Accepted loans only | Rejected applications are not included. | High for underwriting policy claims. | The project models performance among accepted loans, not applicant approval decisions. | Add rejected-applicant data if the goal becomes underwriting approval modeling. |

## 6. Critical Questions and Best Answers

### Data and Target Definition

| # | critical question | best honest answer |
| ---: | --- | --- |
| 1 | Why define default as Charged Off / Default? | Those statuses represent resolved negative credit outcomes in the LendingClub data. They align with the PD target and the LGD population used later. |
| 2 | Why exclude unresolved statuses? | Unresolved statuses do not provide a clean final default/non-default outcome. Excluding them makes the target clearer, though it can introduce resolved-loan sample bias. |
| 3 | Does excluding unresolved statuses introduce bias? | Yes, potentially. The model is trained on resolved outcomes, so it may not fully represent active or censored loans. A production model would need performance windows or censoring-aware methods. |
| 4 | Is LendingClub data representative of real bank portfolios? | Not necessarily. It is marketplace lending data and may differ from bank underwriting, servicing, borrower mix, and macro exposure. The project should be presented as LendingClub portfolio analysis. |
| 5 | Did you handle leakage? | The project explicitly tests the impact of high-risk fields by comparing Feature Set A with borrower-only Feature Set D. However, using `grade`, `sub_grade`, and `int_rate` means the model uses LendingClub embedded risk/pricing information. |
| 6 | Does the target align with the LGD defaulted-loan population? | Yes. The cleaned dataset has 268,599 defaulted loans, and Milestone 6 estimates LGD on `default_flag == 1`, matching the PD target definition. |

### PD Modeling

| # | critical question | best honest answer |
| ---: | --- | --- |
| 7 | Why use logistic regression instead of a more complex model? | Logistic regression is interpretable, stable, and performed competitively. Feature Set A baseline logistic regression had ROC-AUC 0.7094, while tree models did not materially improve the result. |
| 8 | Why did tree models not win? | The strongest predictors include graded and priced risk bands that are already structured. Tree models may not add much when key risk ordering is already captured by features such as grade, sub-grade, and interest rate. |
| 9 | Why select L2 Logistic Regression? | L2 regularization provides stability while preserving logistic regression interpretability. The L2 model had performance nearly identical to the baseline logistic model and became the final candidate for calibration testing. |
| 10 | Why keep LendingClub grade, sub_grade, and interest rate? | They materially improve predictive performance and are useful for portfolio risk analysis. The defense is transparency: the project clearly states that Feature Set A uses embedded platform risk signals. |
| 11 | Are grade and interest rate leakage? | They are not leakage in the narrow sense if they are known at loan origination, but they do embed LendingClub's underwriting and pricing. They should not be presented as independent borrower-only risk discovery. |
| 12 | What did the borrower-only model show? | Feature Set D still had signal, with ROC-AUC 0.6747 and high/low decile default-rate ratio 6.0774, but it was weaker than Feature Set A, which had ROC-AUC 0.7094 and ratio 10.5170. |
| 13 | How strong is the final PD model? | The final selected model reports ROC-AUC 0.7084, PR-AUC 0.3689, Brier Score 0.1455, Log Loss 0.4553, and high/low decile ratio 10.6081. That is useful for ranking, but not enough by itself for production. |
| 14 | What does ROC-AUC mean here? | ROC-AUC measures how well the model ranks defaulted loans above non-defaulted loans across thresholds. A value of 0.7084 indicates meaningful discrimination, though not perfect separation. |
| 15 | What does PR-AUC add? | PR-AUC focuses on precision and recall for the default class. The final PR-AUC is 0.3689, which is useful context because defaults are the event of interest. |
| 16 | Why did calibration not improve the model? | Sigmoid calibration produced essentially the same Brier Score and Log Loss as the uncalibrated L2 model, while isotonic slightly improved Brier and Log Loss but reduced PR-AUC. The improvements were not material. |
| 17 | Why choose the uncalibrated model if calibration was tested? | The uncalibrated L2 model retained strong ranking and probability quality without adding calibration complexity. The final-selection table explicitly states calibration did not materially improve probability quality. |
| 18 | What is the biggest PD model risk? | Time drift. The time-test actual default rate was 0.2182 versus mean predicted PD of 0.1937, meaning the model underpredicted newer loans by 0.0245. |

### Time Validation

| # | critical question | best honest answer |
| ---: | --- | --- |
| 19 | What did time validation show? | It showed performance degradation and underprediction on newer loans. For the uncalibrated L2 model, time-test ROC-AUC was 0.6953 and Brier Score was 0.1579. |
| 20 | Why is underprediction on newer loans important? | Expected Loss depends directly on PD. If newer-loan PDs are understated, portfolio EL can be understated for those vintages. |
| 21 | Would you deploy this model? | No, not as-is. It is project-ready for analysis, but production use would require out-of-time monitoring, recalibration, governance, and stability testing. |
| 22 | How would you fix calibration drift? | Recalibrate by vintage or recent time windows, add monitoring, test macro/time features, use rolling validation, and periodically refit or recalibrate the model. |

### LGD and EAD

| # | critical question | best honest answer |
| ---: | --- | --- |
| 23 | Why estimate LGD only on defaulted loans? | LGD is loss severity conditional on default. Non-defaulted loans do not have observed default loss outcomes in this setup. |
| 24 | Why use funded amount as EAD? | Funded amount is available for every loan and is transparent. It is acceptable as a first proxy, but it is not actual outstanding balance at default. |
| 25 | Why is LGD so high? | Observed recoveries are low relative to funded amount. Baseline mean LGD is 0.9247, median LGD is 0.9379, and zero recovery share is 31.24%. |
| 26 | Why use recoveries divided by funded amount? | It directly measures recovery relative to exposure proxy for defaulted loans. It is simple and auditable, though not a discounted economic loss measure. |
| 27 | Why use portfolio-average LGD instead of segment-level LGD? | Segment-level LGD can be noisy and may overfit. A portfolio-average LGD is stable and transparent for the first EL framework. |
| 28 | What does the LGD sensitivity analysis prove? | It shows the EL framework is stable under recovery-based LGD definitions but highly sensitive to payment-inclusive definitions. Net recovery fee EL is only 1.35% above baseline, while net cashflow EL is 55.28% below baseline. |
| 29 | Why not use total payments as LGD? | Total payments can include pre-default borrower payments, so it may not isolate loss severity at default. It is useful as a sensitivity, not necessarily as the main LGD. |
| 30 | Is the realized loss proxy comparison circular? | Partly. The gross recovery proxy uses related recovery logic, so it is a reasonableness check rather than independent validation. The defense is to be explicit about that limitation. |

### Expected Loss

| # | critical question | best honest answer |
| ---: | --- | --- |
| 31 | What does Expected Loss mean here? | It is preliminary loan-level credit loss under the formula `PD x LGD x EAD`. It is a project analytical metric, not a booked reserve or regulatory capital estimate. |
| 32 | Why is total Expected Loss so high? | The portfolio has total EAD of $19.39B, mean predicted PD of 0.1997, and LGD of 0.9247. Those inputs mechanically produce total EL of $3.86B and an EL rate of 19.92%. |
| 33 | What drives Expected Loss? | Because LGD is constant, cross-sectional EL is driven mainly by PD and EAD. Correlation with EL is 0.7581 for predicted PD and 0.7152 for EAD. |
| 34 | Why does grade C contribute more EL than grade G? | Grade C has much more exposure volume. Grade G has the highest EL rate at 46.72%, but grade C has the largest total EL at $1.17B. |
| 35 | What is the difference between total EL and EL rate? | Total EL measures dollar loss contribution and is affected by portfolio size. EL rate measures risk intensity per dollar of EAD. |
| 36 | How should top-decile concentration be interpreted? | The highest PD decile contributes 28.31% of total EL. This shows risk concentration and prioritization value, not that those loans will all default. |
| 37 | How meaningful is the baseline EL versus realized gross recovery proxy ratio? | It is supportive but not definitive. The ratio is 1.0023, which is close, but the comparison is partly mechanical because both use related recovery-based definitions. |

### Production Readiness

| # | critical question | best honest answer |
| ---: | --- | --- |
| 38 | Is this production-ready? | No. It is project-ready. Production use would require stronger out-of-time validation, recalibration, monitoring, governance, and better LGD/EAD measurement. |
| 39 | What would be needed for production? | Production would require data lineage, leakage controls, monitoring, drift management, model governance, recalibration, challenger models, better EAD, refined LGD, and documentation. |
| 40 | Is this CECL, IFRS 9, or Basel compliant? | No. It is not a CECL, IFRS 9, Basel capital, pricing, or underwriting system. It demonstrates the analytical framework. |
| 41 | What would you improve next? | The highest-priority improvements are a presentation deck, stress scenarios, borrower-only EL sensitivity, PD calibration by vintage, segment-level LGD with thresholds, and better EAD if balance-at-default fields are available. |

## 7. Potential Red Flags and How to Explain Them

| red flag | why it may concern someone | is it actually a problem? | how to explain it | future work |
| --- | --- | --- | --- | --- |
| Feature Set A relies on `grade`, `sub_grade`, and `int_rate` | It may look like the model is using LendingClub's own risk judgment. | It is a limitation for independent underwriting claims, but acceptable for transparent project-level portfolio analysis. | State that Feature Set A is a platform-risk/pricing model, and that borrower-only Feature Set D was tested separately. | Add borrower-only EL sensitivity and present both versions. |
| Borrower-only model was weaker | Reviewers may question whether the model really learned borrower risk. | It is a real limitation, but not a contradiction. | Feature Set D still had signal, but Feature Set A performed better because platform risk/pricing variables are predictive. | Improve borrower-only feature engineering. |
| Tree models did not beat logistic regression | Reviewers may expect complex models to perform better. | Not necessarily a problem. | Key predictors are already strongly ordered. Simpler logistic regression was competitive, interpretable, and stable. | Tune additional models, but keep a simple benchmark. |
| Calibration did not improve the model | Reviewers may ask why calibration was included. | Not a problem. | Testing calibration is the point; the result showed added calibration complexity was not justified. | Revisit calibration by vintage or recent time windows. |
| Time validation showed underprediction | This directly affects Expected Loss reliability on newer loans. | Yes, this is one of the biggest weaknesses. | The project identified the issue and does not claim production readiness. | Add time-based recalibration and monitoring. |
| LGD is very high | A 0.9247 LGD may look extreme. | It is high, but it follows from recoveries relative to funded amount. | Show the recovery evidence: zero recovery share is 31.24%, median LGD is 0.9379, and 75th percentile LGD is 1.0000. | Use discounted recovery cashflows and balance at default. |
| EAD is funded amount | Funded amount is not exposure at default. | Yes, for production. For the project, it is a clear first proxy. | Be explicit that EAD is original funded amount and not balance at default. | Build a true EAD proxy from outstanding balances if available. |
| LGD is constant across loans | It suppresses segment-level severity variation. | It is a simplification, but intentional. | Portfolio-average LGD avoids overfitting noisy segment LGDs in the first framework. | Add segment-level LGD after minimum-count thresholds and validation. |
| Payment-based LGD gives much lower EL | Reviewers may ask why not use the lower number. | It is an important sensitivity, not necessarily a better main definition. | Payment-based LGD may include pre-default payments and may not isolate default severity. | Separate pre-default, default, and post-default cashflows if possible. |
| Baseline EL is close to gross realized loss proxy | It may look too convenient or circular. | It is partly mechanical because both use recovery logic. | Present it as a reasonableness check, not an independent validation. | Add independent cashflow-based and out-of-sample realized loss checks. |
| Project uses accepted loans only | It cannot model rejected applications or approval policy. | Yes, for underwriting policy claims. | The project models credit performance among accepted LendingClub loans. | Add rejected-applicant data for approval or adverse-selection modeling. |
| Notebooks do not preserve execution outputs | Reviewers may want notebook-level audit evidence. | It affects reproducibility presentation more than the results, because CSV outputs exist. | Explain that the accepted reports and persisted outputs are the metric record. | Save executed notebooks or add a reproducible run log. |

## 8. What I Should Emphasize in a Presentation

- Emphasize the end-to-end credit risk workflow, not just model fitting.
- Explain that the project includes target design, PD modeling, validation, model family comparison, calibration testing, LGD/EAD construction, Expected Loss calculation, portfolio decomposition, sensitivity testing, and limitations.
- Make the distinction between ranking performance and production readiness very clear.
- Present the final PD model as useful for risk segmentation, while acknowledging dependence on LendingClub embedded risk fields.
- Use the time-validation result as a strength of honesty: the project found underprediction on newer loans instead of hiding it.
- Emphasize business interpretation: Grade C contributes the most total EL, grade G has the highest EL rate, the highest PD decile contributes 28.31% of EL, and high-PD/high-EAD loans drive concentration.
- Explain why the final framework is transparent and defensible: simple PD x LGD x EAD structure, auditable inputs, and sensitivity tests around LGD.
- Show that the LGD baseline is not arbitrary: recovery-based LGD is close to net recovery fee LGD and aligns with the gross recovery realized proxy ratio of 1.0023.

## 9. What I Should Not Overclaim

- Do not say the model is production-ready.
- Do not say it is a CECL, IFRS 9, or Basel model.
- Do not say the LGD estimate is true discounted economic LGD.
- Do not say the model independently discovers risk if using LendingClub grades and pricing fields.
- Do not say Expected Loss is a booked reserve.
- Do not say payment-based LGD is necessarily better because it produces lower losses.
- Do not say time drift is solved.
- Do not say the model can underwrite rejected applicants, because the data is accepted loans only.
- Do not imply the realized loss proxy comparison is independent proof of accuracy.
- Do not interpret total Expected Loss rankings as pure risk rankings without considering exposure volume.

## 10. Final Defense Position

The right defense is:

This is an end-to-end project-ready credit risk framework. The strongest value is not that every component is production-grade, but that the project demonstrates the full risk modeling workflow: target design, PD modeling, validation, model comparison, calibration testing, LGD/EAD construction, Expected Loss calculation, portfolio decomposition, sensitivity testing, and honest limitations.

The final framework is transparent and empirically reasonable for LendingClub portfolio analysis. The PD model ranks risk well, with a final high/low decile ratio of 10.6081. The Expected Loss framework produces interpretable risk concentrations: the highest PD decile contributes 28.31% of total EL, and the top 10% of loans by EL contribute 34.15%. The recovery-based LGD assumption is severe but defensible, and baseline EL aligns closely with the gross recovery realized proxy.

At the same time, the project should not be defended as production-ready. Production use would require stronger out-of-time validation, recalibration, better EAD, more refined LGD, cashflow timing, monitoring, governance, and validation beyond this LendingClub dataset.

## 11. Recommended Next Steps After This Review

1. Create a presentation deck.
2. Create a Streamlit app only after the narrative and defense are finalized.
3. Add stress testing scenarios.
4. Add borrower-only Expected Loss sensitivity.
5. Improve PD calibration by vintage.
6. Explore segment-level LGD with minimum default-count thresholds.
7. Improve EAD proxy if balance-at-default fields are available.
8. Package the repository with README, environment file, and reproducible run instructions.

## 12. Final Verdict

**Overall quality:** strong for a portfolio or academic credit risk project.

**Story coherence:** strong. The target, PD model, LGD/EAD construction, Expected Loss calculation, decomposition, and sensitivity tests connect logically.

**Suitability:** suitable for a portfolio presentation, academic project, or interview discussion, as long as it is presented as project-ready analysis rather than production credit infrastructure.

**Biggest strengths:** full end-to-end workflow, strong risk-ranking evidence, honest feature-set comparison, model family and calibration testing, time validation, Expected Loss decomposition, and LGD sensitivity.

**Biggest limitations:** reliance on LendingClub embedded risk fields, time-validation underprediction, simplified LGD, funded-amount EAD, constant LGD, and accepted-loan-only data.

**Best next deliverable:** a concise stakeholder presentation deck that tells the project story, shows the key metrics, and proactively addresses the defense points in this document.
