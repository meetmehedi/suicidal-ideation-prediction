import pandas as pd
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


def dataset_stats(df):
    return {
        "Rows": df.shape[0],
        "Columns": df.shape[1],
        "Total Elements": df.count().sum(),
        "Missing Cells": df.isnull().sum().sum(),
    }


def load_and_preprocess_data(filepath, return_stats=False):
    df = pd.read_csv(filepath)
    
    # Convert all column names to lowercase
    df.columns = df.columns.str.lower()
    
    # Check which targeted columns are available in the dataset
    available_cols = [col for col in targeted_fields.keys() if col in df.columns]
    missing_cols = [col for col in targeted_fields.keys() if col not in df.columns]
    
    if missing_cols:
        print(f"Missing columns in dataset: {missing_cols}")
        print(f"Available columns: {len(available_cols)}/{len(targeted_fields)}")
    
    # Select only available columns
    df = df[available_cols]
    
    # Check if we have any columns left after filtering
    if len(df.columns) == 0:
        print("Error: No targeted columns found in dataset. Skipping this dataset.")
        if return_stats:
            return None, None, None
        return None
    
    print(len(df.columns))
    print(df.select_dtypes(exclude=['number']).columns
)
    pre_stats = dataset_stats(df)
    print(pre_stats)
    
    # Handle columns with all NaN values
    all_nan_cols = [col for col in df.columns if df[col].isnull().all()]
    if all_nan_cols:
        print(f"Columns with all NaN values: {all_nan_cols}")
        # Fill all-NaN columns with 0 before imputation
        for col in all_nan_cols:
            df[col] = 0
    
    imputer = KNNImputer(n_neighbors=len(df) - 1)
    df = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)

    post_stats = dataset_stats(df)

    # Create suicide target variable only if the required columns are available
    suicide_cols = ["q24", "q25", "q26"]
    available_suicide_cols = [col for col in suicide_cols if col in df.columns]
    
    if available_suicide_cols:
        def create_suicide_target(row):
            result = 0
            if "q24" in df.columns and pd.notna(row["q24"]) and row["q24"] == 1:  # Considered suicide
                result = 1
            if "q25" in df.columns and pd.notna(row["q25"]) and row["q25"] == 1:  # Made a suicide plan
                result = 1
            if "q26" in df.columns and pd.notna(row["q26"]) and row["q26"] == 1:  # Attempted suicide (assuming 1 means attempted)
                result = 1
            return result
        
        df["suicide"] = df.apply(create_suicide_target, axis=1)
        df = df.drop(columns=available_suicide_cols)
    else:
        print("Warning: No suicide-related columns (q24, q25, q26) available. Skipping suicide target creation.")
        # Create a dummy suicide column with all zeros
        df["suicide"] = 0

    if return_stats:
        return df, pre_stats, post_stats
    return df
