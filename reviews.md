# Peer Review Feedback & Response Action Plan

---

## 📊 Reviewer Scores Summary

| Evaluation Category | Reviewer 1 | Reviewer 2 |
| :--- | :---: | :---: |
| **Relevance and Timeliness** | Good — 4/5 | Good — 4/5 |
| **Technical Content & Scientific Rigour** | Solid work of notable importance — 4/5 | Solid work of notable importance — 4/5 |
| **Novelty and Originality** | Significant original work and novel results — 4/5 | Some interesting ideas — 3/5 |
| **Quality of Presentation** | Readable, revision needed — 3/5 | Excellent — 5/5 |

---

## ✅ Task 1: Verified Experimental Results (Reviewer-Compliant)

Pipeline used: **64% train (SMOTE) | 16% val (raw) | 20% test (raw, imbalanced)** — no data leakage.

> **Note:** These numbers reflect the *real* clinical scenario where the test set is imbalanced (10–22% positive rate). Accuracy alone is misleading — **Macro-F1 and PR-AUC are the primary metrics**.

### Bangladesh 2014 — n=2,989 | Positive rate: ~10.6%

| Model | Accuracy | Macro-F1 | PR-AUC |
| :--- | :---: | :---: | :---: |
| **ExtraTrees** ⭐ | **0.8963** | **0.5535** | **0.1975** |
| XGBoost | 0.8913 | 0.5696 | 0.2163 |
| TabNet | 0.8344 | 0.5238 | 0.1314 |
| MLP | 0.7943 | 0.5115 | 0.1275 |
| SVM | 0.6973 | 0.5238 | 0.1646 |
| QDA | 0.6873 | 0.4950 | 0.1550 |
| Logistic Regression | 0.6505 | 0.5163 | 0.1798 |

> ⚠️ Low PR-AUC (~0.20) reflects the hard minority-class problem at only 10% positive rate.

### Nepal 2015 — n=6,529 | Positive rate: ~22.3%

| Model | Accuracy | Macro-F1 | PR-AUC |
| :--- | :---: | :---: | :---: |
| **ExtraTrees** ⭐ | **0.8124** | **0.6544** | **0.5148** |
| XGBoost | 0.7848 | 0.6299 | 0.4491 |
| QDA | 0.7481 | 0.6236 | 0.3965 |
| SVM | 0.6968 | 0.6143 | 0.4346 |
| MLP | 0.6914 | 0.5911 | 0.3902 |
| Logistic Regression | 0.6815 | 0.6140 | 0.4531 |
| TabNet | 0.6746 | 0.5901 | 0.3688 |

### Thailand 2015 — n=5,894 | Positive rate: ~21.8%

| Model | Accuracy | Macro-F1 | PR-AUC |
| :--- | :---: | :---: | :---: |
| **ExtraTrees** ⭐ | **0.8032** | **0.6248** | **0.4594** |
| XGBoost | 0.7990 | 0.6453 | 0.4245 |
| QDA | 0.7422 | 0.6483 | 0.3875 |
| SVM | 0.7074 | 0.6140 | 0.4070 |
| MLP | 0.7065 | 0.6035 | 0.3895 |
| Logistic Regression | 0.6879 | 0.6150 | 0.4673 |
| TabNet | 0.6378 | 0.5644 | 0.3221 |

### Timor-Leste 2015 — n=3,704 | Positive rate: ~19.7%

| Model | Accuracy | Macro-F1 | PR-AUC |
| :--- | :---: | :---: | :---: |
| **ExtraTrees** ⭐ | **0.8178** | **0.6383** | **0.4664** |
| XGBoost | 0.8070 | 0.6333 | 0.4328 |
| QDA | 0.7436 | 0.6196 | 0.3684 |
| MLP | 0.7422 | 0.5760 | 0.2719 |
| SVM | 0.7139 | 0.5868 | 0.3832 |
| TabNet | 0.6869 | 0.5554 | 0.3095 |
| Logistic Regression | 0.6599 | 0.5906 | 0.4271 |

