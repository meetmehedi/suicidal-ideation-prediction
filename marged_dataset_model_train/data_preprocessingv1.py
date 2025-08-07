# data_preprocessing.py
import os
import pandas as pd
from scipy.__config__ import show
from sklearn.impute import KNNImputer

targeted_fields = {
    "q1": "Custom Age",
    "q2": "Sex",
    "q3": "In what grade are you",
    "q10": "Fast food eating",
    "q11": "Tooth brushing",
    "q12": "Hand washing before eating",
    "q13": "Hand washing after toilet",
    "q14": "Hand washing with soap",
    "q15": "Physically attacked",
    "q20": "Bullied",
    "q22": "Felt lonely",
    "q23": "Could not sleep",
    "q24": "Considered suicide",
    "q25": "Made a suicide plan",
    "q26": "Attempted suicide",
    "q27": "Close friends",
    "q28": "Initiation of cigarette use",
    "q29": "Current cigarette use",
    "q35": "Current alcohol use",
    "q40": "Initiation of drug use",
    "q44": "Ever sexual intercourse",
    "q49": "Physical activity >= 5 days",
    "q53": "Miss school no permission",
    "q54": "Other students kind and helpful",
    "q56": "Parents understand problems",
    "q57": "Parents know about free time",
}


def load_and_preprocess_data():
    # Initialize empty dataframe
    df = pd.DataFrame()
    
    print(f"Loading and merging datasets from datasets folder...")
    print("=" * 50)
    
    # Get list of CSV files in datasets folder
    dataset_files = [file for file in os.listdir("datasets") if file.endswith(".csv")]
    
    if not dataset_files:
        print("No CSV files found in datasets folder!")
        return None
    
    # Load and merge each dataset
    for i, file in enumerate(dataset_files, 1):
        print(f"[{i}/{len(dataset_files)}] Loading dataset: {file}")
        
        # Load dataset
        temp_df = pd.read_csv(f"datasets/{file}")
        print(f"   - Original shape: {temp_df.shape}")
        
        # Convert column names to lowercase
        temp_df.columns = temp_df.columns.str.lower()
        print(f"   - Converted column names to lowercase")
        
        # Keep only targeted fields that exist in the dataset
        available_fields = [col for col in targeted_fields.keys() if col in temp_df.columns]
        missing_fields = [col for col in targeted_fields.keys() if col not in temp_df.columns]
        
        if available_fields:
            temp_df = temp_df[available_fields]
            print(f"   - Extracted {len(available_fields)} targeted fields")
            if missing_fields:
                print(f"   - Missing fields: {missing_fields}")
        else:
            print(f"   - Warning: No targeted fields found in this dataset!")
            continue
        
        # Merge with main dataframe
        if df.empty:
            df = temp_df.copy()
        else:
            df = pd.concat([df, temp_df], ignore_index=True)
        
        print(f"   - Successfully loaded and merged. Current total shape: {df.shape}")
        print(f"   - Dataset '{file}' processed successfully!")
        print("-" * 40)
    
    print(f"\n✓ All datasets loaded and merged successfully!")
    print(f"✓ Final merged dataset shape: {df.shape}")
    print(f"✓ Total records: {len(df)}")
    print(f"✓ Available columns: {list(df.columns)}")
    print("=" * 50)


    print("\nBefore imputation:")
    # showing loaded dataset information
    show_dataset_info(df)

    # KNN imputation
    imputer = KNNImputer(n_neighbors=len(df) - 1)
    df = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)

    print("\nAfter imputation:")
    # showing imputed dataset information
    show_dataset_info(df)

    # Create "suicide" label
    df["suicide"] = df.apply(
        lambda row: 1 if (row["q24"] == 1 or row["q25"] == 1 or row["q26"] != 1) else 0, axis=1
    )

    # Drop the original suicide-related columns
    df = df.drop(columns=["q24", "q25", "q26"])

    return df

def show_dataset_info(df):
    """
    Displays detailed information about the dataset.
    
    Parameters:
    - df: pandas DataFrame
    """
    print("--- Dataset Basic Info ---")
    print(f"Shape: {df.shape[0]} rows, {df.shape[1]} columns\nTotal number of data = {df.count().sum()}")

    missing = df.isnull().sum()
    total_missing = missing.sum()
    print(f"Total missing values in dataset: {total_missing}")



