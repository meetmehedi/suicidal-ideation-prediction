# ml_models.py

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    roc_curve,
    auc,
)
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import label_binarize

# Core Models (1 per category)
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.neural_network import MLPClassifier

from xgboost import XGBClassifier
from pytorch_tabnet.tab_model import TabNetClassifier

import numpy as np
import torch


# ------------------------- Confusion Matrix Plot -------------------------
def save_confusion_matrix(y_true, y_pred, model_name, filename):
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=[1, 2], yticklabels=[1, 2])
    plt.title(f'{model_name} Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.savefig(filename)
    plt.close()


# ------------------------- ROC Curve Plot -------------------------
def save_roc_curve(y_true, y_proba, model_name, filename):
    y_true_bin = label_binarize(y_true, classes=[1, 2]).ravel()
    fpr, tpr, _ = roc_curve(y_true_bin, y_proba)
    roc_auc = auc(fpr, tpr)

    plt.figure(figsize=(7, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'AUC = {roc_auc:.2f}')
    plt.plot([0, 1], [0, 1], color='navy', linestyle='--')
    plt.title(f'{model_name} ROC Curve')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.legend(loc='lower right')
    plt.savefig(filename)
    plt.close()


# ------------------------- Train and Evaluate Selected Models -------------------------
def smote_train(X, y):
    print("\n[SMOTE Version: With SMOTE, No Class Weight]\n")
    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X, y)

    X_train, X_test, y_train, y_test = train_test_split(
        X_resampled, y_resampled, test_size=0.2, random_state=42, stratify=y_resampled
    )

    # One model per category
    models = {
        "Extra Trees": ExtraTreesClassifier(random_state=42),
        "SVM": SVC(random_state=42, probability=True),
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "QDA": QuadraticDiscriminantAnalysis(),
        "MLP": MLPClassifier(random_state=42, max_iter=1000),
        "XGBoost": XGBClassifier(random_state=42, use_label_encoder=False, eval_metric='logloss'),
        "TabNet": TabNetClassifier(verbose=0, seed=42),
    }

    # Fit models (TabNet separately due to numpy requirement)
    for name, model in models.items():
        if name == "TabNet":
            model.fit(
                X_train.values, y_train.values,
                eval_set=[(X_test.values, y_test.values)],
                patience=20,
                max_epochs=200,
                batch_size=1024,
            )
        else:
            model.fit(X_train, y_train)

    evaluate_models(models, X_test, y_test)


# ------------------------- Evaluation -------------------------
def evaluate_models(models, X_test, y_test):
    for name, model in models.items():
        X_input = X_test.values if name == "TabNet" else X_test
        y_pred = model.predict(X_input)
        y_proba = model.predict_proba(X_input)[:, 1]

        print(f"\n{name} Accuracy:", accuracy_score(y_test, y_pred))
        print(f"{name} Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
        print(f"{name} Classification Report:\n", classification_report(y_test, y_pred))

        short_name = name.lower().replace(" ", "_")
        save_confusion_matrix(y_test, y_pred, name, f"{short_name}_confusion_matrix.png")
        save_roc_curve(y_test, y_proba, name, f"{short_name}_roc_curve.png")
