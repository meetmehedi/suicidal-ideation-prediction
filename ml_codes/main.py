# main.py
from data_preprocessing import load_and_preprocess_data
from ml_models import (
    original_version_train,
    smote_train,
    classweight_train,
    smote_and_classweight_train
)

# Load and preprocess data
df = load_and_preprocess_data("BGD2014_Public_Use.csv")

# Split features and target
X = df.drop(columns=["suicide"])
y = df["suicide"]

print(f"Total samples: {len(df)}")
print(f"Number of 1s in suicide column: {y.value_counts().get(1, 0)}")
print(f"Number of 2s in suicide column: {y.value_counts().get(2, 0)}")

# Train models
print("Starting training with original version...")
original_version_train(X, y)

print("Starting training with SMOTE version...")
smote_train(X, y)

print("Starting training with class weight version...")
classweight_train(X, y)

print("Starting training with SMOTE and class weight version...")
smote_and_classweight_train(X, y)
