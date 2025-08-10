# main.py
import os
import pandas as pd
from datetime import datetime
from data_preprocessing import load_and_preprocess_data
from ml_models import smote_train
import joblib

# =====================================================
# Configuration
# =====================================================
DATA_DIR = "datasets"

# Generate filename with international datetime format (ISO 8601)
current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
OUTPUT_CSV = f"summary_results_{current_datetime}.csv"

# Store evaluation summaries (future use if needed)
summary = []

# Default properties (can be modified by user input)
PROPERTIES = {
    'merge_datasets': False,
    'save_graphs': True,
    'save_models': True,
    'model_dir': 'trained_models',
    'graphs_dir': 'model_graphs',
    'save_merged_dataset': False,
    'data_dir': DATA_DIR,
}


# =====================================================
# Initialize User Settings
# =====================================================
def initialize_properties():
    """
    Ask user for training settings.
    This lets them control whether to merge datasets, save models, graphs, etc.
    """
    print("\n=== ML Training Configuration ===")
    print("Press Enter to use the default option shown in brackets.\n")

    def ask_yes_no(prompt, default="no"):
        """Ask a yes/no question, return True for yes, False for no."""
        valid = ['yes', 'no', 'y', 'n', '']
        default_bool = default.lower() in ['yes', 'y']

        while True:
            answer = input(f"{prompt} (yes/no) [{default}]: ").strip().lower()
            if answer in valid:
                return answer in ['yes', 'y'] if answer else default_bool
            print("⚠️ Please enter 'yes' or 'y' or 'no' or 'n' or press Enter for default.")

    # Questions
    PROPERTIES['merge_datasets'] = ask_yes_no("Merge datasets?", default="no")
    if PROPERTIES['merge_datasets']:
        print("💡 Merging datasets will increase training time and memory usage.\n")
        # Ask if they want to save the merged dataset when merging true
        PROPERTIES['save_merged_dataset'] = ask_yes_no("Save merged dataset as CSV?", default="no")
        if PROPERTIES['save_merged_dataset']:
            print("💾 Merged dataset will be saved as 'merged_dataset.csv'.\n")

    PROPERTIES['save_graphs'] = ask_yes_no("Save confusion matrix & ROC curve?", default="yes")
    PROPERTIES['save_models'] = ask_yes_no("Save model as .pkl file?", default="yes")



# =====================================================
# Main Training Function
# =====================================================
def loadPreprocessTrain():
    """
    Load, preprocess, and train models on datasets.
    If merging is enabled, datasets will be combined before training.
    """

    merged_df = None  # Will store merged dataset if required

    for filename in os.listdir(PROPERTIES['data_dir']):
        if filename.endswith(".csv"):
            filepath = os.path.join(PROPERTIES['data_dir'], filename)
            dataset_name = os.path.splitext(filename)[0]

            print("\n" + "="*20 + f" Processing Dataset: {dataset_name} " + "="*20)
            # Load and preprocess
            df = load_and_preprocess_data(filepath)
            if df is None:
                print(f"⚠️ Skipping {dataset_name} - no relevant columns found.")
                continue

            # Shuffle dataset
            df = df.sample(frac=1, random_state=42).reset_index(drop=True)

            # Store for merging if required
            if PROPERTIES['merge_datasets']:
                merged_df = df if merged_df is None else pd.concat([merged_df, df], ignore_index=True)

            # Prepare features & target
            X = df.drop(columns=["suicide"])
            y = df["suicide"]

            # Train models
            print("\n" + "="*20 + f" Training Models for : {dataset_name} " + "="*20)
            trained_models = smote_train(X, y)

            # Save only Extra Trees model
            if PROPERTIES['save_models'] and trained_models and 'ExtraTrees' in trained_models:
                os.makedirs(PROPERTIES['model_dir'], exist_ok=True)
                model_filename = os.path.join(PROPERTIES['model_dir'], f"{dataset_name}_extra_trees.pkl")
                try:
                    joblib.dump(trained_models['ExtraTrees'], model_filename)
                    print(f"✅ Saved Extra Trees model: {model_filename}")
                except Exception as e:
                    print(f"❌ Error saving model: {e}")

    # If merging enabled, train on merged dataset
    if PROPERTIES['merge_datasets'] and merged_df is not None:
        loadPreprocessTrainMergedDataset(merged_df)


# =====================================================
# Training on Merged Dataset
# =====================================================
def loadPreprocessTrainMergedDataset(merged_df):
    """
    Train models on merged dataset.
    Optionally save dataset and model.
    """
    print("\n" + "="*20 + " Working on Merged Dataset " + "="*20)

    # Shuffle merged dataset
    merged_df = merged_df.sample(frac=1, random_state=42).reset_index(drop=True)

    X = merged_df.drop(columns=["suicide"])
    y = merged_df["suicide"]

    # show basic info about merged_df
    print(f"\n📊 Dataset States ")
    print(f"Rows: {merged_df.shape[0]}")
    print(f"Columns: {merged_df.shape[1]}")
    print(f"Total Elements: {merged_df.count().sum()}")

    trained_models = smote_train(X, y)

    # Save Extra Trees model
    if PROPERTIES['save_models'] and trained_models and 'ExtraTrees' in trained_models:
        os.makedirs(PROPERTIES['model_dir'], exist_ok=True)
        model_filename = os.path.join(PROPERTIES['model_dir'], "merged_extra_trees.pkl")
        try:
            joblib.dump(trained_models['ExtraTrees'], model_filename)
            print(f"✅ Saved merged Extra Trees model: {model_filename}")
        except Exception as e:
            print(f"❌ Error saving model: {e}")

    # Save merged dataset
    if PROPERTIES['save_merged_dataset']:
        try:
            merged_df.to_csv("merged_dataset.csv", index=False)
            print("💾 Saved merged dataset: merged_dataset.csv")
        except Exception as e:
            print(f"❌ Error saving merged dataset: {e}")


# =====================================================
# Main Execution
# =====================================================
def main():
    initialize_properties()
    loadPreprocessTrain()


if __name__ == '__main__':
    main()
