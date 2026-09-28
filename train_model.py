import os
import pandas as pd
import joblib
from sklearn.tree import DecisionTreeClassifier


# ============================================================
# FILE PATHS
# ============================================================

DATASET = "symptoms_disease_dataset_40.csv"

MODEL_DIR = "model"

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "disease-model.pkl"
)

os.makedirs(MODEL_DIR, exist_ok=True)


# ============================================================
# LOAD DATASET
# ============================================================

df = pd.read_csv(DATASET)

df.columns = df.columns.str.strip()


# ============================================================
# FIND DISEASE COLUMN
# ============================================================

disease_column = None

for column in df.columns:

    if column.strip().lower() == "disease":

        disease_column = column
        break


if disease_column is None:

    raise ValueError(
        "Disease column not found in dataset."
    )


# ============================================================
# SPLIT MULTIPLE SYMPTOMS FROM ONE CELL
# ============================================================

def split_symptoms(value):

    if pd.isna(value):

        return []

    text = str(value).strip()

    if not text:

        return []

    # Replace semicolon with comma
    text = text.replace(";", ",")

    # Split comma-separated symptoms
    parts = text.split(",")

    symptoms = []

    for part in parts:

        symptom = part.strip()

        if symptom:

            symptoms.append(symptom)

    return symptoms


# ============================================================
# GET ALL INDIVIDUAL SYMPTOMS
# ============================================================

all_symptoms = set()


for _, row in df.iterrows():

    for column in df.columns:

        if column == disease_column:

            continue

        value = row[column]

        current_symptoms = split_symptoms(value)

        for symptom in current_symptoms:

            all_symptoms.add(symptom)


all_symptoms = sorted(all_symptoms)


# ============================================================
# DISPLAY INFORMATION
# ============================================================

print()
print("============================================")
print("DATASET INFORMATION")
print("============================================")
print("Number of diseases :", df[disease_column].nunique())
print("Number of symptoms :", len(all_symptoms))
print("Number of records  :", len(df))
print("============================================")
print()


# ============================================================
# CREATE TRAINING DATA
# ============================================================

X = []

y = []


for _, row in df.iterrows():

    patient_symptoms = set()


    for column in df.columns:

        if column == disease_column:

            continue


        value = row[column]


        current_symptoms = split_symptoms(value)


        for symptom in current_symptoms:

            patient_symptoms.add(symptom)


    # --------------------------------------------
    # CREATE BINARY FEATURES
    # --------------------------------------------

    features = []


    for symptom in all_symptoms:

        if symptom in patient_symptoms:

            features.append(1)

        else:

            features.append(0)


    X.append(features)


    # --------------------------------------------
    # DISEASE LABEL
    # --------------------------------------------

    disease = str(
        row[disease_column]
    ).strip()


    y.append(disease)


# ============================================================
# CREATE DATAFRAME
# ============================================================

X = pd.DataFrame(
    X,
    columns=all_symptoms
)

y = pd.Series(y)


# ============================================================
# TRAIN MODEL
# ============================================================

model = DecisionTreeClassifier(
    random_state=42
)

model.fit(
    X,
    y
)


# ============================================================
# SAVE MODEL
# ============================================================

model_data = {

    "model": model,

    "symptoms": all_symptoms

}


joblib.dump(
    model_data,
    MODEL_PATH
)


# ============================================================
# SUCCESS
# ============================================================

print()
print("============================================")
print("MODEL TRAINED SUCCESSFULLY")
print("============================================")
print("Diseases :", y.nunique())
print("Symptoms :", len(all_symptoms))
print("Records  :", len(df))
print()
print("Model saved to:")
print(MODEL_PATH)
print("============================================")