# Quick Start Guide

## What Was Done

Your GSHS datasets have been preprocessed to standardize question columns across all countries according to the reference mapping in the Excel file.

## Files Created

### Scripts
1. **`preprocess_datasets.py`** - Main preprocessing script
2. **`view_mapping_details.py`** - View mapping structure
3. **`merge_datasets.py`** - Merge all converted datasets
4. **`run_complete_workflow.py`** - Run all scripts in sequence

### Output Files
- **`data-sets/converted-data-with-qustions/`** - 11 converted CSV files (one per country)
- **`data-sets/unified_dataset.csv`** - Single merged dataset (39,885 rows)
- **`mapping_report.txt`** - Detailed mapping documentation
- **`data-sets/unified_dataset_summary.txt`** - Data quality report

## How It Works

### Example: Rodrigues 2019
**Before (Original):**
```csv
site,record,q1,q2,q3,...,q11,q12,q13,...
MUA,1,2,2,1,...,2,5,5,...
```

**After (Converted):**
```csv
q1,q2,q3,...,q10,q11,q12,...
2.0,2.0,1.0,...,2.0,5.0,5.0,...
```

The Rodrigues Q11 → Reference q10 (as per your mapping)

## Quick Commands

### Run Complete Workflow
```powershell
cd "d:\Research\suicide analysis\suicidal-ideation-prediction\updates-analysis"
python run_complete_workflow.py
```

### Individual Scripts
```powershell
# View mapping details
python view_mapping_details.py

# Preprocess all datasets
python preprocess_datasets.py

# Merge converted datasets
python merge_datasets.py
```

## Results Summary

### Converted Datasets
| Country | Year | Rows | Questions |
|---------|------|------|-----------|
| Bangladesh | 2014 | 2,989 | 22 |
| Brunei | 2019 | 2,400 | 21 |
| Mauritius (Rodrigues) | 2019 | 2,715 | 22 |
| Nepal | 2015 | 6,529 | 22 |
| Panama | 2018 | 2,948 | 21 |
| Philippines | 2019 | 3,520 | 23 |
| Saint Lucia | 2018 | 1,970 | 22 |
| Thailand | 2015 | 5,894 | 22 |
| Thailand | 2021 | 5,661 | 21 |
| Timor-Leste | 2015 | 3,704 | 24 |
| Uruguay | 2019 | 1,555 | 15 |
| **TOTAL** | | **39,885** | **27** |

### Reference Questions
All datasets now use these standardized question columns:
- **q1** - Age
- **q2** - Sex
- **q3** - Grade level
- **q10** - Fast food frequency
- **q11** - Tooth brushing frequency
- **q12** - Handwashing before eating
- **q13** - Handwashing after toilet
- **q14** - Use of soap when washing hands
- **q15** - Physically attacked
- **q20** - Bullied
- **q22** - Felt lonely
- **q23** - Could not sleep due to worry
- **q24** - Seriously considered suicide
- **q25** - Made a suicide plan
- **q26** - Attempted suicide
- **q27** - Number of close friends
- **q28** - Age at cigarette initiation
- **q29** - Current cigarette use
- **q35** - Current alcohol use
- **q40** - Age at drug initiation
- **q44** - Ever had sexual intercourse
- **q49** - Physically active ≥5 days/week
- **q53** - Missed school w/o permission
- **q54** - Peers kind/helpful
- **q56** - Parents understood problems
- **q57** - Parents knew free-time activities
- **q58** - Parents went through things w/o permission

## Data Quality Notes

### Missing Data by Question
- **Low missing** (<5%): q1-q15, q22-q27, q35, q49
- **Moderate missing** (5-20%): q28, q29, q40, q44
- **High missing** (>80%): q53, q54, q56-q58

**Note:** High missing rates for some questions (q53-q58) are due to these questions not being included in all country surveys, not data quality issues.

## Next Steps

### For Machine Learning
1. Load the unified dataset:
   ```python
   import pandas as pd
   df = pd.read_csv('data-sets/unified_dataset.csv')
   ```

2. Handle missing values:
   ```python
   # Option 1: Drop columns with >80% missing
   df_clean = df.drop(columns=['q53', 'q54', 'q56', 'q57', 'q58'])
   
   # Option 2: Impute missing values
   from sklearn.impute import SimpleImputer
   imputer = SimpleImputer(strategy='median')
   df_imputed = pd.DataFrame(imputer.fit_transform(df.select_dtypes(include=[np.number])))
   ```

3. Use for model training:
   ```python
   # Suicide-related questions: q24, q25, q26
   X = df_clean.drop(columns=['country', 'q24', 'q25', 'q26'])
   y = df_clean['q24']  # Seriously considered suicide
   ```

### For Statistical Analysis
- Compare suicide rates across countries
- Analyze risk factors (bullying, loneliness, etc.)
- Examine temporal trends (Thailand 2015 vs 2021)
- Cross-country behavioral patterns

## Troubleshooting

### Issue: Missing columns in output
**Solution:** Some countries don't have all 27 reference questions. This is expected - the script only maps available questions.

### Issue: High missing values
**Solution:** Questions q53-q58 were not included in all country surveys. Consider dropping these columns or analyzing only countries that have them.

### Issue: Need to reprocess
**Solution:** Delete files in `data-sets/converted-data-with-qustions/` and run `preprocess_datasets.py` again.

## Documentation

For detailed documentation, see:
- **README.md** - Complete guide with all features
- **mapping_report.txt** - Full mapping structure
- **unified_dataset_summary.txt** - Data quality statistics

## Contact & Support

For questions about:
- **Mapping**: Check `mapping_report.txt` and the Excel file
- **Data quality**: Review `unified_dataset_summary.txt`
- **Processing**: Check the output logs from each script

---

**All preprocessing complete! Your datasets are now ready for analysis.** 🎉
