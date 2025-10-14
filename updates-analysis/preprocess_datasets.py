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
    df = pd.read_csv(input_csv_path, low_memory=False)
    print(f"  Original shape: {df.shape}")
    print(f"  Original columns (first 20): {df.columns.tolist()[:20]}")
    
    # Create a case-insensitive column mapping for the dataframe
    col_mapping_lower = {col.lower(): col for col in df.columns}
    
    # Create a new dataframe with mapped columns
    mapped_df = pd.DataFrame()
    
    # Track which reference questions we found
    found_mappings = []
    missing_mappings = []
    
    # Clean the question_mapping to remove lowercase duplicates
    # (we added them for matching, but we only want to iterate once per question)
    seen_ref_questions = set()
    
    for country_q, ref_q in question_mapping.items():
        # Skip if we've already processed this reference question
        if ref_q in seen_ref_questions:
            continue
            
        # Try to find the column in the dataframe (case-insensitive)
        country_q_lower = country_q.lower()
        
        if country_q in df.columns:
            # Exact match
            mapped_df[ref_q] = df[country_q]
            found_mappings.append(f"{country_q} -> {ref_q}")
            seen_ref_questions.add(ref_q)
        elif country_q_lower in col_mapping_lower:
            # Case-insensitive match
            actual_col = col_mapping_lower[country_q_lower]
            mapped_df[ref_q] = df[actual_col]
            found_mappings.append(f"{actual_col} -> {ref_q}")
            seen_ref_questions.add(ref_q)
        else:
            # Column not found
            if country_q not in missing_mappings and country_q_lower not in [m.lower() for m in missing_mappings]:
                missing_mappings.append(f"{country_q} (for {ref_q})")
    
    print(f"  Mapped {len(found_mappings)} questions")
    if missing_mappings and len(missing_mappings) > 0:
        print(f"  Warning: {len(missing_mappings)} expected columns not found in dataset")
        if len(missing_mappings) <= 10:
            print(f"    Missing: {', '.join([m.split(' (')[0] for m in missing_mappings])}")
        else:
            print(f"    Missing: {', '.join([m.split(' (')[0] for m in missing_mappings[:10]])}... (and {len(missing_mappings)-10} more)")
    
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
    
    # Get reference questions (first column contains reference questions like q1, q2, etc.)
    ref_col = mapping_df.columns[0]  # 'Ref' column
    
    # Skip the second column if it's a description (like 'Question Concept')
    start_col_idx = 2 if len(mapping_df.columns) > 2 else 1
    
    # Iterate through country columns to create mappings
    for col in mapping_df.columns[start_col_idx:]:
        country_name = col.strip()
        country_mappings[country_name] = {}
        
        for idx, row in mapping_df.iterrows():
            ref_question = row[ref_col]
            country_question = row[col]
            
            # Skip if mapping is empty or NaN
            if pd.notna(ref_question) and pd.notna(country_question):
                ref_q_str = str(ref_question).strip()
                country_q_str = str(country_question).strip()
                
                if ref_q_str and country_q_str:
                    # Store both the original and lowercase version for case-insensitive matching
                    country_mappings[country_name][country_q_str] = ref_q_str
                    # Also add lowercase version as key
                    country_mappings[country_name][country_q_str.lower()] = ref_q_str
    
    return country_mappings

def map_csv_filename_to_country(csv_filename):
    """
    Map CSV filename to country name in the mapping Excel.
    Returns: country name string
    """
    # Extract country name from filename to match Excel column names
    # The Excel has columns like: 'Mauritius, 2019', 'Thailand 2021', etc.
    
    name_mappings = {
        'Bangladesh_22014.csv': 'Bangladesh 2014',
        'Brunei_Darussalam_2019.csv': 'Brunei Darussalam 2019',
        'MUS_Rodrigues_2019_GSHS.csv': 'Mauritius, 2019',
        'Nepal_2015.csv': 'Nepal 2015',
        'Panama_2018.csv': 'Panama 2018',
        'Saint_Lucia_2018.csv': 'Saint Lucia 2018',
        'Thailand_2015.csv': 'Thailand 2014',
        'Thailand-2021.csv': 'Thailand 2021',
        'Timor_leste_2015.csv': 'Timor-Leste 2014',
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
        
        # Find exact matching mapping first, then try partial match
        mapping = None
        matched_country = None
        
        # First try exact match (case-insensitive)
        for map_country, map_dict in country_mappings.items():
            if map_country.lower() == country_name.lower():
                mapping = map_dict
                matched_country = map_country
                break
        
        # If no exact match, try partial match
        if not mapping:
            for map_country, map_dict in country_mappings.items():
                if (map_country.lower() in country_name.lower() or 
                    country_name.lower() in map_country.lower()):
                    mapping = map_dict
                    matched_country = map_country
                    break
        
        if mapping and len(mapping) > 0:
            print(f"\n{'='*60}")
            print(f"Matched '{csv_file.name}' to mapping column '{matched_country}'")
            try:
                result_df = preprocess_dataset(csv_file, output_file, mapping, country_name)
                results[country_name] = {
                    'status': 'success',
                    'rows': len(result_df),
                    'columns': len(result_df.columns)
                }
            except Exception as e:
                print(f"  Error processing {country_name}: {e}")
                import traceback
                traceback.print_exc()
                results[country_name] = {'status': 'error', 'message': str(e)}
        else:
            print(f"\nSkipping {csv_file.name}: No mapping found for '{country_name}'")
            print(f"  Available mappings: {', '.join(country_mappings.keys())}")
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
