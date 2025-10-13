"""
Script to preprocess GSHS datasets according to reference question mapping.
Maps country-specific questions to standardized reference questions and 
removes all other fields.
"""

import pandas as pd
import os
from pathlib import Path

def load_mapping_file(excel_path):
    """
    Load the Excel mapping file and create a mapping dictionary.
    Returns: dict with country names as keys and question mappings as values
    """
    print(f"Loading mapping file from: {excel_path}")
    
    # Read the Excel file
    df = pd.read_excel(excel_path)
    
    # Display the structure to understand it better
    print(f"\nMapping file columns: {df.columns.tolist()}")
    print(f"Mapping file shape: {df.shape}")
    print("\nFirst few rows:")
    print(df.head())
    
    return df

def create_country_mapping(mapping_df, country_name):
    """
    Create a mapping dictionary for a specific country.
    Returns: dict mapping {country_question: reference_question}
    """
    # This function will need to be adjusted based on the actual structure
    # of your Excel file. For now, creating a template.
    mapping = {}
    
    # Assuming the Excel has columns like: 'Reference_Question', 'Country1_Q', 'Country2_Q', etc.
    # or rows with reference questions and country-specific mappings
    
    return mapping

def preprocess_dataset(input_csv_path, output_csv_path, question_mapping, country_name):
    """
    Preprocess a single CSV dataset according to the question mapping.
    
    Args:
        input_csv_path: Path to input CSV file
        output_csv_path: Path to output CSV file
        question_mapping: Dictionary mapping country questions to reference questions
        country_name: Name of the country for logging
    """
    print(f"\nProcessing {country_name}...")
    
    # Read the CSV file
    df = pd.read_csv(input_csv_path)
    print(f"  Original shape: {df.shape}")
    print(f"  Original columns: {df.columns.tolist()[:20]}...")  # Show first 20 columns
    
    # Create a case-insensitive column mapping for the dataframe
    col_mapping_lower = {col.lower(): col for col in df.columns}
    
    # Create a new dataframe with mapped columns
    mapped_df = pd.DataFrame()
    
    # Track which reference questions we found
    found_mappings = []
    missing_mappings = []
    
    for country_q, ref_q in question_mapping.items():
        # Try both original case and lowercase
        country_q_lower = country_q.lower()
        
        if country_q in df.columns:
            mapped_df[ref_q] = df[country_q]
            found_mappings.append(f"{country_q} -> {ref_q}")
        elif country_q_lower in col_mapping_lower:
            actual_col = col_mapping_lower[country_q_lower]
            mapped_df[ref_q] = df[actual_col]
            found_mappings.append(f"{actual_col} -> {ref_q}")
        else:
            missing_mappings.append(f"{country_q} (for {ref_q})")
    
    print(f"  Mapped {len(found_mappings)} questions")
    if missing_mappings:
        print(f"  Warning: {len(missing_mappings)} expected columns not found in dataset")
        print(f"    Missing: {', '.join([m.split(' (')[0] for m in missing_mappings[:5]])}...")
    
    # Save the preprocessed data
    mapped_df.to_csv(output_csv_path, index=False)
    print(f"  Saved to: {output_csv_path}")
    print(f"  New shape: {mapped_df.shape}")
    
    return mapped_df

def parse_mapping_excel(mapping_df):
    """
    Parse the Excel mapping file and create country-specific mappings.
    
    This function needs to be customized based on your Excel structure.
    Returns: dict of {country_name: {country_question: ref_question}}
    """
    country_mappings = {}
    
    # Example structure - adjust based on actual Excel format:
    # If Excel has columns: RefQuestion, Bangladesh_Q, Nepal_Q, Thailand_Q, etc.
    
    print("\nParsing mapping structure...")
    print(f"Available columns: {mapping_df.columns.tolist()}")
    
    # Get reference questions (assuming first column or named 'RefQuestion')
    ref_col = mapping_df.columns[0]  # Adjust if needed
    
    # Iterate through other columns to create country mappings
    for col in mapping_df.columns[1:]:
        country_name = col.replace('_Q', '').replace('_', ' ')
        country_mappings[country_name] = {}
        
        for idx, row in mapping_df.iterrows():
            ref_question = row[ref_col]
            country_question = row[col]
            
            # Skip if mapping is empty or NaN
            if pd.notna(country_question) and str(country_question).strip():
                country_mappings[country_name][str(country_question).strip()] = str(ref_question).strip()
    
    return country_mappings

