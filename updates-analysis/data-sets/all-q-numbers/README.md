# All Q Numbers Dataset - Complete Documentation

## Overview
This directory contains GSHS datasets with **ALL** column names converted to standardized Q## format, including both regular questions and derived variables.

## 📁 Output Location
```
data-sets/all-q-numbers/
```

## 🎯 Conversion Rules

### 1. **Regular Questions** (Q1-Q79)
- **q1, q2, q3** → **Q1, Q2, Q3**
- Original question responses from the survey
- Question numbers may be non-sequential (e.g., Q1, Q2, Q3, Q6, Q10... with gaps)

### 2. **Derived Variables - Recoded** (QN6-QN79)
- **qn6, qn7, qn8** → **QN6, QN7, QN8**
- Recoded/derived versions of the original questions
- **QN** prefix differentiates from original **Q** questions
- Same number as the question they're derived from

### 3. **Derived Variables - Special** (Q59-Q85)
These are GSHS standard derived variables with special names:

| Original Variable | New Code | Description |
|------------------|----------|-------------|
| `qnunwtg` | **Q59** | Underweight |
| `qnowtg` | **Q60** | Overweight |
| `qnobeseg` | **Q61** | Obese |
| `qnfrlg` | **Q62** | Low fruit consumption |
| `qnfr1g` | **Q63** | Fruit 1+ times per day |
| `qnfr2g` | **Q64** | Fruit 2+ times per day |
| `qnfr3g` | **Q65** | Fruit 3+ times per day |
| `qnveglg` | **Q66** | Low vegetable consumption |
| `qnveg1g` | **Q67** | Vegetables 1+ times per day |
| `qnveg2g` | **Q68** | Vegetables 2+ times per day |
| `qnveg3g` | **Q69** | Vegetables 3+ times per day |
| `qnsodalg` | **Q70** | Low soft drink consumption |
| `qnsoda1g` | **Q71** | Soft drinks 1+ times per day |
| `qnsoda2g` | **Q72** | Soft drinks 2+ times per day |
| `qnsoda3g` | **Q73** | Soft drinks 3+ times per day |
| `qnff1g` | **Q74** | Fast food 1+ times per day |
| `qnff2g` | **Q75** | Fast food 2+ times per day |
| `qnff3g` | **Q76** | Fast food 3+ times per day |
| `qnc2g` | **Q77** | Current cigarette use |
| `qntob2g` | **Q78** | Current tobacco use |
| `qnnotb2g` | **Q79** | Current non-cigarette tobacco use |
| `qnbcanyg` | **Q80** | Ever been bullied (any) |
| `qnc1g` | **Q81** | Ever tried cigarettes |
| `qnpa5g` | **Q82** | Physical activity 5+ days |
| `qnpa7g` | **Q83** | Physical activity 7 days |
| `qnpe3g` | **Q84** | Physical education 3+ days |
| `qnpe5g` | **Q85** | Physical education 5+ days |

### 4. **Metadata Columns** (Unchanged)
- `site`, `record`, `weight`, `stratum`, `psu`, `age`, `sex`, `class`, `grade`

## 📊 Dataset Summary

### Processed Countries (12 datasets):
1. **Bangladesh_22014** - 135 columns, 2,989 rows
2. **Brunei_Darussalam_2019** - 129 columns, 2,400 rows
3. **MUS_Rodrigues_2019_GSHS** - 143 columns, 2,715 rows
4. **Nepal_2015** - 141 columns, 6,529 rows
5. **Panama_2018** - 132 columns, 2,948 rows
6. **Philippines_2019** - 104 columns, 3,520 rows
7. **Saint_Lucia_2018** - 141 columns, 1,970 rows
8. **Thailand-2021** - 132 columns, 5,661 rows
9. **Thailand_2015** - 141 columns, 5,894 rows
10. **Timor_leste_2015** - 144 columns, 3,704 rows
11. **Uruguay-2019** - 106 columns, 1,555 rows
12. **GHSH_Pooled_Data1** - 17 columns, 106 rows (special pooled dataset)

### Total Question Coverage:
- **Q1 to Q85**: Regular and derived questions
- **QN6 to QN79**: Recoded variables
- **Total unique codes**: 156 (including Q, QN, and metadata)

