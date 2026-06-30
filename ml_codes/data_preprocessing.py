# data_preprocessing.py
import pandas as pd
from sklearn.impute import KNNImputer

# =====================================================
# Targeted Columns Mapping
# =====================================================
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

# Suicide-indicator columns (used for label creation, then dropped)
SUICIDE_COLS = ["q24", "q25", "q26"]


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
    Loads and preprocesses a dataset — reviewer-compliant version.

    Pipeline (leakage-free):
      1. Read CSV
      2. Filter to targeted columns
      3. Build 'suicide' label from RAW q24/q25/q26 (before imputation)
      4. Drop q24/q25/q26 from feature set
      5. KNN-impute (k=5) ONLY on feature columns
      6. Re-attach label

    Returns:
      (DataFrame, stats_dict) or (None, None) on failure
    """
    print(f"\n📂 Loading dataset: {filepath}")
    df = pd.read_csv(filepath)

    # Normalise column names
    df.columns = df.columns.str.lower()

    # Identify available & missing targeted columns
    available_cols = [col for col in targeted_fields if col in df.columns]
    missing_cols   = [col for col in targeted_fields if col not in df.columns]

    if missing_cols:
        print(f"⚠️  Missing targeted columns: {missing_cols}")
    print(f"✅ Found {len(available_cols)}/{len(targeted_fields)} targeted columns.")

    df = df[available_cols]

    if df.empty:
        print("❌ No targeted columns found. Skipping this dataset.")
        return None, None

    # ── Step 1: Check suicide columns exist ──────────────────────────────────
    available_suicide_cols = [c for c in SUICIDE_COLS if c in df.columns]
    if len(available_suicide_cols) < 3:
        print(f"⚠️  Missing suicide columns. Found: {available_suicide_cols}. Skipping.")
        return None, None

    print(f"✅ All suicide-related columns found: {available_suicide_cols}")

    # ── Step 2: Build label from RAW values (no imputation yet) ──────────────
    def create_suicide_target(row):
        """
        Positive (1) if the student:
          - considered suicide  (q24 == 1), OR
          - made a plan         (q25 == 1), OR
          - attempted ≥1 time   (q26 >  1; value 1 means "0 attempts")
        """
        if row["q24"] == 1:
            return 1
        if row["q25"] == 1:
            return 1
        if row["q26"] > 1:
            return 1
        return 0

    suicide_target = df.apply(create_suicide_target, axis=1)

    # ── Step 3: Drop outcome columns BEFORE imputation ───────────────────────
    feature_df = df.drop(columns=available_suicide_cols)

    # Pre-imputation statistics
    print_dataset_states(feature_df, "Before Imputation (features only)")
    stats = {
        "Pre-Rows":           len(feature_df),
        "Pre-Columns":        feature_df.shape[1] + len(available_suicide_cols),
        "Pre-Total Elements": int(feature_df.count().sum()),
        "Pre-Missing Cells":  int(feature_df.isnull().sum().sum()),
    }

    # ── Step 4: KNN impute features ONLY (k=5, reviewer-recommended) ─────────
    try:
        imputer   = KNNImputer(n_neighbors=5)
        feature_df = pd.DataFrame(
            imputer.fit_transform(feature_df),
            columns=feature_df.columns,
        )
    except Exception as e:
        print(f"❌ KNN imputation failed: {e}")
        return None, None

    print_dataset_states(feature_df, "After KNN Imputation (features only)")

    # ── Step 5: Re-attach label ───────────────────────────────────────────────
    feature_df["suicide"] = suicide_target.values

    print("🆕 'suicide' target column created and attached.")
    print_dataset_states(feature_df, "Final Processed Dataset")

    # Post stats
    stats["Post-Rows"]           = feature_df.shape[0]
    stats["Post-Columns"]        = feature_df.shape[1]
    stats["Post-Total Elements"] = int(feature_df.count().sum())
    stats["Post-Missing Cells"]  = int(feature_df.isnull().sum().sum())

    return feature_df, stats


