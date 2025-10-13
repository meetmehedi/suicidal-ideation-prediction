"""
Convert ALL column names (including derived variables) to Q## format
This script converts:
- q1, q2, q3 -> Q1, Q2, Q3
- qn6, qn7, qn8 -> Q6, Q7, Q8
- qnunwtg, qnfrlg, qnowtg -> Q59, Q60, Q61, etc. (sequential numbering)
"""

import pandas as pd
import os
import glob
import re

# Mapping for special derived variables to Q numbers
# These are GSHS standard derived variables
DERIVED_VARIABLE_MAPPING = {
    # Anthropometric measures
    'qnunwtg': 'Q59',      # Underweight
    'qnowtg': 'Q60',       # Overweight
    'qnobeseg': 'Q61',     # Obese
    
    # Dietary behaviors - Fruit
    'qnfrlg': 'Q62',       # Low fruit consumption
    'qnfr1g': 'Q63',       # Fruit 1+ times per day
    'qnfr2g': 'Q64',       # Fruit 2+ times per day
    'qnfr3g': 'Q65',       # Fruit 3+ times per day
    
    # Dietary behaviors - Vegetables
    'qnveglg': 'Q66',      # Low vegetable consumption
    'qnveg1g': 'Q67',      # Vegetables 1+ times per day
    'qnveg2g': 'Q68',      # Vegetables 2+ times per day
    'qnveg3g': 'Q69',      # Vegetables 3+ times per day
    
    # Dietary behaviors - Soft drinks
    'qnsodalg': 'Q70',     # Low soft drink consumption
    'qnsoda1g': 'Q71',     # Soft drinks 1+ times per day
    'qnsoda2g': 'Q72',     # Soft drinks 2+ times per day
    'qnsoda3g': 'Q73',     # Soft drinks 3+ times per day
    
    # Dietary behaviors - Fast food
    'qnff1g': 'Q74',       # Fast food 1+ times per day
    'qnff2g': 'Q75',       # Fast food 2+ times per day
    'qnff3g': 'Q76',       # Fast food 3+ times per day
    
    # Tobacco and cigarette use
    'qnc2g': 'Q77',        # Current cigarette use
    'qntob2g': 'Q78',      # Current tobacco use
    'qnnotb2g': 'Q79',     # Current non-cigarette tobacco use
    'qnbcanyg': 'Q80',     # Ever been bullied (any)
    'qnc1g': 'Q81',        # Ever tried cigarettes
    
    # Physical activity
    'qnpa5g': 'Q82',       # Physical activity 5+ days
    'qnpa7g': 'Q83',       # Physical activity 7 days
    
    # Physical education
    'qnpe3g': 'Q84',       # Physical education 3+ days
    'qnpe5g': 'Q85',       # Physical education 5+ days
    
    # Add more mappings as needed
    'qnwater': 'Q86',      # Water consumption
    'qnmilk': 'Q87',       # Milk consumption
    'qnbk7day': 'Q88',     # Breakfast 7 days
    'qnbk0day': 'Q89',     # No breakfast
    'qnfr0day': 'Q90',     # No fruit
    'qnveg0day': 'Q91',    # No vegetables
}

