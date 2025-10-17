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

# Store evaluation summaries
summary_results = []

# Default properties (can be modified by user input)
PROPERTIES = {
    'merge_datasets': False,
    'save_graphs': False,
    'save_models': False,
    'save_results': False,
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

        # Convert default string to boolean properly
        if default.lower() in ['yes', 'y']:
            default_bool = True
        elif default.lower() in ['no', 'n']:
            default_bool = False
        else:
            default_bool = False  # fallback

        while True:
            answer = input(f"{prompt} (yes/no) [{default}]: ").strip().lower()
            if answer in valid:
                if answer == '':
                    return default_bool
                return answer in ['yes', 'y']
            print("⚠️ Please enter 'yes', 'y', 'no', 'n', or press Enter for default.")

    # Initialize PROPERTIES dictionary if not exists
    global PROPERTIES
    if 'PROPERTIES' not in globals():
        PROPERTIES = {}

    # Questions
    PROPERTIES['merge_datasets'] = ask_yes_no("Merge datasets?", default="no")
    if PROPERTIES['merge_datasets']:
        print("💡 Merging datasets will increase training time and memory usage.\n")
        PROPERTIES['save_merged_dataset'] = ask_yes_no("Save merged dataset as CSV?", default="no")
        if PROPERTIES['save_merged_dataset']:
            print("💾 Merged dataset will be saved as 'merged_dataset.csv'.\n")

    PROPERTIES['save_graphs'] = ask_yes_no("Save confusion matrix & ROC curve?", default="no")
    PROPERTIES['save_models'] = ask_yes_no("Save model as .pkl file?", default="no")
    PROPERTIES['save_results'] = ask_yes_no("Save results to CSV file?", default="no")
    if PROPERTIES['save_results']:
        print("💾 Results will be saved in 'summary_results_[datetime].csv'.\n")




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
            df, stats = load_and_preprocess_data(filepath)
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
            # Set current dataset name for graph saving
            PROPERTIES['current_dataset_name'] = dataset_name
            trained_models, model_scores = smote_train(X, y, PROPERTIES ,return_metrics=True)

            # Store results
            if PROPERTIES['save_results']:
                result_row = {"Dataset_Name": dataset_name}
                result_row.update(stats)
                result_row.update(model_scores)
                summary_results.append(result_row)

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

    # Set current dataset name for graph saving
    PROPERTIES['current_dataset_name'] = "merged_dataset"

    # Shuffle merged dataset
    merged_df = merged_df.sample(frac=1, random_state=42).reset_index(drop=True)

    X = merged_df.drop(columns=["suicide"])
    y = merged_df["suicide"]

    # Get merged dataset statistics
    merged_stats = {
        'Pre-Rows': merged_df.shape[0],
        'Pre-Columns': merged_df.shape[1] + 1,  # Add 1 for the suicide column we dropped
        'Pre-Total Elements': merged_df.count().sum() + len(merged_df),  # Add suicide column count
        'Pre-Missing Cells': 0,  # Already imputed in individual datasets
        'Post-Rows': merged_df.shape[0],
        'Post-Columns': merged_df.shape[1] + 1,
        'Post-Total Elements': merged_df.count().sum() + len(merged_df),
        'Post-Missing Cells': 0,
        'Class_0_Samples': int(y[y == 0].count()),
        'Class_1_Samples': int(y[y == 1].count())
    }

    # Show basic info about merged_df
    print(f"\n📊 Dataset States ")
    print(f"Rows: {merged_df.shape[0]}")
    print(f"Columns: {merged_df.shape[1] + 1}")
    print(f"Total Elements: {merged_df.count().sum() + len(merged_df)}")

    trained_models, model_scores = smote_train(X, y, return_metrics=True)

    # Store merged dataset results if results saving is enabled
    if PROPERTIES['save_results']:
        result_row = {"Dataset_Name": "merged_dataset"}
        result_row.update(merged_stats)
        result_row.update(model_scores)
        summary_results.append(result_row)

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
    
    # Save results to CSV if enabled
    if PROPERTIES['save_results'] and summary_results:
        try:
            results_df = pd.DataFrame(summary_results)
            results_df.to_csv(OUTPUT_CSV, index=False)
            print(f"\n💾 Results saved to: {OUTPUT_CSV}")
        except Exception as e:
            print(f"❌ Error saving results to CSV: {e}")


if __name__ == '__main__':
    main()
