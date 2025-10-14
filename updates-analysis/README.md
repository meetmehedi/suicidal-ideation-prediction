# GSHS Dataset Preprocessing - Complete Guide

## Overview
This directory contains scripts and tools for preprocessing Global School-based Student Health Survey (GSHS) datasets according to standardized reference question mappings.

## Directory Structure
```
updates-analysis/
├── preprocess_datasets.py          # Main preprocessing script
├── validate_conversions.py         # Validation script for converted data
├── PREPROCESSING_SUMMARY.md        # Detailed summary of preprocessing results
├── data-sets/
│   ├── row-data/                   # Original raw GSHS datasets (12 files)
│   └── converted-data-with-qustions/  # Standardized converted datasets (9 files)
└── others-files/
    └── country-specific-GSHS-questionnaires-maping.xlsx  # Question mapping file
```

## Quick Start

### 1. Preprocess All Datasets
```powershell
cd "d:\Research\suicide analysis\suicidal-ideation-prediction\updates-analysis"
python preprocess_datasets.py
```

This will:
- Read the Excel mapping file
- Process all CSV files in `data-sets/row-data/`
- Map country-specific questions to standardized reference questions
- Save converted files to `data-sets/converted-data-with-qustions/`

### 2. Validate Conversions
```powershell
python validate_conversions.py
```

This will verify that all converted files:
- Have exactly 27 standardized columns
- Match the expected reference question format
- Contain valid data for suicide-related questions (q24, q25, q26)

## Mapping File Structure

The Excel file `country-specific-GSHS-questionnaires-maping.xlsx` contains:
- **Column 1 (Ref)**: Reference question IDs (q1, q2, q3, etc.)
- **Column 2 (Question Concept)**: Description of each question
- **Columns 3+**: Country-specific question mappings

Example:
| Ref | Question Concept | Bangladesh 2014 | Nepal 2015 | Thailand 2021 |
|-----|-----------------|-----------------|------------|---------------|
| q1  | Custom Age      | q1              | q1         | Q1            |
| q24 | Seriously considered attempting suicide | q24 | q24 | Q24 |

## Standardized Reference Questions (27 total)

### Demographics (3)
- `q1` - Age
- `q2` - Sex
- `q3` - Grade level

### Health Behaviors (8)
- `q10` - Fast food consumption frequency
- `q11` - Tooth brushing frequency
- `q12` - Hand washing before eating
- `q13` - Hand washing after toilet
- `q14` - Hand washing with soap
- `q49` - Physical activity (5+ days/week)
- `q28` - Age at cigarette initiation
- `q29` - Current cigarette use

### Mental Health & Violence (6)
- `q15` - Physically attacked (past 12 months)
- `q20` - Bullied (past 30 days)
- `q22` - Felt lonely (past 12 months)
- `q23` - Could not sleep due to worry (past 12 months)
- `q24` - **Seriously considered suicide**
- `q25` - **Made a suicide plan**
- `q26` - **Attempted suicide (past 12 months)**

### Substance Use (2)
- `q35` - Current alcohol use
- `q40` - Age at drug use initiation

### Social & Environmental (6)
- `q27` - Number of close friends
- `q44` - Sexual intercourse history
- `q53` - Missed school without permission
- `q54` - Students were kind/helpful
- `q56` - Parents understood problems
- `q57` - Parents knew free time activities
- `q58` - Parents invaded privacy

## Successfully Processed Datasets (9)

| Country/Region | Year | Records | Status |
|----------------|------|---------|--------|
| Bangladesh | 2014 | 2,989 | ✅ |
| Brunei Darussalam | 2019 | 2,400 | ✅ |
| Mauritius | 2019 | 2,715 | ✅ |
| Nepal | 2015 | 6,529 | ✅ |
| Panama | 2018 | 2,948 | ✅ |
| Saint Lucia | 2018 | 1,970 | ✅ |
| Thailand | 2021 | 5,661 | ✅ |
| Thailand | 2014 | 5,894 | ✅ |
| Timor-Leste | 2014 | 3,704 | ✅ |

**Total: 34,810 student records**

## Datasets Not Yet Mapped (3)

These datasets are available but not yet included in the mapping file:
1. Philippines 2019
2. Uruguay 2019
3. GHSH Pooled Data

**To add these datasets:**
1. Open the Excel mapping file
2. Add new columns for each country
3. Map each country's questions to the reference questions
4. Update the `map_csv_filename_to_country()` function in `preprocess_datasets.py`
5. Re-run the preprocessing script

## Key Features

### ✅ Case-Insensitive Matching
The script handles different capitalizations:
- `Q1`, `q1`, `Q1` are all treated as equivalent
- Ensures robust matching across different dataset formats

### ✅ Data Preservation
- Original data values are preserved exactly
- No transformations or cleaning applied
- Missing values (NaN) retained as-is
- Original files remain untouched

### ✅ Comprehensive Validation
The validation script checks:
- Column count (must be exactly 27)
- Column names (must match reference questions)
- Data completeness for suicide-related questions
- Overall data quality metrics

### ✅ Detailed Logging
Both scripts provide:
- Progress updates during processing
- Column mapping confirmations
- Warning messages for missing columns
- Summary statistics

## Script Details

### `preprocess_datasets.py`

**Main Functions:**
- `load_mapping_file()` - Loads Excel mapping file
- `parse_mapping_excel()` - Extracts country-specific mappings
- `preprocess_dataset()` - Converts a single dataset
- `map_csv_filename_to_country()` - Maps filenames to mapping columns
- `main()` - Orchestrates the entire process

**Input:** Raw CSV files from various countries
**Output:** Standardized CSV files with 27 reference questions

### `validate_conversions.py`

**Main Function:**
- `validate_converted_datasets()` - Checks all converted files

**Validation Checks:**
- Column consistency across datasets
- Expected column count (27)
- Data completeness metrics
- Suicide-related question response counts

## Data Quality Metrics

From validation results:
- **Average missing data**: 1.5% - 5.2% per dataset
- **Suicide question responses**:
  - q24 (considered suicide): 33,924 valid responses (97.5%)
  - q25 (suicide plan): 34,005 valid responses (97.7%)
  - q26 (attempted suicide): 34,499 valid responses (99.1%)

## Requirements

```bash
pip install pandas openpyxl
```

## Troubleshooting

### Error: "No mapping found"
- Check that the country name in `map_csv_filename_to_country()` matches the Excel column name exactly
- Verify the Excel file contains the country column

### Error: "Column not found"
- The original dataset may use different question IDs
- Update the mapping in the Excel file
- Verify column names in the raw CSV file

### Error: "Missing optional dependency 'openpyxl'"
```bash
pip install openpyxl
```

## Next Steps

1. **Add Missing Mappings**: Include Philippines, Uruguay, and Pooled data
2. **Merge Datasets**: Combine all converted files into a single dataset
3. **Feature Engineering**: Create derived variables for analysis
4. **Model Training**: Use standardized data for predictive modeling

## Contact & Support

For questions about the mapping or preprocessing:
- Review `PREPROCESSING_SUMMARY.md` for detailed results
- Check the Excel mapping file for question definitions
- Run validation script to verify data quality

---

**Last Updated**: October 15, 2025
**Version**: 1.0
**Total Records**: 34,810 students across 9 countries
