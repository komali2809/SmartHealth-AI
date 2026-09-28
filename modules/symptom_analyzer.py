import joblib
import numpy as np

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    BASE_DIR
    / "model"
    / "disease-model.pkl"
)


class SymptomAnalyzer:

    def __init__(self):

        if not MODEL_PATH.exists():

            raise FileNotFoundError(
                f"Model file not found: {MODEL_PATH}"
            )

        self.model_data = joblib.load(
            MODEL_PATH
        )

        self.model = (
            self.model_data["model"]
        )

        self.symptoms = (
            self.model_data["symptoms"]
        )

    @staticmethod
    def normalize_symptom(symptom):

        return (
            str(symptom)
            .strip()
            .lower()
            .replace("_", " ")
            .replace("-", " ")
        )

    def _create_feature_vector(
        self,
        selected_symptoms
    ):

        normalized_selected = {

            self.normalize_symptom(
                symptom
            )

            for symptom
            in selected_symptoms
        }

        vector = []

        for symptom in self.symptoms:

            normalized_feature = (
                self.normalize_symptom(
                    symptom
                )
            )

            vector.append(
                1
                if normalized_feature
                in normalized_selected
                else 0
            )

        return np.array(
            vector
        ).reshape(1, -1)

    def analyze(
        self,
        selected_symptoms,
        top_n=5
    ):

        if not selected_symptoms:

            raise ValueError(
                "Please select at least one symptom."
            )

        features = (
            self._create_feature_vector(
                selected_symptoms
            )
        )

        prediction = (
            self.model.predict(
                features
            )[0]
        )

        results = []

        if hasattr(
            self.model,
            "predict_proba"
        ):

            probabilities = (
                self.model.predict_proba(
                    features
                )[0]
            )

            classes = self.model.classes_

            ranked_indices = np.argsort(
                probabilities
            )[::-1]

            for index in ranked_indices[:top_n]:

                results.append({

                    "condition":
                        str(classes[index]),

                    "probability":
                        float(
                            probabilities[index]
                        )
                })

        else:

            results.append({

                "condition":
                    str(prediction),

                "probability":
                    None
            })

        return {

            "primary_prediction":
                str(prediction),

            "results":
                results,

            "selected_symptoms":
                list(selected_symptoms)
        }