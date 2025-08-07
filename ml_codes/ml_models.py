from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix, roc_curve, auc
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

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.preprocessing import label_binarize

def smote_train(X, y, return_metrics=False):
    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X, y)

    X_train, X_test, y_train, y_test = train_test_split(
        X_resampled, y_resampled, test_size=0.2, random_state=42, stratify=y_resampled
    )

    models = {
        "ExtraTrees": ExtraTreesClassifier(random_state=42),
        "SVM": SVC(random_state=42, probability=True),
        "LogisticRegression": LogisticRegression(max_iter=1000, random_state=42),
        "QDA": QuadraticDiscriminantAnalysis(),
        "MLP": MLPClassifier(random_state=42, max_iter=1000),
        "XGBoost": XGBClassifier(random_state=42, use_label_encoder=False, eval_metric='logloss'),
        "TabNet": TabNetClassifier(verbose=0, seed=42),
    }

    model_scores = {}

    for name, model in models.items():
        X_input = X_train.values if name == "TabNet" else X_train
        y_input = y_train.values if name == "TabNet" else y_train

        if name == "TabNet":
            model.fit(
                X_input, y_input,
                eval_set=[(X_test.values, y_test.values)],
                patience=20,
                max_epochs=200,
                batch_size=1024,
            )
            X_eval = X_test.values
        else:
            model.fit(X_input, y_input)
            X_eval = X_test

        y_pred = model.predict(X_eval)

        # For ROC curve, skip in CSV
        y_proba = model.predict_proba(X_eval)[:, 1] if hasattr(model, "predict_proba") else None

        model_scores[name] = {
            "Accuracy": round(accuracy_score(y_test, y_pred), 4),
            "Precision": round(precision_score(y_test, y_pred), 4),
            "Recall": round(recall_score(y_test, y_pred), 4),
            "F1": round(f1_score(y_test, y_pred), 4),
        }

    return model_scores if return_metrics else None
