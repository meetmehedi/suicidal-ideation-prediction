# GSHS Dataset Preprocessing Summary

## Overview
This document summarizes the preprocessing of GSHS (Global School-based Student Health Survey) datasets according to country-specific question mappings.

## Date: October 15, 2025

## Preprocessing Details

### Mapping Source
- **Mapping File**: `country-specific-GSHS-questionnaires-maping.xlsx`
- **Location**: `updates-analysis/others-files/`
- **Total Reference Questions**: 27

### Reference Questions Mapped
The following standardized reference questions were used:
- `q1` - Custom Age
- `q2` - Sex
- `q3` - Grade level
- `q10` - Frequency of fast food consumption
- `q11` - Frequency of tooth brushing
- `q12` - Hand washing before eating
- `q13` - Hand washing after using the toilet
- `q14` - Hand washing with soap
- `q15` - Physically attacked in the past 12 months
- `q20` - Bullied in the past 30 days
- `q22` - Felt lonely in the past 12 months
- `q23` - Could not sleep due to worry in the past 12 months
- `q24` - Seriously considered attempting suicide
- `q25` - Made a suicide plan
- `q26` - Attempted suicide in the past 12 months
- `q27` - Number of close friends
- `q28` - Age at initiation of cigarette use
- `q29` - Current cigarette use
- `q35` - Current alcohol use
- `q40` - Age at initiation of drug use
- `q44` - Ever engaged in sexual intercourse
- `q49` - Engaged in physical activity on at least 5 days in the past week
- `q53` - Missed school without permission
- `q54` - Other students were kind and helpful
- `q56` - Parents or guardians understood their problems
- `q57` - Parents or guardians knew how they spent free time
- `q58` - Parents or guardians went through their things without permission

## Successfully Processed Datasets

| Dataset | Country/Region | Year | Original Rows | Original Columns | Final Columns | Output File |
|---------|----------------|------|---------------|------------------|---------------|-------------|
| Bangladesh_22014.csv | Bangladesh | 2014 | 2,989 | 135 | 27 | converted_Bangladesh_22014.csv |
| Brunei_Darussalam_2019.csv | Brunei Darussalam | 2019 | 2,400 | 129 | 27 | converted_Brunei_Darussalam_2019.csv |
| MUS_Rodrigues_2019_GSHS.csv | Mauritius | 2019 | 2,715 | 143 | 27 | converted_MUS_Rodrigues_2019_GSHS.csv |
| Nepal_2015.csv | Nepal | 2015 | 6,529 | 141 | 27 | converted_Nepal_2015.csv |
| Panama_2018.csv | Panama | 2018 | 2,948 | 132 | 27 | converted_Panama_2018.csv |
| Saint_Lucia_2018.csv | Saint Lucia | 2018 | 1,970 | 141 | 27 | converted_Saint_Lucia_2018.csv |
| Thailand-2021.csv | Thailand | 2021 | 5,661 | 132 | 27 | converted_Thailand-2021.csv |
| Thailand_2015.csv | Thailand | 2014 | 5,894 | 141 | 27 | converted_Thailand_2015.csv |
| Timor_leste_2015.csv | Timor-Leste | 2014 | 3,704 | 144 | 27 | converted_Timor_leste_2015.csv |

### Total Successfully Processed
- **9 datasets**
- **Total records**: 40,810 students
- **All standardized to**: 27 reference questions

## Skipped Datasets

The following datasets were not processed because they were not included in the mapping file:

1. **GHSH_Pooled_Data1.csv** - No mapping available (Pooled data)
2. **Philippines_2019.csv** - No mapping available
3. **Uruguay-2019.csv** - No mapping available

## Processing Features

### Case-Insensitive Matching
The preprocessing script handles case-insensitive column matching, so:
- `Q1`, `q1`, `Q1` are all treated as the same column
- This ensures robust matching across different dataset formats

### Data Preservation
- All original data values are preserved
- No data transformation or cleaning applied
- Missing values (NaN) are retained as-is

### Validation
- Each dataset was verified to have exactly 27 columns after conversion
- Column names match the reference question format (q1, q2, q3, etc.)

## Output Location
All converted files are saved to:
```
updates-analysis/data-sets/converted-data-with-qustions/
```

## Script Used
- **Script**: `preprocess_datasets.py`
- **Location**: `updates-analysis/`

## Next Steps

To add mappings for the skipped datasets:
1. Add new columns to the Excel mapping file for:
   - Philippines 2019
   - Uruguay 2019
   - GHSH Pooled Data (if needed)
2. Update the `map_csv_filename_to_country()` function in `preprocess_datasets.py`
3. Re-run the script

## Notes
- The script automatically creates the output directory if it doesn't exist
- Original files remain unchanged
- All mappings are case-insensitive to handle variations in dataset formats
