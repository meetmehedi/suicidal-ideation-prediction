    # Shuffle merged dataset
import pandas as pd
from ml_models import smote_train

merged_df = pd.read_csv("merged_dataset.csv")
merged_df = merged_df.sample(frac=1, random_state=42).reset_index(drop=True)

X = merged_df.drop(columns=["suicide"])
y = merged_df["suicide"]

trained_models, model_scores = smote_train(X, y, return_metrics=True)