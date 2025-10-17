# smote_training.py

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix, roc_curve, auc
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import label_binarize

from imblearn.over_sampling import SMOTE

from sklearn.ensemble import ExtraTreesClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.neural_network import MLPClassifier

from xgboost import XGBClassifier
from pytorch_tabnet.tab_model import TabNetClassifier


def print_class_distribution(y, label=""):
    """Prints class distribution of a target variable."""
    print(f"\n{label} Class Distribution:")
    print(pd.Series(y).value_counts())


def smote_train(X, y, PROPERTIES: dict, return_metrics=False):
    """
    Train multiple models using SMOTE oversampling to balance the dataset.
    
    Parameters:
        X (pd.DataFrame): Features
        y (pd.Series): Target labels
        return_metrics (bool): Whether to return performance metrics dictionary.
        
    Returns:
        dict | None: Trained models and optionally performance metrics.
    """

    # Before SMOTE
    print(f"Original dataset size: {len(X)}")
    class_dist = pd.Series(y).value_counts()
    print_class_distribution(y, "Original")

    # Store class distribution
    metrics_dict = {
        'Class_0_Samples': int(class_dist.get(0, 0)),
        'Class_1_Samples': int(class_dist.get(1, 0))
    }

    # Apply SMOTE
    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X, y)

    # After SMOTE
    print(f"\nSMOTED dataset size: {len(X_resampled)}")
    print_class_distribution(y_resampled, "SMOTED")

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X_resampled, y_resampled,
        test_size=0.2, random_state=42, stratify=y_resampled
    )

    # Model definitions
    models = {
        "ExtraTrees": ExtraTreesClassifier(random_state=42),
        "SVM": SVC(random_state=42, probability=True),
        "LogisticRegression": LogisticRegression(max_iter=1000, random_state=42),
        "QDA": QuadraticDiscriminantAnalysis(),
        "MLP": MLPClassifier(random_state=42, max_iter=1000),
        "XGBoost": XGBClassifier(
            random_state=42, eval_metric='logloss'
        ),
        "TabNet": TabNetClassifier(verbose=0, seed=42),
    }

    model_scores = {}
    print("\nTraining models...")

    for name, model in models.items():
        # TabNet requires NumPy arrays
        X_train_input = X_train.values if name == "TabNet" else X_train
        y_train_input = y_train.values if name == "TabNet" else y_train
        X_test_input = X_test.values if name == "TabNet" else X_test

        if name == "TabNet":
            model.fit(
                X_train_input, y_train_input,
                eval_set=[(X_test.values, y_test.values)],
                patience=20, max_epochs=200, batch_size=1024
            )
        else:
            model.fit(X_train_input, y_train_input)

        # Predictions
        y_pred = model.predict(X_test_input)
        y_proba = model.predict_proba(X_test_input)[:, 1] if hasattr(model, "predict_proba") else None

        # Save performance
        model_scores[name] = {
            "Accuracy": round(accuracy_score(y_test, y_pred), 4),
            "Precision": round(precision_score(y_test, y_pred), 4),
            "Recall": round(recall_score(y_test, y_pred), 4),
            "F1": round(f1_score(y_test, y_pred), 4),
        }
        if name == "ExtraTrees":
            print(f"Feature Importances for {name}:")
            importances = pd.Series(model.feature_importances_, index=X_train.columns).sort_values(ascending=False)
            print(importances)
    print("\nModel training completed.")
    evaluate_models(models, PROPERTIES, X_test, y_test)

    # Add model metrics to metrics_dict (which already has class distribution)
    for name, scores in model_scores.items():
        metrics_dict[f"{name}_Accuracy"] = scores["Accuracy"]
        metrics_dict[f"{name}_Precision"] = scores["Precision"]
        metrics_dict[f"{name}_Recall"] = scores["Recall"]
        metrics_dict[f"{name}_F1"] = scores["F1"]

    return (models, metrics_dict) if return_metrics else (models, metrics_dict)


def evaluate_models(models, PROPERTIES: dict, X_test, y_test):
    """Evaluate trained models and print results."""
    # Store ROC data for combined plot
    roc_data = {}
    
    for name, model in models.items():
        X_input = X_test.values if name == "TabNet" else X_test
        y_pred = model.predict(X_input)
        y_proba = model.predict_proba(X_input)[:, 1] if hasattr(model, "predict_proba") else None

        print(f"\n{name} Accuracy: {accuracy_score(y_test, y_pred):.4f}")
        print(f"{name} Confusion Matrix:\n{confusion_matrix(y_test, y_pred)}")
        print(f"{name} Classification Report:\n{classification_report(y_test, y_pred)}")

        # Store ROC data for combined plot
        if y_proba is not None:
            fpr, tpr, _ = roc_curve(y_test, y_proba)
            roc_auc = auc(fpr, tpr)
            roc_data[name] = {'fpr': fpr, 'tpr': tpr, 'auc': roc_auc}

        try:
            if PROPERTIES.get("save_graphs", False):
                dataset_name = PROPERTIES.get("current_dataset_name", "unknown")
                graphs_dir = PROPERTIES.get("graphs_dir", "model_graphs")
                # Create dataset-specific directory
                dataset_graphs_dir = os.path.join(graphs_dir, dataset_name)
                os.makedirs(dataset_graphs_dir, exist_ok=True)
                print(f"Saving graphs for {dataset_name}")
                save_confusion_matrix(y_test, y_pred, name, os.path.join(dataset_graphs_dir, f"{name.lower()}_cm.png"))
        except ImportError:
            print("Note: 'main.PROPERTIES' not found. Skipping graph saving.")
    
    # Save combined ROC curve after evaluating all models
    try:
        if PROPERTIES.get("save_graphs", False) and roc_data:
            dataset_name = PROPERTIES.get("current_dataset_name", "unknown")
            graphs_dir = PROPERTIES.get("graphs_dir", "model_graphs")
            # Create dataset-specific directory
            dataset_graphs_dir = os.path.join(graphs_dir, dataset_name)
            os.makedirs(dataset_graphs_dir, exist_ok=True)
            print(f"Saving combined ROC curve for {dataset_name}")
            save_combined_roc_curve(roc_data, os.path.join(dataset_graphs_dir, "combined_roc_curve.png"))
    except ImportError:
        print("Note: 'main.PROPERTIES' not found. Skipping combined ROC curve saving.")


def save_confusion_matrix(y_true, y_pred, model_name, filename):
    """Save a confusion matrix heatmap."""
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=[1, 2], yticklabels=[1, 2])
    plt.title(f'{model_name} Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


def save_combined_roc_curve(roc_data, filename):
    """Save a combined ROC curve plot for all models."""
    plt.figure(figsize=(10, 8))
    
    # Define colors for different models
    colors = ['darkorange', 'red', 'green', 'blue', 'purple', 'brown', 'pink']
    
    for i, (model_name, data) in enumerate(roc_data.items()):
        color = colors[i % len(colors)]
        plt.plot(data['fpr'], data['tpr'], color=color, lw=2, 
                label=f'{model_name} (AUC = {data["auc"]:.3f})')
    
    # Plot diagonal line (random classifier)
    plt.plot([0, 1], [0, 1], color='navy', linestyle='--', lw=2, label='Random Classifier (AUC = 0.5)')
    
    plt.title('Combined ROC Curves for All Models', fontsize=16)
    plt.xlabel('False Positive Rate', fontsize=14)
    plt.ylabel('True Positive Rate', fontsize=14)
    plt.legend(loc='lower right', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Combined ROC curve saved as '{filename}'")