def convert_column_to_q_number(col, seen_columns):
    """
    Convert any column name to Q## format
    Keep track of duplicates to avoid overwriting
    
    Examples:
    - q1, Q1, q01 -> Q1
    - qn6, QN6 -> QN6 (to differentiate from Q6)
    - qnunwtg -> Q59 (from mapping)
    - site, record, weight -> unchanged
    """
    col_lower = col.lower()
    
    # Keep metadata columns unchanged
    if col_lower in ['site', 'record', 'weight', 'country', 'stratum', 'psu', 'age', 'sex', 'class', 'grade', 'schoolid', 'classid']:
        return col
    
    # Check if it's in the special derived variable mapping
    if col_lower in DERIVED_VARIABLE_MAPPING:
        new_col = DERIVED_VARIABLE_MAPPING[col_lower]
        # Handle duplicates
        if new_col in seen_columns:
            suffix = 1
            while f"{new_col}_{suffix}" in seen_columns:
                suffix += 1
            new_col = f"{new_col}_{suffix}"
        seen_columns.add(new_col)
        return new_col
    
    # Pattern 1: qn## or QN## (derived variables like qn6, qn20)
    # Keep these as QN## to differentiate from Q##
    match = re.match(r'^qn(\d+)$', col_lower)
    if match:
        q_num = int(match.group(1))
        new_col = f'QN{q_num}'
        if new_col in seen_columns:
            suffix = 1
            while f"{new_col}_{suffix}" in seen_columns:
                suffix += 1
            new_col = f"{new_col}_{suffix}"
        seen_columns.add(new_col)
        return new_col
    
    # Pattern 2: q## or Q## (regular questions like q1, q10)
    match = re.match(r'^q(\d+)$', col_lower)
    if match:
        q_num = int(match.group(1))
        new_col = f'Q{q_num}'
        if new_col in seen_columns:
            suffix = 1
            while f"{new_col}_{suffix}" in seen_columns:
                suffix += 1
            new_col = f"{new_col}_{suffix}"
        seen_columns.add(new_col)
        return new_col
    
    # If no pattern matches, return as uppercase
    return col.upper()

def process_dataset(input_file, output_dir):
    """Process a single dataset and convert all columns to Q## format"""
    print(f"\nProcessing: {os.path.basename(input_file)}")
    
    # Read the dataset
    df = pd.read_csv(input_file)
    original_columns = df.columns.tolist()
    
    # Convert column names
    new_columns = {}
    seen_columns = set()
    for col in original_columns:
        new_col = convert_column_to_q_number(col, seen_columns)
        new_columns[col] = new_col
        if col != new_col:
            print(f"  {col} -> {new_col}")
    
    # Rename columns
    df.rename(columns=new_columns, inplace=True)
    
    # Save to output directory
    output_file = os.path.join(output_dir, f"QNum_{os.path.basename(input_file)}")
    df.to_csv(output_file, index=False)
    
    print(f"  Saved to: {os.path.basename(output_file)}")
    print(f"  Total columns: {len(df.columns)}, Rows: {len(df)}")
    
    return df.columns.tolist()

def main():
    # Directories
    input_dir = r"d:\Research\suicide analysis\suicidal-ideation-prediction\updates-analysis\data-sets\row-data"
    output_dir = r"d:\Research\suicide analysis\suicidal-ideation-prediction\updates-analysis\data-sets\all-q-numbers"
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all CSV files
    csv_files = glob.glob(os.path.join(input_dir, "*.csv"))
    
    if not csv_files:
        print(f"No CSV files found in {input_dir}")
        return
    
    print(f"Found {len(csv_files)} datasets to process")
    print("=" * 80)
    
    # Process each dataset
    all_q_numbers = set()
    for csv_file in sorted(csv_files):
        q_numbers = process_dataset(csv_file, output_dir)
        all_q_numbers.update([q for q in q_numbers if q.startswith('Q')])
    
    # Create summary
    print("\n" + "=" * 80)
    print("PROCESSING COMPLETE")
    print("=" * 80)
    print(f"\nOutput directory: {output_dir}")
    print(f"Total datasets processed: {len(csv_files)}")
    print(f"\nAll unique Q numbers across datasets:")
    sorted_q_nums = sorted(all_q_numbers, key=lambda x: int(re.search(r'\d+', x).group()))
    print(", ".join(sorted_q_nums[:50]))
    if len(sorted_q_nums) > 50:
        print(f"... and {len(sorted_q_nums) - 50} more")
    
    # Save summary
    summary_file = os.path.join(output_dir, "column_conversion_summary.txt")
    with open(summary_file, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("Column Conversion Summary\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"All unique Q numbers ({len(sorted_q_nums)} total):\n")
        for i, q in enumerate(sorted_q_nums, 1):
            f.write(f"{q}")
            if i % 10 == 0:
                f.write("\n")
            else:
                f.write(", ")
        f.write("\n\n")
        f.write("Derived Variable Mappings:\n")
        f.write("-" * 80 + "\n")
        for orig, new in sorted(DERIVED_VARIABLE_MAPPING.items()):
            f.write(f"{orig:20} -> {new}\n")
    
    print(f"\nSummary saved to: {os.path.basename(summary_file)}")

if __name__ == "__main__":
    main()
