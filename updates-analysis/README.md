# GSHS Dataset Preprocessing

This directory contains scripts to preprocess Global School-based Student Health Survey (GSHS) datasets according to standardized reference questions.

## Overview

The preprocessing maps country-specific question numbers to standardized reference questions (e.g., Rodrigues 2019's Q11 maps to reference q10). This ensures consistency across all datasets for analysis.

## Directory Structure

```
updates-analysis/
├── preprocess_datasets.py          # Main preprocessing script
├── view_mapping_details.py         # View mapping details
├── others-files/
│   └── country-specific-GSHS-questionnaires-maping.xlsx  # Mapping file
├── data-sets/
│   ├── row-data/                   # Original CSV files
│   │   ├── Bangladesh_22014.csv
│   │   ├── Brunei_Darussalam_2019.csv
│   │   ├── MUS_Rodrigues_2019_GSHS.csv
│   │   ├── Nepal_2015.csv
│   │   ├── Panama_2018.csv
│   │   ├── Philippines_2019.csv
│   │   ├── Saint_Lucia_2018.csv
│   │   ├── Thailand_2015.csv
│   │   ├── Thailand-2021.csv
│   │   ├── Timor_leste_2015.csv
│   │   └── Uruguay-2019.csv
│   └── converted-data-with-qustions/  # Preprocessed output files
│       ├── converted_Bangladesh_22014.csv
│       ├── converted_Brunei_Darussalam_2019.csv
│       └── ... (other converted files)
```

## Reference Questions

The mapping file defines 27 reference questions that are standardized across all countries:

| Ref Question | Concept | Example Mapping |
|-------------|---------|-----------------|
| q1 | Custom Age | All countries: Q1 |
| q2 | Sex | All countries: Q2 |
| q3 | Grade level | All countries: Q3 |
| q10 | Fast food frequency | Philippines Q10, Rodrigues Q11 |
| q11 | Tooth brushing frequency | Philippines Q11, Rodrigues Q12 |
| q12 | Handwashing before eating | Philippines Q12, Rodrigues Q13 |
| q13 | Handwashing after toilet | Philippines Q13, Rodrigues Q14 |
| q14 | Use of soap when washing hands | Philippines Q14, Rodrigues Q15 |
| q15 | Physically attacked | Philippines Q15, Rodrigues Q16 |
| q20 | Bullied | Philippines Q20, Rodrigues Q21 |
| q22 | Felt lonely | Philippines Q22, Rodrigues Q23 |
| q23 | Could not sleep due to worry | Philippines Q23, Rodrigues Q24 |
| q24 | Seriously considered suicide | Philippines Q24, Rodrigues Q25 |
| q25 | Made a suicide plan | Philippines Q25, Rodrigues Q26 |
| q26 | Attempted suicide | Philippines Q26, Rodrigues Q27 |
| q27 | Number of close friends | Philippines Q27, Rodrigues Q28 |
| q28 | Age at cigarette initiation | Philippines Q28, Rodrigues Q30 |
| q29 | Current cigarette use | Philippines Q29, Rodrigues Q31 |
| q35 | Current alcohol use | Philippines Q35, Rodrigues Q37 |
| q40 | Age at drug initiation | Philippines Q40, Rodrigues Q43 |
| q44 | Ever had sexual intercourse | Philippines Q44, Rodrigues Q47 |
| q49 | Physically active ≥5 days/week | Philippines Q49, Rodrigues Q51 |
| q53 | Missed school w/o permission | Philippines Q53, Rodrigues Q66 |
| q54 | Peers kind/helpful | Philippines Q54, Rodrigues Q67 |
| q56 | Parents understood problems | Philippines Q56, Rodrigues Q70 |
| q57 | Parents knew free-time activities | Philippines Q57, Rodrigues Q71 |
| q58 | Parents went through things w/o permission | Philippines Q58, Rodrigues Q72 |

## Usage

### Prerequisites

Install required packages:
```powershell
pip install pandas openpyxl
```

### Running the Preprocessing

1. **Preprocess all datasets:**
   ```powershell
   cd "d:\Research\suicide analysis\suicidal-ideation-prediction\updates-analysis"
   python preprocess_datasets.py
   ```

   This will:
   - Read the mapping Excel file
   - Process each CSV file in `data-sets/row-data/`
   - Map country-specific questions to reference questions
   - Remove all non-reference columns
   - Save converted files to `data-sets/converted-data-with-qustions/`

2. **View mapping details:**
   ```powershell
   python view_mapping_details.py
   ```

   This will:
   - Display the complete mapping structure
   - Show which questions map to which reference questions for each country
   - Generate a detailed report file (`mapping_report.txt`)

## Output

### Converted Files

Each converted file contains only the reference questions (q1, q2, q3, q10-q58) with data mapped from the original country-specific column names.

**Example:** `converted_MUS_Rodrigues_2019_GSHS.csv`
```csv
q1,q2,q3,q10,q11,q12,q13,q14,q15,q20,q22,q23,q24,q25,q26,q27,q28,q29,q35,q40,q44,q49
2.0,2.0,1.0,5.0,5.0,5.0,5.0,3.0,2.0,2.0,1.0,2.0,2.0,1.0,4.0,,1.0,,1.0,1.0,,2.0
3.0,2.0,2.0,6.0,2.0,5.0,4.0,3.0,1.0,1.0,1.0,2.0,2.0,1.0,1.0,1.0,,1.0,6.0,1.0,1.0,2.0
```

### Processing Summary

The script provides a summary showing:
- Number of rows and columns for each converted dataset
- Which questions were successfully mapped
- Which expected questions were not found in the original dataset

**Example output:**
```
✓ Bangladesh: 2989 rows, 22 columns
✓ Brunei: 2400 rows, 21 columns
✓ Rodrigues: 2715 rows, 22 columns
✓ Nepal: 6529 rows, 22 columns
✓ Panama: 2948 rows, 21 columns
✓ Philippines: 3520 rows, 23 columns
✓ Saint Lucia: 1970 rows, 22 columns
✓ Thailand 2021: 5661 rows, 21 columns
✓ Thailand 2015: 5894 rows, 22 columns
✓ Timor-Leste: 3704 rows, 24 columns
✓ Uruguay: 1555 rows, 15 columns
```

## Features

### Case-Insensitive Matching
The script handles both uppercase (Q10) and lowercase (q10) column names automatically.

### Missing Question Handling
- Questions not available in a country's dataset are simply excluded
- A warning is displayed showing which expected questions were not found
- The script continues processing other available questions

### Data Preservation
- All original data values are preserved during mapping
- Missing values (NaN) are maintained
- No data transformation is performed, only column renaming

## Troubleshooting

### Issue: "No mapping found"
**Solution:** Check that the country name in the mapping Excel file matches the filename mapping in `map_csv_filename_to_country()` function.

### Issue: "Expected columns not found"
**Solution:** This is normal - some countries don't have all 27 reference questions. The script will process available questions and skip missing ones.

### Issue: Excel file not found
**Solution:** Ensure `country-specific-GSHS-questionnaires-maping.xlsx` is in the `others-files/` directory.

## Script Details

### `preprocess_datasets.py`
Main script that:
1. Loads the Excel mapping file
2. Parses country-specific question mappings
3. Processes each CSV file
4. Maps columns according to the reference questions
5. Removes non-reference columns
6. Saves converted datasets

### `view_mapping_details.py`
Utility script that:
1. Displays the complete mapping structure
2. Shows country-specific mappings
3. Generates a detailed text report

### `merge_datasets.py`
Dataset merging script that:
1. Combines all converted datasets into a single unified CSV
2. Adds a 'country' column to identify the source
3. Handles missing questions gracefully (outer join)
4. Generates data quality summary with missing value analysis
5. Creates a unified dataset ready for analysis

## Merging Converted Datasets

After preprocessing, you can merge all converted datasets into one:

```powershell
python merge_datasets.py
```

**Output:**
- `data-sets/unified_dataset.csv` - Single CSV with all countries (39,885+ rows)
- `data-sets/unified_dataset_summary.txt` - Data quality report

The unified dataset includes:
- A 'country' column identifying the source country and year
- All 27 reference questions (q1-q58)
- Proper handling of missing questions (NaN values)

**Example unified dataset structure:**
```csv
country,q1,q2,q3,q10,q11,q12,q13,q14,q15,q20,q22,q23,q24,q25,q26,q27,q28,q29,q35,q40,q44,q49,q53,q54,q56,q57,q58
Bangladesh 2014,3.0,1.0,1.0,1.0,3.0,4.0,5.0,5.0,4.0,1.0,1.0,3.0,2.0,2.0,1.0,2.0,1.0,1.0,1.0,1.0,2.0,6.0,,,,,
Philippines 2019,2.0,1.0,3.0,4.0,5.0,5.0,5.0,4.0,2.0,2.0,1.0,1.0,2.0,2.0,1.0,3.0,1.0,1.0,2.0,1.0,2.0,5.0,1.0,2.0,,,
```

## Notes

- The "Pooled" dataset (GHSH_Pooled_Data1.csv) is skipped because it doesn't have a mapping in the Excel file
- Some countries may have fewer than 27 questions due to survey variations
- The column order in output files follows the reference question order

## Next Steps

After preprocessing, the converted datasets can be:
1. Combined into a single merged dataset
2. Used for machine learning model training
3. Analyzed for cross-country comparisons
4. Processed for statistical analysis

All converted files maintain the same reference question structure, making them compatible for merging and analysis.
