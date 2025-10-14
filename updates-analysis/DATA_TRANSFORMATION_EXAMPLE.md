# Data Transformation Example

## Before and After Conversion

### Example: Bangladesh 2014 Dataset

#### BEFORE Conversion
- **Total columns**: 135 (includes many questions not relevant to the study)
- **Sample columns**: Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10, Q11, Q12, Q13, Q14, Q15...
- **Total records**: 2,989 students
- **Format**: Original GSHS format with country-specific question IDs

#### AFTER Conversion
- **Total columns**: 27 (only standardized reference questions)
- **All columns**: q1, q2, q3, q10, q11, q12, q13, q14, q15, q20, q22, q23, q24, q25, q26, q27, q28, q29, q35, q40, q44, q49, q53, q54, q56, q57, q58
- **Total records**: 2,989 students (no data loss)
- **Format**: Standardized reference format, compatible across all countries

### Data Preservation Example

**Original Record (First Student):**
```
Q1: 3.0   (Age)
Q2: 1.0   (Sex)
Q3: 1.0   (Grade)
Q24: 2.0  (Considered suicide)
Q25: 2.0  (Suicide plan)
Q26: 1.0  (Attempted suicide)
```

**Converted Record (Same Student):**
```
q1: 3.0   (Age)
q2: 1.0   (Sex)
q3: 1.0   (Grade)
q24: 2.0  (Considered suicide)
q25: 2.0  (Suicide plan)
q26: 1.0  (Attempted suicide)
```

**Key Points:**
- ✅ All values preserved exactly
- ✅ Column names standardized (Q → q)
- ✅ Only relevant questions retained
- ✅ Data remains unchanged

## Column Reduction Summary

### All Processed Datasets

| Dataset | Original Columns | Final Columns | Reduction |
|---------|-----------------|---------------|-----------|
| Bangladesh 2014 | 135 | 27 | 80.0% |
| Brunei Darussalam 2019 | 129 | 27 | 79.1% |
| Mauritius 2019 | 143 | 27 | 81.1% |
| Nepal 2015 | 141 | 27 | 80.9% |
| Panama 2018 | 132 | 27 | 79.5% |
| Saint Lucia 2018 | 141 | 27 | 80.9% |
| Thailand 2021 | 132 | 27 | 79.5% |
| Thailand 2014 | 141 | 27 | 80.9% |
| Timor-Leste 2014 | 144 | 27 | 81.3% |

**Average column reduction: ~80%**

This reduction:
- Eliminates unnecessary columns
- Standardizes across all datasets
- Focuses on research-relevant questions
- Simplifies downstream analysis

## Standardization Benefits

### 1. Cross-Country Comparability
All datasets now use the same 27 standardized questions, enabling direct comparison across countries.

### 2. Simplified Analysis
Reduced from 129-144 columns to just 27 relevant columns per dataset.

### 3. Consistent Naming
- All column names lowercase (q1, q2, q3...)
- Consistent format across all countries
- Easy to reference and use in code

### 4. Focus on Key Variables
The 27 retained questions cover:
- Demographics (age, sex, grade)
- Mental health (loneliness, worry, sleep)
- **Suicide indicators (q24, q25, q26)** ← Primary outcome variables
- Health behaviors (diet, hygiene, exercise)
- Social factors (friends, school, parents)
- Risk behaviors (substance use, violence)

## Data Integrity Verification

✅ **Row counts preserved**: All 34,810 student records retained
✅ **Values unchanged**: Original responses preserved exactly
✅ **Missing data maintained**: NaN values kept as-is
✅ **Data types preserved**: Numeric values remain numeric
✅ **No transformations**: Raw data ready for analysis

## Next Steps After Preprocessing

1. **Merge all converted datasets** into single file
2. **Handle missing values** according to analysis requirements
3. **Encode categorical variables** if needed
4. **Create derived features** (e.g., suicide risk composite scores)
5. **Split data** into train/test sets
6. **Build predictive models** for suicide ideation

---

**Processing Date**: October 15, 2025
**Script Version**: 1.0
**Quality Check**: All validations passed ✅
