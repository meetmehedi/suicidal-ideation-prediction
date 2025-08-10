# smote_training.py

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


def smote_train(X, y, return_metrics=False):
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
    print_class_distribution(y, "Original")

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

    print("\nModel training completed.")
    evaluate_models(models, X_test, y_test)

    return (models, model_scores) if return_metrics else models


def evaluate_models(models, X_test, y_test):
    """Evaluate trained models and print results."""
    for name, model in models.items():
        X_input = X_test.values if name == "TabNet" else X_test
        y_pred = model.predict(X_input)
        y_proba = model.predict_proba(X_input)[:, 1] if hasattr(model, "predict_proba") else None

        print(f"\n{name} Accuracy: {accuracy_score(y_test, y_pred):.4f}")
        print(f"{name} Confusion Matrix:\n{confusion_matrix(y_test, y_pred)}")
        print(f"{name} Classification Report:\n{classification_report(y_test, y_pred)}")

        try:
            from main import PROPERTIES
            if PROPERTIES.get("save_graphs", False):
                print(f"Saving graphs")
                save_confusion_matrix(y_test, y_pred, name, f"{name.lower()}_confusion_matrix.png")
                if y_proba is not None:
                    save_roc_curve(y_test, y_proba, name, f"{name.lower()}_roc_curve.png")
        except ImportError:
            print("Note: 'main.PROPERTIES' not found. Skipping graph saving.")


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


def save_roc_curve(y_true, y_proba, model_name, filename):
    """Save a ROC curve plot."""
    fpr, tpr, _ = roc_curve(y_true, y_proba)
    roc_auc = auc(fpr, tpr)

    plt.figure(figsize=(7, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'AUC = {roc_auc:.2f}')
    plt.plot([0, 1], [0, 1], color='navy', linestyle='--')
    plt.title(f'{model_name} ROC Curve')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.legend(loc='lower right')
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
