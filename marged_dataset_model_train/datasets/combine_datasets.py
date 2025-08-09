import pandas as pd
import glob
import os
from pathlib import Path

def merge_csv_files(input_folder=".", output_file="combined_data.csv", pattern="*.csv"):
    """
    Merge multiple CSV files into one combined CSV file.
    
    Parameters:
    input_folder (str): Path to folder containing CSV files (default: current directory)
    output_file (str): Name of the output combined CSV file
    pattern (str): File pattern to match (default: "*.csv")
    """
    
    try:
        # Get list of all CSV files in the specified folder
        csv_files = glob.glob(os.path.join(input_folder, pattern))
        
        if not csv_files:
            print(f"No CSV files found in '{input_folder}' matching pattern '{pattern}'")
            return
        
        print(f"Found {len(csv_files)} CSV files to merge:")
        for file in csv_files:
            print(f"  - {os.path.basename(file)}")
        
        # List to store individual dataframes
        dataframes = []
        
        # Read each CSV file and add to list
        for file in csv_files:
            try:
                df = pd.read_csv(file)
                # convert column names to lowercase
                df.columns = df.columns.str.lower()
                # Add a column to identify source file (optional)
                df['source_file'] = os.path.basename(file)
                dataframes.append(df)
                print(f"✓ Successfully read {os.path.basename(file)} - {len(df)} rows")
            except Exception as e:
                print(f"✗ Error reading {os.path.basename(file)}: {str(e)}")
                continue
        
        if not dataframes:
            print("No CSV files could be read successfully.")
            return
        
        # Combine all dataframes
        print("\nMerging CSV files...")
        combined_df = pd.concat(dataframes, ignore_index=True, sort=False)
        
        # Save combined dataframe to new CSV file
        combined_df.to_csv(output_file, index=False)
        
        print(f"\n✓ Successfully merged {len(dataframes)} files!")
        print(f"✓ Combined CSV saved as: {output_file}")
        print(f"✓ Total rows in combined file: {len(combined_df)}")
        print(f"✓ Total columns in combined file: {len(combined_df.columns)}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    # Example usage - Basic merge
    print("=== BASIC CSV MERGE ===")
    merge_csv_files(
        input_folder=".",  # Current directory
        output_file="merged_data.csv"
    )
    
    # Example for specific folder
    # merge_csv_files(
    #     input_folder="./data",
    #     output_file="combined_dataset.csv",
    #     pattern="*.csv"
    # )