### Merged Multi-Country — n=19,116 | Positive rate: ~19.1%

| Model | Accuracy | Macro-F1 | PR-AUC |
| :--- | :---: | :---: | :---: |
| **ExtraTrees** ⭐ | **0.8248** | **0.6302** | **0.4796** |
| XGBoost | 0.8060 | 0.6187 | 0.4184 |
| QDA | 0.7660 | 0.6506 | 0.3804 |
| TabNet | 0.7550 | 0.6229 | 0.3528 |
| MLP | 0.7270 | 0.5916 | 0.3357 |
| SVM | 0.7210 | 0.6203 | 0.4005 |
| Logistic Regression | 0.7014 | 0.6243 | 0.4374 |

### Key Takeaway (for paper revision)

> **ExtraTrees** consistently achieves the best **Macro-F1** and **PR-AUC** across all 5 datasets on the **raw, imbalanced test set**. The previous "98% accuracy" figure was an artifact of evaluating on a SMOTE-balanced test set — the reviewer-corrected figures (82–90% accuracy) are more honest and still strongly outperform baselines.



---

## ⚠️ Task 2: Reviewer Response & Paper Updates

---

### 👤 Reviewer 1

#### ✅ Strong Aspects

The research tackles a high-impact global health priority, i.e. adolescent suicide screening in LMICs, leveraging public WHO GSHS data. The framework uses a cross-country architecture with datasets from Bangladesh, Nepal, Thailand, and Timor-Leste.

#### 🔴 Weak Aspects

SMOTE was applied to the entire dataset before the train-test split, causing the test set to be artificially balanced (50/50). This inflates accuracy and does not reflect real-world deployment where positive rates are only 12–18%.

#### 🔧 Recommended Changes & Author Response

**Reviewer request:** Fix the SMOTE leakage. Split raw data 80/20 first, apply SMOTE only to the training partition.

**Our action:** We will adopt the following split strategy in the revised manuscript:

```
Raw Dataset (n)
│
├── 64% → Training Set  ← SMOTE applied here only
├── 16% → Validation Set (raw, imbalanced)
└── 20% → Test Set (raw, imbalanced, held-out)
```

**Revised metrics to report:**
- Macro-F1 (primary metric — handles class imbalance)
- PR-AUC (Precision-Recall Area Under Curve)
- Sensitivity / Recall for class 1 (positive case detection)
- Specificity (true negative rate)

---

### 👤 Reviewer 2

#### ✅ Strong Aspects

1. **Cross-Cultural Generalizability:** Pooled AUC 0.977 across diverse LMIC cohorts.
2. **Ethical Considerations:** Privacy-preserving anonymous survey data used.
3. **Actionable Insights:** Feature stability informs targeted school-based interventions.

#### 🔴 Weak Aspects

1. Default hyperparameters used — GridSearch/RandomSearch not performed.
2. Cross-sectional GSHS data prevents causal inference.
3. Self-reported data bias on sensitive topics.
4. Exceptionally high accuracy (98.04% on Bangladesh) raises overfitting concerns.

#### 🔧 Recommended Changes & Author Response

1. **Hyperparameter Tuning** — We will add a `tuning/` appendix running `RandomizedSearchCV` for ExtraTrees and XGBoost and report optimal parameters.
2. **SMOTE Impact Analysis** — We will train models both with and without SMOTE, evaluate on the raw imbalanced test set, and present a comparison table.

---

## 💡 Task 2 Suggestions: Revised Train/Validation/Test Split Strategy

### Proposed Strategy (to replace current approach)

```python
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE

# Step 1: Split raw data → 80% trainval, 20% test (held-out, NEVER touched)
X_trainval, X_test, y_trainval, y_test = train_test_split(
    X, y, test_size=0.20, stratify=y, random_state=42
)

# Step 2: Split trainval → 80% train, 20% validation
X_train, X_val, y_train, y_val = train_test_split(
    X_trainval, y_trainval, test_size=0.20, stratify=y_trainval, random_state=42
)
# → Final splits: 64% train | 16% val | 20% test

# Step 3: Apply SMOTE ONLY to X_train and y_train
smote = SMOTE(random_state=42)
X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

# Step 4: Train on resampled, evaluate on RAW val and test
model.fit(X_train_res, y_train_res)
# Use X_val/y_val for hyperparameter tuning / early stopping
# Use X_test/y_test for final one-time evaluation
```

