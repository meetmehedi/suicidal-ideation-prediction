"""
Master script to run the complete preprocessing workflow.
Runs all preprocessing steps in sequence.
"""

import subprocess
import sys
from pathlib import Path

def run_script(script_name, description):
    """Run a Python script and return success status."""
    print("\n" + "="*80)
    print(f"{description}")
    print("="*80)
    
    script_path = Path(__file__).parent / script_name
    
    if not script_path.exists():
        print(f"❌ Error: Script not found: {script_path}")
        return False
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            check=True,
            capture_output=False
        )
        print(f"\n✓ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error running {script_name}: {e}")
        return False

def main():
    print("="*80)
    print("GSHS COMPLETE PREPROCESSING WORKFLOW")
    print("="*80)
    print("\nThis script will run the complete preprocessing pipeline:")
    print("  1. View mapping details")
    print("  2. Preprocess all datasets")
    print("  3. Merge converted datasets")
    print("\n" + "="*80)
    
    input("\nPress Enter to start the workflow...")
    
    # Step 1: View mapping details
    success = run_script(
        "view_mapping_details.py",
        "STEP 1/3: Viewing Mapping Details"
    )
    
    if not success:
        print("\n⚠ Warning: Could not display mapping details, but continuing...")
    
    # Step 2: Preprocess datasets
    success = run_script(
        "preprocess_datasets.py",
        "STEP 2/3: Preprocessing All Datasets"
    )
    
    if not success:
        print("\n❌ Preprocessing failed. Stopping workflow.")
        return
    
    # Step 3: Merge datasets
    success = run_script(
        "merge_datasets.py",
        "STEP 3/3: Merging Converted Datasets"
    )
    
    if not success:
        print("\n❌ Merging failed.")
        return
    
    # Final summary
    print("\n" + "="*80)
    print("WORKFLOW COMPLETE! ✓")
    print("="*80)
    
    base_dir = Path(__file__).parent
    
    print("\nGenerated files:")
    print("-"*80)
    
    # List converted files
    converted_dir = base_dir / 'data-sets' / 'converted-data-with-qustions'
    converted_files = list(converted_dir.glob('converted_*.csv'))
    print(f"\n📁 Converted datasets ({len(converted_files)} files):")
    print(f"   Location: {converted_dir}")
    
    # Unified dataset
    unified_file = base_dir / 'data-sets' / 'unified_dataset.csv'
    if unified_file.exists():
        file_size = unified_file.stat().st_size / (1024 * 1024)  # MB
        print(f"\n📊 Unified dataset:")
        print(f"   File: {unified_file}")
        print(f"   Size: {file_size:.2f} MB")
    
    # Reports
    mapping_report = base_dir / 'mapping_report.txt'
    summary_report = base_dir / 'data-sets' / 'unified_dataset_summary.txt'
    
    print(f"\n📄 Reports:")
    if mapping_report.exists():
        print(f"   - Mapping details: {mapping_report}")
    if summary_report.exists():
        print(f"   - Dataset summary: {summary_report}")
    
    print("\n" + "="*80)
    print("Next steps:")
    print("  • Review the unified dataset: data-sets/unified_dataset.csv")
    print("  • Check data quality: data-sets/unified_dataset_summary.txt")
    print("  • Use the unified dataset for machine learning or analysis")
    print("="*80)

if __name__ == "__main__":
    main()