## 📝 File Naming Convention
```
QNum_<original_filename>.csv
```
Example: `QNum_Philippines_2019.csv`

## 🔍 Example Usage

### Python
```python
import pandas as pd

# Load a dataset
df = pd.read_csv('QNum_Philippines_2019.csv')

# Access specific questions
age = df['Q1']  # Age question
suicide_consideration = df['Q26']  # Suicide consideration
suicide_plan = df['Q27']  # Suicide plan
suicide_attempt = df['Q28']  # Suicide attempt

# Access derived variables
underweight = df['Q59']  # qnunwtg
overweight = df['Q60']   # qnowtg
obese = df['Q61']        # qnobeseg

# Access recoded variables (if available)
age_recoded = df['QN6']  # Recoded age category
```

## 🎨 Column Structure Example

**Philippines_2019 Headers:**
```
site, record, weight, stratum, psu,
Q1, Q2, Q3, Q4, Q5, Q6, Q10, Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19,
Q22, Q23, Q24, Q25, Q26, Q27, Q34, Q35, Q36, Q37, Q38, Q39, Q40, Q41, Q42,
Q49, Q50, Q51, Q52, Q53, Q54, Q55, Q56, Q57, Q58,
Q62, Q63, Q64, Q76, Q77, Q79,
QN6, QN10, QN11, QN12, QN13, QN14, QN15, QN16, QN17, QN18, QN19,
QN22, QN23, QN24, QN25, QN26, QN27,
QN34, QN35, QN36, QN37, QN38, QN39, QN40, QN41, QN42,
QN49, QN50, QN51, QN52, QN53, QN54, QN55, QN56, QN57, QN58,
QN62, QN63, QN64, QN76, QN77, QN79,
Q59, Q60, Q61, Q74, Q75, Q76_1, Q82, Q83, Q84, Q85
```

## ⚠️ Important Notes

### Duplicate Handling
When both `q##` and `qn##` convert to the same number, they are differentiated:
- **q6** → **Q6** (original question)
- **qn6** → **QN6** (derived/recoded version)

If there's still a conflict (e.g., `qnobeseg` → `Q61`, but `q61` also exists), a suffix is added:
- **q61** → **Q61**
- **qnobeseg** → **Q61_1**

### Missing Question Numbers
Not all countries have all questions. Gaps in question numbering are normal:
- **Bangladesh**: Q1-Q58 (missing Q19, Q21)
- **Philippines**: Q1-Q79 (many gaps, only 47 questions)
- **Panama**: Q1-Q67 (59 questions with gaps)

## 📂 Related Directories

1. **`row-data/`** - Original raw datasets
2. **`converted-data-with-qustions/`** - Preprocessed to reference questions
3. **`question-numbers-only/`** - Simple Q1, Q2, Q3 format (no QN distinction)
4. **`all-q-numbers/`** - **THIS DIRECTORY** - Complete Q/QN format

## 🚀 Next Steps

### For Machine Learning:
```python
# Select suicide-related questions
suicide_features = ['Q26', 'Q27', 'Q28', 'Q29']  # Ideation, plan, attempt, factors

# Select demographic features
demographics = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5']  # Age, sex, grade, etc.

# Select derived health variables
health_vars = ['Q59', 'Q60', 'Q61']  # BMI categories

# Combine all features
features = demographics + suicide_features + health_vars
X = df[features]
```

### For Analysis:
```python
# Compare original vs recoded
print("Original Q26:", df['Q26'].value_counts())
print("Recoded QN26:", df['QN26'].value_counts())

# Analyze derived variables
print("Underweight (Q59):", df['Q59'].value_counts())
print("Overweight (Q60):", df['Q60'].value_counts())
```

## 📧 Questions?
Refer to:
- `column_conversion_summary.txt` - Complete mapping details
- GSHS questionnaire PDFs in `qustions/` folder
- Original codebooks for variable definitions

---
**Generated**: October 14, 2025  
**Script**: `convert_all_to_q_numbers.py`  
**Total Datasets**: 12 countries  
**Total Rows**: 39,885 (excluding pooled data)
