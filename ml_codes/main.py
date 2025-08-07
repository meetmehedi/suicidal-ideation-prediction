import os
import pandas as pd
from datetime import datetime
from data_preprocessing import load_and_preprocess_data, dataset_stats
from ml_models import smote_train

DATA_DIR = "datasets"
# Generate filename with international datetime format (ISO 8601)
current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
OUTPUT_CSV = f"summary_results_{current_datetime}.csv"

summary = []

# Loop through all CSV files in the datasets directory
for filename in os.listdir(DATA_DIR):
    if filename.endswith(".csv"):
        filepath = os.path.join(DATA_DIR, filename)
        dataset_name = os.path.splitext(filename)[0]

        print(f"\n\n=== Processing Dataset: {dataset_name} ===")
        
        # Load, preprocess, and collect stats
        df, pre_stats, post_stats = load_and_preprocess_data(filepath, return_stats=True)
        
        # Skip dataset if no relevant columns found
        if df is None:
            print(f"Skipping dataset {dataset_name} - no relevant columns found")
            continue
            
        X = df.drop(columns=["suicide"])
        y = df["suicide"]

        # Train and evaluate models
        metrics = smote_train(X, y, return_metrics=True)

        # Combine all into one row
        row = {
            "Dataset": dataset_name,
            **{f"Pre-{k}": v for k, v in pre_stats.items()},
            **{f"Post-{k}": v for k, v in post_stats.items()},
        }
        for model_name, scores in metrics.items():
            for metric_name, value in scores.items():
                row[f"{model_name}_{metric_name}"] = value

        summary.append(row)

# Save summary
pd.DataFrame(summary).to_csv(OUTPUT_CSV, index=False)
print(f"\nAll results saved to '{OUTPUT_CSV}'")
