# main.py
from data_preprocessing import load_and_preprocess_data
from ml_models import (
    smote_train,
)

# Load and preprocess data
df = load_and_preprocess_data("BGD2014_Public_Use.csv")

# Split features and target
X = df.drop(columns=["suicide"])
y = df["suicide"]

print(f"\nNumber of 1s in suicide column: {y.value_counts().get(1, 0)}")
print(f"Number of 2s in suicide column: {y.value_counts().get(0, 0)}")
print(f"Total suicide samples: {len(df)}")

# Train models

print("Starting training with SMOTE version...")
smote_train(X, y)

