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
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import label_binarize


def save_confusion_matrix(y_true, y_pred, model_name, filename):
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=[1, 2], yticklabels=[1, 2])
    plt.title(f'{model_name} Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.savefig(filename)
    plt.close()


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


def original_version_train(X, y):
    print("\n[Original Version: No SMOTE, No Class Weight]\n")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    rf = RandomForestClassifier(random_state=42)
    svm_clf = SVC(random_state=42, probability=True)
    et = ExtraTreesClassifier(random_state=42)

    rf.fit(X_train, y_train)
    svm_clf.fit(X_train, y_train)
    et.fit(X_train, y_train)

    evaluate_models(rf, svm_clf, et, X_test, y_test)


def smote_train(X, y):
    print("\n[SMOTE Version: With SMOTE, No Class Weight]\n")
    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X, y)

    X_train, X_test, y_train, y_test = train_test_split(
        X_resampled, y_resampled, test_size=0.2, random_state=42, stratify=y_resampled
    )

    rf = RandomForestClassifier(random_state=42)
    svm_clf = SVC(random_state=42, probability=True)
    et = ExtraTreesClassifier(random_state=42)

    rf.fit(X_train, y_train)
    svm_clf.fit(X_train, y_train)
    et.fit(X_train, y_train)

    evaluate_models(rf, svm_clf, et, X_test, y_test)


def classweight_train(X, y):
    print("\n[Class Weight Version: No SMOTE, With Class Weight]\n")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    rf = RandomForestClassifier(class_weight='balanced', random_state=42)
    svm_clf = SVC(class_weight='balanced', random_state=42, probability=True)
    et = ExtraTreesClassifier(class_weight='balanced', random_state=42)

    rf.fit(X_train, y_train)
    svm_clf.fit(X_train, y_train)
    et.fit(X_train, y_train)

    evaluate_models(rf, svm_clf, et, X_test, y_test)


def smote_and_classweight_train(X, y):
    print("\n[SMOTE + Class Weight Version: With SMOTE and Class Weight]\n")
    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X, y)

    X_train, X_test, y_train, y_test = train_test_split(
        X_resampled, y_resampled, test_size=0.2, random_state=42, stratify=y_resampled
    )

    rf = RandomForestClassifier(class_weight='balanced', random_state=42)
    svm_clf = SVC(class_weight='balanced', random_state=42, probability=True)
    et = ExtraTreesClassifier(class_weight='balanced', random_state=42)

    rf.fit(X_train, y_train)
    svm_clf.fit(X_train, y_train)
    et.fit(X_train, y_train)

    evaluate_models(rf, svm_clf, et, X_test, y_test)


def evaluate_models(rf, svm_clf, et, X_test, y_test):
    y_pred_rf = rf.predict(X_test)
    y_pred_svm = svm_clf.predict(X_test)
    y_pred_et = et.predict(X_test)

    print("RF Accuracy:", accuracy_score(y_test, y_pred_rf))
    print("RF Confusion Matrix:\n", confusion_matrix(y_test, y_pred_rf))
    print("RF Classification Report:\n", classification_report(y_test, y_pred_rf))

    print("\nSVM Accuracy:", accuracy_score(y_test, y_pred_svm))
    print("SVM Confusion Matrix:\n", confusion_matrix(y_test, y_pred_svm))
    print("SVM Classification Report:\n", classification_report(y_test, y_pred_svm))

    print("\nExtra Trees Accuracy:", accuracy_score(y_test, y_pred_et))
    print("Extra Trees Confusion Matrix:\n", confusion_matrix(y_test, y_pred_et))
    print("Extra Trees Classification Report:\n", classification_report(y_test, y_pred_et))

    save_confusion_matrix(y_test, y_pred_rf, "Random Forest", "rf_confusion_matrix.png")
    save_confusion_matrix(y_test, y_pred_svm, "SVM", "svm_confusion_matrix.png")
    save_confusion_matrix(y_test, y_pred_et, "Extra Trees", "et_confusion_matrix.png")

    save_roc_curve(y_test, rf.predict_proba(X_test)[:, 1], "Random Forest", "rf_roc_curve.png")
    save_roc_curve(y_test, svm_clf.predict_proba(X_test)[:, 1], "SVM", "svm_roc_curve.png")
    save_roc_curve(y_test, et.predict_proba(X_test)[:, 1], "Extra Trees", "et_roc_curve.png")
