# data_preprocessing.py
import pandas as pd
from sklearn.impute import KNNImputer

# =====================================================
# Targeted Columns Mapping
# =====================================================
# Maps question IDs to human-readable names (for developer reference)
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
    "q58": "Parents go through their things",
}


# =====================================================
# Helper: Print Dataset State
# =====================================================
def print_dataset_states(df, title="Dataset States"):
    """Prints key statistics about the dataset."""
    print(f"\n📊 {title}")
    print(f"   Rows: {df.shape[0]}")
    print(f"   Columns: {df.shape[1]}")
    print(f"   Total Non-NaN Elements: {df.count().sum()}")
    print(f"   Missing Values: {df.isnull().sum().sum()}")


# =====================================================
# Main Preprocessing Function
# =====================================================
def load_and_preprocess_data(filepath):
    """
    Loads and preprocesses a dataset.
    Steps:
      1. Reads CSV file
      2. Filters only targeted columns
      3. Imputes missing values (KNN)
      4. Creates 'suicide' target variable
    Returns:
      Tuple of (preprocessed DataFrame, stats_dict) or (None, None) if preprocessing is not possible
      where stats_dict contains pre and post processing statistics
    """
    print(f"\n📂 Loading dataset: {filepath}")
    df = pd.read_csv(filepath)

    # Convert column names to lowercase to avoid case mismatches
    df.columns = df.columns.str.lower()

    # Identify available & missing targeted columns
    available_cols = [col for col in targeted_fields if col in df.columns]
    missing_cols = [col for col in targeted_fields if col not in df.columns]

    if missing_cols:
        print(f"⚠️ Missing targeted columns: {missing_cols}")
    print(f"✅ Found {len(available_cols)}/{len(targeted_fields)} targeted columns.")

    # Keep only available targeted columns
    df = df[available_cols]

    # If no targeted columns found → skip dataset
    if df.empty:
        print("❌ No targeted columns found. Skipping this dataset.")
        return None

    # Before imputation statistics
    print_dataset_states(df, "Before Imputation")
    stats = {
        'Pre-Rows': len(df),
        'Pre-Columns': len(df.columns),
        'Pre-Total Elements': df.count().sum(),
        'Pre-Missing Cells': df.isnull().sum().sum(),
    }

    # Impute missing values using KNN
    try:
        imputer = KNNImputer(n_neighbors=len(df) - 1)  # Avoid too large k
        df = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)
    except Exception as e:
        print(f"❌ Error during KNN imputation: {e}")
        return None

    print_dataset_states(df, "After KNN Imputation")

    # Suicide-related columns
    suicide_cols = ["q24", "q25", "q26"]
    available_suicide_cols = [col for col in suicide_cols if col in df.columns]

    if len(available_suicide_cols) == 3:
        print(f"✅ All suicide-related columns found: {available_suicide_cols}")
    else:
        print(f"⚠️ Missing suicide-related columns. Found: {available_suicide_cols}")
        print("   Skipping this dataset.")
        return None

    # Create suicide target variable
    def create_suicide_target(row):
        """
        Returns:
            1 → if student considered suicide, made a plan, or attempted
            0 → otherwise
        """
        if row["q24"] == 1:  # Considered suicide
            return 1
        if row["q25"] == 1:  # Made a suicide plan
            return 1
        if row["q26"] > 1:   # Attempted suicide (1 = no attempt, >1 = attempts)
            return 1
        return 0

    df["suicide"] = df.apply(create_suicide_target, axis=1)

    # Remove original suicide-related columns to avoid leakage
    df.drop(columns=available_suicide_cols, inplace=True)

    print("🆕 'suicide' target column created successfully.")
    print_dataset_states(df, "Final Processed Dataset")

    # Collect statistics
    stats["Post-Rows"] = df.shape[0]
    stats["Post-Columns"] = df.shape[1]
    stats["Post-Total Elements"] = df.count().sum()
    stats["Post-Missing Cells"] = df.isnull().sum().sum()

    return df, stats