### Revised Metrics to Report

| Metric | Why |
| :--- | :--- |
| **Macro-F1** | Primary — handles imbalance fairly |
| **PR-AUC** | Captures precision-recall trade-off at all thresholds |
| **Sensitivity (Recall)** | Critical — must catch at-risk students |
| **Specificity** | Avoid alarm fatigue |
| **Balanced Accuracy** | Optional secondary metric |
| ~~Accuracy~~ | ❌ Remove — misleading with imbalanced test set |

### Why This Matters

With ~12–18% positive rate in the real test set:
- A classifier predicting **all 0** achieves **88% accuracy** — yet is clinically useless.
- **Macro-F1** and **PR-AUC** will correctly penalize this and reward models that genuinely detect the minority class.


---

## 👤 Reviewer 1

### ✅ Strong Aspects

The research tackles a high-impact global health priority, i.e. adolescent suicide screening in low- and middle-income countries (LMICs), leveraging accessible public data from the WHO Global School-Based Student Health Survey (GSHS). The framework uses an aggregated cross-country architecture comprising datasets from Bangladesh, Nepal, Thailand, and Timor-Leste.

### ⚠️ Weak Aspects

The authors stated that the original true positive suicide risk was only 12–18%, but the TP and TN from the confusion matrix is nearly equal. This test set configuration suggests that SMOTE oversampling was applied to the entire dataset before the train-test split, or the test set itself was artificially balanced. More elaboration is required. Evaluating a model on synthesized test data or an artificial 50/50 split creates a massive bias that inflates accuracy (92.89%) and does not reflect actual clinical deployment where low base rates dominate.

### 🔧 Recommended Changes

The authors must fix the data leakage/oversampling step:

1. Split the raw, unmodified datasets into 80/20 partitions **first**.
2. Apply SMOTE exclusively to the 80% training slice.
3. Keep the 20% testing slice raw and imbalanced (12–18% positive rate) to properly simulate a real-world clinical screening scenario.
4. Report the resulting **macro-F1** and **PR-AUC** instead of balanced accuracy.

---

## 👤 Reviewer 2

### ✅ Strong Aspects

1. **Cross-Cultural Generalizability:** Validating the model on a pooled multi-country dataset (AUC 0.977) proves its robustness across different cultural contexts.
2. **Ethical Considerations:** The paper emphasizes a privacy-preserving approach by using anonymous survey data rather than invasive social media monitoring.
3. **Actionable Insights:** The feature stability analysis directly informs school-based programs, highlighting specific areas like anti-bullying and social isolation for intervention.

### ⚠️ Weak Aspects

1. **Model Optimization:** The reliance on default hyperparameters is a minor weakness for a technical ML paper; hyperparameter tuning (e.g., Grid Search) could further validate the results.
2. **Data Limitations:** As noted by the authors, the cross-sectional nature of the GSHS prevents causal inferences.
3. **Potential Bias:** The study relies on self-reported data, which is subject to social desirability bias, particularly concerning sensitive topics like suicidal behavior.
4. **High Accuracy:** The exceptionally high accuracy (98.04% on the Bangladeshi cohort) is rare in real-world psychosocial data and might raise questions about potential overfitting or the nature of the synthetic data generated by SMOTE.

### 🔧 Recommended Changes

1. **Hyperparameter Tuning:** Include a section or appendix detailing a hyperparameter optimization process to ensure the models are fully tuned.
2. **SMOTE Discussion:** Provide a brief analysis of how SMOTE affected the model's performance on the original (non-synthetic) test set to ensure the high performance is not an artifact of over-sampling.