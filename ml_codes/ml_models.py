# ml_models.py  -- reviewer-compliant version
# Split: 64% train (SMOTE) | 16% val (raw) | 20% test (raw, imbalanced)

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report,
    roc_curve, auc, average_precision_score,
)
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE

from sklearn.ensemble import ExtraTreesClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier
from pytorch_tabnet.tab_model import TabNetClassifier


def print_class_distribution(y, label=""):
    print(f"\n{label} Class Distribution:")
    print(pd.Series(y).value_counts())


def _specificity(y_true, y_pred):
    """TN / (TN + FP)"""
    cm = confusion_matrix(y_true, y_pred)
    if cm.shape == (2, 2):
        tn, fp = cm[0, 0], cm[0, 1]
        return round(tn / (tn + fp + 1e-9), 4)
    return None


def smote_train(X, y, PROPERTIES: dict, return_metrics=False):
    """
    Reviewer-compliant training pipeline (no leakage).

    1. Stratified 80/20 -> trainval / test      (test NEVER touched by SMOTE)
    2. Stratified 80/20 -> train / val           (from trainval)
    3. SMOTE only on training set
    4. Train classifiers on resampled train
    5. Evaluate on raw imbalanced test set

    Metrics: Accuracy, Macro-F1, Precision, Sensitivity, Specificity, PR-AUC
    """
    print(f"\nOriginal dataset size: {len(X)}")
    class_dist = pd.Series(y).value_counts()
    print_class_distribution(y, "Original (full dataset)")

    metrics_dict = {
        "Class_0_Samples": int(class_dist.get(0, 0)),
        "Class_1_Samples": int(class_dist.get(1, 0)),
    }

    # Step 1 -- hold-out test set (20%, raw)
    X_trainval, X_test, y_trainval, y_test = train_test_split(
        X, y, test_size=0.20, stratify=y, random_state=42
    )

    # Step 2 -- validation set (16% of total, raw)
    X_train, X_val, y_train, y_val = train_test_split(
        X_trainval, y_trainval, test_size=0.20, stratify=y_trainval, random_state=42
    )

    print_class_distribution(y_train, "Train pre-SMOTE (64%)")
    print_class_distribution(y_val,   "Val  (raw 16%)")
    print_class_distribution(y_test,  "Test (raw 20%)")

    # Step 3 -- SMOTE on training only
    smote = SMOTE(random_state=42)
    X_train_res, y_train_res = smote.fit_resample(X_train, y_train)
    print(f"\nResampled training size: {len(X_train_res)}")
    print_class_distribution(y_train_res, "Train post-SMOTE")

    # Step 4 -- Model definitions
    models = {
        "ExtraTrees":         ExtraTreesClassifier(random_state=42),
        "SVM":                SVC(random_state=42, probability=True),
        "LogisticRegression": LogisticRegression(max_iter=1000, random_state=42),
        "QDA":                QuadraticDiscriminantAnalysis(),
        "MLP":                MLPClassifier(random_state=42, max_iter=1000),
        "XGBoost":            XGBClassifier(random_state=42, eval_metric="logloss"),
        "TabNet":             TabNetClassifier(verbose=0, seed=42),
    }

    model_scores = {}
    print("\nTraining models on resampled train set ...")

    for name, model in models.items():
        Xtr = X_train_res.values if name == "TabNet" else X_train_res
        ytr = y_train_res.values if name == "TabNet" else y_train_res
        Xva = X_val.values       if name == "TabNet" else X_val
        Xte = X_test.values      if name == "TabNet" else X_test

        if name == "TabNet":
            model.fit(
                Xtr, ytr,
                eval_set=[(Xva, y_val.values)],
                patience=20, max_epochs=200, batch_size=1024,
            )
        else:
            model.fit(Xtr, ytr)

        # Evaluate on RAW imbalanced test set
        y_pred  = model.predict(Xte)
        y_proba = model.predict_proba(Xte)[:, 1] if hasattr(model, "predict_proba") else None

        acc      = round(accuracy_score(y_test, y_pred), 4)
        macro_f1 = round(f1_score(y_test, y_pred, average="macro"), 4)
        prec     = round(precision_score(y_test, y_pred, zero_division=0), 4)
        sens     = round(recall_score(y_test, y_pred, zero_division=0), 4)
        spec     = _specificity(y_test, y_pred)
        pr_auc   = round(average_precision_score(y_test, y_proba), 4) if y_proba is not None else None

        model_scores[name] = {
            "Accuracy":    acc,
            "Macro-F1":    macro_f1,
            "Precision":   prec,
            "Sensitivity": sens,
            "Specificity": spec,
            "PR-AUC":      pr_auc,
        }

        if name == "ExtraTrees":
            print(f"\nFeature Importances ({name}):")
            importances = pd.Series(
                model.feature_importances_, index=X_train.columns
            ).sort_values(ascending=False)
            print(importances)

    print("\nModel training completed.")
    evaluate_models(models, PROPERTIES, X_test, y_test)

    for name, scores in model_scores.items():
        for metric, value in scores.items():
            metrics_dict[f"{name}_{metric}"] = value

    return (models, metrics_dict) if return_metrics else (models, metrics_dict)


