"""
Script to merge all converted country datasets into a single unified dataset.
Adds a 'country' column to identify the source of each record.
"""

import pandas as pd
from pathlib import Path

def main():
    # Define paths
    base_dir = Path(__file__).parent
    converted_dir = base_dir / 'data-sets' / 'converted-data-with-qustions'
    output_file = base_dir / 'data-sets' / 'unified_dataset.csv'
    
    print("="*80)
    print("GSHS Dataset Merger")
    print("="*80)
    
    # Get all converted CSV files
    csv_files = list(converted_dir.glob('converted_*.csv'))
    
    if not csv_files:
        print("\nError: No converted files found!")
        print(f"Please ensure converted files are in: {converted_dir}")
        return
    
    print(f"\nFound {len(csv_files)} converted datasets to merge")
    
    # Country name mapping
    country_mappings = {
        'converted_Bangladesh_22014.csv': 'Bangladesh 2014',
        'converted_Brunei_Darussalam_2019.csv': 'Brunei 2019',
        'converted_MUS_Rodrigues_2019_GSHS.csv': 'Mauritius (Rodrigues) 2019',
        'converted_Nepal_2015.csv': 'Nepal 2015',
        'converted_Panama_2018.csv': 'Panama 2018',
        'converted_Philippines_2019.csv': 'Philippines 2019',
        'converted_Saint_Lucia_2018.csv': 'Saint Lucia 2018',
        'converted_Thailand_2015.csv': 'Thailand 2015',
        'converted_Thailand-2021.csv': 'Thailand 2021',
        'converted_Timor_leste_2015.csv': 'Timor-Leste 2015',
        'converted_Uruguay-2019.csv': 'Uruguay 2019'
    }
    
    # List to store all dataframes
    all_dataframes = []
    
    print("\nLoading and processing datasets:")
    print("-"*80)
    
    # Load each dataset and add country column
    for csv_file in csv_files:
        country_name = country_mappings.get(csv_file.name, csv_file.stem.replace('converted_', ''))
        
        # Read the dataset
        df = pd.read_csv(csv_file)
        
        # Add country column
        df.insert(0, 'country', country_name)
        
        print(f"  {country_name:35} - {len(df):5} rows, {len(df.columns)-1:2} questions")
        
        all_dataframes.append(df)
    
    # Merge all datasets
    print("\n" + "="*80)
    print("Merging datasets...")
    
    # Concatenate all dataframes
    # Use outer join to include all columns from all datasets
    unified_df = pd.concat(all_dataframes, axis=0, ignore_index=True, sort=False)
    
    print(f"Unified dataset shape: {unified_df.shape}")
    print(f"  Total rows: {len(unified_df)}")
    print(f"  Total columns: {len(unified_df.columns)} (including 'country' column)")
    
    # Display column names
    ref_columns = [col for col in unified_df.columns if col != 'country']
    print(f"\nReference questions included: {len(ref_columns)}")
    print(f"  {', '.join(sorted(ref_columns))}")
    
    # Check for missing data
    print("\n" + "="*80)
    print("Data Quality Summary:")
    print("-"*80)
    
    # Count records per country
    country_counts = unified_df['country'].value_counts().sort_index()
    print("\nRecords per country:")
    for country, count in country_counts.items():
        print(f"  {country:35} {count:5} records")
    
    # Check missing values per column
    print("\nMissing values per question:")
    missing_counts = unified_df.isnull().sum()
    missing_pct = (missing_counts / len(unified_df) * 100).round(2)
    
    for col in sorted(ref_columns):
        if col in unified_df.columns:
            missing = missing_counts[col]
            pct = missing_pct[col]
            print(f"  {col:5} - {missing:6} missing ({pct:6.2f}%)")
    
    # Save the unified dataset
    print("\n" + "="*80)
    print("Saving unified dataset...")
    unified_df.to_csv(output_file, index=False)
    print(f"✓ Saved to: {output_file}")
    
    # Create a summary report
    summary_file = base_dir / 'data-sets' / 'unified_dataset_summary.txt'
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("UNIFIED GSHS DATASET SUMMARY\n")
        f.write("="*80 + "\n\n")
        f.write(f"Total Records: {len(unified_df)}\n")
        f.write(f"Total Countries: {unified_df['country'].nunique()}\n")
        f.write(f"Total Questions: {len(ref_columns)}\n\n")
        f.write("Countries Included:\n")
        for country, count in country_counts.items():
            f.write(f"  - {country}: {count} records\n")
        f.write("\nDataset Info:\n")
        f.write(unified_df.info().__str__())
    
    print(f"✓ Summary saved to: {summary_file}")
    
    # Display first few rows
    print("\n" + "="*80)
    print("Preview of unified dataset (first 5 rows):")
    print("-"*80)
    print(unified_df.head().to_string(index=False))
    
    print("\n" + "="*80)
    print("Dataset merging complete!")
    print("="*80)

if __name__ == "__main__":
    main()
