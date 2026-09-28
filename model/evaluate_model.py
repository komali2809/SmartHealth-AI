import pandas as pd
import numpy as np
import joblib

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)


BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = (
    BASE_DIR
    / "data"
    / "symptoms_disease_dataset_40.csv"
)

MODEL_PATH = (
    BASE_DIR
    / "model"
    / "disease_model.pkl"
)


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

df = pd.read_csv(DATA_PATH)

df["Symptoms"] = (
    df["Symptoms"]
    .astype(str)
    .str.lower()
    .str.replace("_", " ", regex=False)
    .str.replace("-", " ", regex=False)
)

df["Disease"] = df["Disease"].astype(str).str.strip()


# ---------------------------------------------------------
# CREATE SYMPTOM VOCABULARY
# ---------------------------------------------------------

symptom_vocabulary = sorted(
    set(
        symptom.strip()
        for symptoms in df["Symptoms"]
        for symptom in symptoms.split(",")
        if symptom.strip()
    )
)


# ---------------------------------------------------------
# CREATE FEATURE MATRIX
# ---------------------------------------------------------

X = []

for symptoms in df["Symptoms"]:

    selected = {
        symptom.strip()
        for symptom in symptoms.split(",")
    }

    row = [
        1 if symptom in selected else 0
        for symptom in symptom_vocabulary
    ]

    X.append(row)


X = np.array(X)

y = df["Disease"].values


# ---------------------------------------------------------
# TRAIN / TEST SPLIT
# ---------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# ---------------------------------------------------------
# TRAIN MODEL
# ---------------------------------------------------------

model = DecisionTreeClassifier(
    random_state=42
)

model.fit(
    X_train,
    y_train
)


# ---------------------------------------------------------
# PREDICTION
# ---------------------------------------------------------

y_pred = model.predict(X_test)


# ---------------------------------------------------------
# METRICS
# ---------------------------------------------------------

accuracy = accuracy_score(
    y_test,
    y_pred
)

precision = precision_score(
    y_test,
    y_pred,
    average="weighted",
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    average="weighted",
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    average="weighted",
    zero_division=0
)


# ---------------------------------------------------------
# RESULTS
# ---------------------------------------------------------

print("\n========================================")
print("SmartHealth AI - Model Evaluation")
print("========================================")

print(f"Training samples : {len(X_train)}")
print(f"Testing samples  : {len(X_test)}")
print(f"Symptoms/features: {len(symptom_vocabulary)}")
print(f"Disease classes  : {len(set(y))}")

print("\nEvaluation Metrics")
print("----------------------------------------")

print(f"Accuracy  : {accuracy:.4f}")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")


print("\nClassification Report")
print("----------------------------------------")

print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)