def evaluate_models(models, PROPERTIES: dict, X_test, y_test):
    roc_data = {}
    for name, model in models.items():
        X_input = X_test.values if name == "TabNet" else X_test
        y_pred  = model.predict(X_input)
        y_proba = model.predict_proba(X_input)[:, 1] if hasattr(model, "predict_proba") else None

        print(f"\n{'─'*50}")
        print(f"{name}  Acc={accuracy_score(y_test,y_pred):.4f}  Macro-F1={f1_score(y_test,y_pred,average='macro'):.4f}", end="")
        if y_proba is not None:
            print(f"  PR-AUC={average_precision_score(y_test,y_proba):.4f}", end="")
        print()
        print(f"Confusion Matrix:\n{confusion_matrix(y_test, y_pred)}")
        print(classification_report(y_test, y_pred))

        if y_proba is not None:
            fpr, tpr, _ = roc_curve(y_test, y_proba)
            roc_data[name] = {"fpr": fpr, "tpr": tpr, "auc": auc(fpr, tpr)}

        if PROPERTIES.get("save_graphs", False):
            ds  = PROPERTIES.get("current_dataset_name", "unknown")
            gd  = os.path.join(PROPERTIES.get("graphs_dir", "model_graphs"), ds)
            os.makedirs(gd, exist_ok=True)
            save_confusion_matrix(y_test, y_pred, name, os.path.join(gd, f"{name.lower()}_cm.png"))

    if PROPERTIES.get("save_graphs", False) and roc_data:
        ds = PROPERTIES.get("current_dataset_name", "unknown")
        gd = os.path.join(PROPERTIES.get("graphs_dir", "model_graphs"), ds)
        os.makedirs(gd, exist_ok=True)
        save_combined_roc_curve(roc_data, os.path.join(gd, "combined_roc_curve.png"))


def save_confusion_matrix(y_true, y_pred, model_name, filename):
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
    plt.title(f"{model_name} Confusion Matrix")
    plt.xlabel("Predicted"); plt.ylabel("Actual")
    plt.tight_layout(); plt.savefig(filename); plt.close()


def save_combined_roc_curve(roc_data, filename):
    colors = ["darkorange","red","green","blue","purple","brown","pink"]
    plt.figure(figsize=(10, 8))
    for i, (name, data) in enumerate(roc_data.items()):
        plt.plot(data["fpr"], data["tpr"], color=colors[i % len(colors)], lw=2,
                 label=f"{name} (AUC={data['auc']:.3f})")
    plt.plot([0,1],[0,1],"navy",linestyle="--",lw=2,label="Random (AUC=0.5)")
    plt.title("Combined ROC Curves", fontsize=16)
    plt.xlabel("False Positive Rate", fontsize=14)
    plt.ylabel("True Positive Rate",  fontsize=14)
    plt.legend(loc="lower right", fontsize=12)
    plt.grid(True, alpha=0.3); plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches="tight"); plt.close()
    print(f"Combined ROC saved -> '{filename}'")
