# Quick Reference: Understanding Q vs QN Format

## 🎯 What's the Difference?

### **Q##** = Original Question
These are the **actual questions** asked in the survey:
- **Q26**: "During the past 12 months, did you ever seriously consider attempting suicide?"
- **Q27**: "During the past 12 months, did you make a plan about how you would attempt suicide?"
- **Q28**: "During the past 12 months, how many times did you actually attempt suicide?"

### **QN##** = Derived/Recoded Variable
These are **calculated or recoded** versions of the original questions:
- **QN26**: Binary (Yes/No) version of Q26
- **QN27**: Binary (Yes/No) version of Q27  
- **QN28**: Binary (Any attempt vs No attempt)

---

## 📋 Column Name Patterns

### Pattern 1: Regular Questions
```
q1, q2, q3, q26, q27, q28 → Q1, Q2, Q3, Q26, Q27, Q28
```
- Original survey responses
- May have 5-7 response options

### Pattern 2: Recoded Variables  
```
qn6, qn7, qn26, qn27 → QN6, QN7, QN26, QN27
```
- Simplified/binary versions
- Usually 1/2 (Yes/No) or categories

### Pattern 3: Special Derived Variables
```
qnunwtg → Q59   (Underweight)
qnowtg  → Q60   (Overweight)
qnfrlg  → Q62   (Low fruit consumption)
qnff1g  → Q74   (Fast food 1+ times/day)
```
- Complex derived measures
- Assigned Q59-Q85 range

---

## 🔍 Examples

### Bangladesh Dataset Columns:
```
Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10...    ← Original questions
QN6, QN7, QN8, QN9, QN10, QN11...            ← Recoded versions
Q59, Q60, Q61, Q62, Q63...Q85                ← Special derived
```

### Philippines Dataset Columns:
```
Q1, Q2, Q3, Q4, Q5, Q6, Q10, Q11...          ← Original (has gaps)
QN6, QN10, QN11, QN12, QN13...               ← Recoded
Q59, Q60, Q61, Q74, Q75, Q76_1...            ← Special derived
```

---

## 🎨 Visual Comparison

| Original Column | Converted To | Type | Description |
|----------------|--------------|------|-------------|
| `q1` | **Q1** | Original | How old are you? |
| `qn6` | **QN6** | Recoded | Age category (derived from Q1) |
| `q26` | **Q26** | Original | Considered suicide? (5 options) |
| `qn26` | **QN26** | Recoded | Considered suicide? (Yes/No) |
| `qnunwtg` | **Q59** | Special | Underweight status (BMI-based) |
| `qnfr3g` | **Q65** | Special | Fruit 3+ times/day (dietary) |

---

## 💡 Which Should I Use?

### For Most Analysis → Use **Q##** (Original Questions)
```python
# Suicide ideation questions
df[['Q26', 'Q27', 'Q28']]  # Get original detailed responses
```

### For Binary Analysis → Use **QN##** (Recoded)
```python
# Simple Yes/No for suicide ideation
df[['QN26', 'QN27', 'QN28']]  # Already recoded to 1/2
```

### For Health Indicators → Use **Q59-Q85** (Special Derived)
```python
# BMI categories, dietary patterns, physical activity
df[['Q59', 'Q60', 'Q61', 'Q62', 'Q74', 'Q82']]
```

---

## ⚠️ Important Notes

1. **Not all countries have both Q and QN** for every question
   - Philippines: Has both Q6 and QN6
   - Some countries: Only have Q6 or only QN6

2. **Numbering may not be sequential**
   - Philippines: Q1, Q2, Q3, Q4, Q5, Q6, **Q10** (no Q7, Q8, Q9)
   - This is normal - countries customize questionnaires

3. **Duplicates get suffixes**
   - If both `q61` and `qnobeseg` exist:
     - `q61` → **Q61**
     - `qnobeseg` → **Q61_1**

---

## 📊 Quick Check Script

```python
import pandas as pd

# Load your dataset
df = pd.read_csv('QNum_Philippines_2019.csv')

# Separate column types
q_cols = [c for c in df.columns if c.startswith('Q') and not c.startswith('QN')]
qn_cols = [c for c in df.columns if c.startswith('QN')]
meta_cols = [c for c in df.columns if not c.startswith('Q')]

print(f"Original Questions (Q##): {len(q_cols)}")
print(f"Recoded Variables (QN##): {len(qn_cols)}")
print(f"Metadata Columns: {len(meta_cols)}")
print(f"\nFirst 10 Q columns: {q_cols[:10]}")
print(f"First 10 QN columns: {qn_cols[:10]}")
```

---

## 🎓 GSHS Standard Codes Reference

### Suicide Questions (Most Important):
- **Q26** / **QN26**: Seriously considered suicide
- **Q27** / **QN27**: Made suicide plan
- **Q28** / **QN28**: Attempted suicide
- **Q29** / **QN29**: Suicide attempt required medical treatment

### Demographic:
- **Q1**: Age
- **Q2**: Sex  
- **Q3**: Grade
- **Q4**: Height
- **Q5**: Weight

### Special Derived (Q59-Q85):
- **Q59-Q61**: BMI categories (underweight, overweight, obese)
- **Q62-Q69**: Dietary behaviors (fruit, vegetables)
- **Q70-Q76**: Food frequency (sodas, fast food)
- **Q77-Q81**: Tobacco use
- **Q82-Q85**: Physical activity

---

**Need more details?** See `README.md` in this directory!
