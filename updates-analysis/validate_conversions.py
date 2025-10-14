"""
Validation script for converted GSHS datasets.
Checks that all converted files have the same columns and expected structure.
"""

import pandas as pd
from pathlib import Path

def validate_converted_datasets():
    """
    Validate all converted GSHS datasets to ensure consistency.
    """
    # Define paths
    base_dir = Path(__file__).parent
    converted_dir = base_dir / 'data-sets' / 'converted-data-with-qustions'
    
    # Expected columns (27 reference questions)
    expected_columns = [
        'q1', 'q2', 'q3', 'q10', 'q11', 'q12', 'q13', 'q14', 'q15',
        'q20', 'q22', 'q23', 'q24', 'q25', 'q26', 'q27', 'q28', 'q29',
        'q35', 'q40', 'q44', 'q49', 'q53', 'q54', 'q56', 'q57', 'q58'
    ]
    
    print("="*80)
    print("GSHS Converted Dataset Validation")
    print("="*80)
    print(f"\nExpected columns: {len(expected_columns)}")
    print(f"Columns: {', '.join(expected_columns)}\n")
    
    # Get all converted CSV files
    csv_files = sorted(list(converted_dir.glob('converted_*.csv')))
    
    if not csv_files:
        print("ERROR: No converted files found!")
        return False
    
    print(f"Found {len(csv_files)} converted files\n")
    
    all_valid = True
    validation_results = []
    
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file)
            
            # Check columns
            actual_columns = sorted(df.columns.tolist())
            expected_sorted = sorted(expected_columns)
            
            columns_match = actual_columns == expected_sorted
            
            # Get basic stats
            total_rows = len(df)
            missing_data = df.isnull().sum().sum()
            missing_percent = (missing_data / (total_rows * len(df.columns))) * 100
            
            # Check suicide-related questions (q24, q25, q26)
            suicide_questions = ['q24', 'q25', 'q26']
            suicide_responses = {}
            for sq in suicide_questions:
                if sq in df.columns:
                    non_null = df[sq].notna().sum()
                    suicide_responses[sq] = non_null
            
            result = {
                'file': csv_file.name,
                'valid': columns_match,
                'rows': total_rows,
                'columns': len(df.columns),
                'missing_percent': round(missing_percent, 2),
                'suicide_q_responses': suicide_responses
            }
            
            validation_results.append(result)
            
            if not columns_match:
                all_valid = False
                print(f"❌ {csv_file.name}")
                print(f"   ERROR: Column mismatch!")
                missing_cols = set(expected_sorted) - set(actual_columns)
                extra_cols = set(actual_columns) - set(expected_sorted)
                if missing_cols:
                    print(f"   Missing: {missing_cols}")
                if extra_cols:
                    print(f"   Extra: {extra_cols}")
            else:
                print(f"✅ {csv_file.name}")
                print(f"   Rows: {total_rows:,} | Columns: {len(df.columns)} | Missing: {missing_percent:.1f}%")
                print(f"   Suicide Q responses: q24={suicide_responses.get('q24', 0):,}, " +
                      f"q25={suicide_responses.get('q25', 0):,}, q26={suicide_responses.get('q26', 0):,}")
                
        except Exception as e:
            all_valid = False
            print(f"❌ {csv_file.name}")
            print(f"   ERROR: {str(e)}")
            validation_results.append({
                'file': csv_file.name,
                'valid': False,
                'error': str(e)
            })
        
        print()
    
    # Summary
    print("="*80)
    print("VALIDATION SUMMARY")
    print("="*80)
    
    valid_count = sum(1 for r in validation_results if r.get('valid', False))
    total_count = len(validation_results)
    
    print(f"\nTotal files: {total_count}")
    print(f"Valid files: {valid_count}")
    print(f"Invalid files: {total_count - valid_count}")
    
    if all_valid:
        print("\n✅ All datasets passed validation!")
        
        # Calculate totals
        total_rows = sum(r['rows'] for r in validation_results if 'rows' in r)
        print(f"\nTotal records across all datasets: {total_rows:,}")
        
        # Suicide question summary
        print("\nSuicide-related questions summary:")
        for sq in ['q24', 'q25', 'q26']:
            total_responses = sum(r['suicide_q_responses'].get(sq, 0) 
                                 for r in validation_results if 'suicide_q_responses' in r)
            print(f"  {sq}: {total_responses:,} valid responses")
    else:
        print("\n❌ Some datasets failed validation. Please check the errors above.")
    
    print("="*80)
    
    return all_valid

if __name__ == "__main__":
    validate_converted_datasets()