def map_csv_filename_to_country(csv_filename):
    """
    Map CSV filename to country name in the mapping Excel.
    Returns: country name string
    """
    # Extract country name from filename
    # e.g., "MUS_Rodrigues_2019_GSHS.csv" -> "Rodrigues"
    # or "Bangladesh_22014.csv" -> "Bangladesh"
    
    name_mappings = {
        'Bangladesh_22014.csv': 'Bangladesh',
        'Brunei_Darussalam_2019.csv': 'Brunei',
        'MUS_Rodrigues_2019_GSHS.csv': 'Rodrigues',
        'Nepal_2015.csv': 'Nepal',
        'Panama_2018.csv': 'Panama',
        'Philippines_2019.csv': 'Philippines',
        'Saint_Lucia_2018.csv': 'Saint Lucia',
        'Thailand_2015.csv': 'Thailand 2015',
        'Thailand-2021.csv': 'Thailand 2021',
        'Timor_leste_2015.csv': 'Timor-Leste',  # Match Excel column name
        'Uruguay-2019.csv': 'Uruguay',
        'GHSH_Pooled_Data1.csv': 'Pooled'
    }
    
    return name_mappings.get(csv_filename, csv_filename.replace('.csv', ''))

def main():
    """Main execution function"""
    
    # Define paths
    base_dir = Path(__file__).parent
    mapping_file = base_dir / 'others-files' / 'country-specific-GSHS-questionnaires-maping.xlsx'
    input_dir = base_dir / 'data-sets' / 'row-data'
    output_dir = base_dir / 'data-sets' / 'converted-data-with-qustions'
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("="*80)
    print("GSHS Dataset Preprocessing Script")
    print("="*80)
    
    # Load mapping file
    try:
        mapping_df = load_mapping_file(mapping_file)
    except Exception as e:
        print(f"\nError loading mapping file: {e}")
        print("\nPlease ensure the Excel file exists and is properly formatted.")
        return
    
    print("\n" + "="*80)
    print("Please review the mapping file structure above.")
    print("You may need to adjust the parsing logic in parse_mapping_excel()")
    print("based on your actual Excel structure.")
    print("="*80)
    
    # Parse the mapping to get country-specific question mappings
    try:
        country_mappings = parse_mapping_excel(mapping_df)
        print(f"\nFound mappings for {len(country_mappings)} countries/datasets")
    except Exception as e:
        print(f"\nError parsing mapping file: {e}")
        print("You may need to customize the parse_mapping_excel() function")
        return
    
    # Get all CSV files in the input directory
    csv_files = list(input_dir.glob('*.csv'))
    print(f"\nFound {len(csv_files)} CSV files to process")
    
    # Process each CSV file
    results = {}
    for csv_file in csv_files:
        country_name = map_csv_filename_to_country(csv_file.name)
        output_file = output_dir / f"converted_{csv_file.name}"
        
        # Find matching mapping
        mapping = None
        for map_country, map_dict in country_mappings.items():
            if map_country.lower() in country_name.lower() or country_name.lower() in map_country.lower():
                mapping = map_dict
                break
        
        if mapping and len(mapping) > 0:
            try:
                result_df = preprocess_dataset(csv_file, output_file, mapping, country_name)
                results[country_name] = {
                    'status': 'success',
                    'rows': len(result_df),
                    'columns': len(result_df.columns)
                }
            except Exception as e:
                print(f"  Error processing {country_name}: {e}")
                results[country_name] = {'status': 'error', 'message': str(e)}
        else:
            print(f"\nSkipping {country_name}: No mapping found in Excel file")
            results[country_name] = {'status': 'skipped', 'message': 'No mapping found'}
    
    # Print summary
    print("\n" + "="*80)
    print("PROCESSING SUMMARY")
    print("="*80)
    for country, result in results.items():
        status = result['status']
        if status == 'success':
            print(f"✓ {country}: {result['rows']} rows, {result['columns']} columns")
        elif status == 'error':
            print(f"✗ {country}: Error - {result['message']}")
        else:
            print(f"⊘ {country}: {result['message']}")
    
    print("\n" + "="*80)
    print(f"Output files saved to: {output_dir}")
    print("="*80)

if __name__ == "__main__":
    main()
