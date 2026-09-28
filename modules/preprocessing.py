import re
import numpy as np


class TextPreprocessor:

    @staticmethod
    def normalize_text(text):
        if text is None:
            return ""

        text = str(text).strip().lower()
        text = text.replace("_", " ")
        text = text.replace("-", " ")
        text = re.sub(r"\s+", " ", text)

        return text

    @classmethod
    def normalize_symptom(cls, symptom):
        return cls.normalize_text(symptom)

    @classmethod
    def normalize_symptoms(cls, symptoms):

        if symptoms is None:
            return []

        if isinstance(symptoms, str):
            symptoms = symptoms.split(",")

        normalized = []

        for symptom in symptoms:

            value = cls.normalize_symptom(symptom)

            if value:
                normalized.append(value)

        return list(dict.fromkeys(normalized))

    @classmethod
    def create_binary_vector(
        cls,
        selected_symptoms,
        symptom_vocabulary
    ):

        selected = set(
            cls.normalize_symptoms(selected_symptoms)
        )

        vector = []

        for symptom in symptom_vocabulary:

            normalized = cls.normalize_symptom(
                symptom
            )

            vector.append(
                1 if normalized in selected else 0
            )

        return np.array(vector)

    @staticmethod
    def clean_dataframe_columns(df):

        result = df.copy()

        result.columns = [
            str(column).strip()
            for column in result.columns
        ]

        return result
