def normalize_symptom(symptom):
    return (
        str(symptom)
        .strip()
        .lower()
        .replace("_", " ")
        .replace("-", " ")
    )


def get_selected_features(model_data, selected_symptoms):
    symptoms = model_data["symptoms"]

    selected_normalized = {
        normalize_symptom(symptom)
        for symptom in selected_symptoms
    }

    selected_features = []

    for symptom in symptoms:

        normalized = normalize_symptom(
            symptom
        )

        if normalized in selected_normalized:

            selected_features.append(
                symptom
            )

    return selected_features


def get_feature_importance(
    model_data,
    selected_symptoms,
    top_n=10
):

    model = model_data["model"]

    if not hasattr(
        model,
        "feature_importances_"
    ):
        return []

    symptoms = model_data["symptoms"]

    importances = (
        model.feature_importances_
    )

    selected_normalized = {
        normalize_symptom(symptom)
        for symptom in selected_symptoms
    }

    candidates = []

    for symptom, importance in zip(
        symptoms,
        importances
    ):

        normalized = normalize_symptom(
            symptom
        )

        if normalized in selected_normalized:

            candidates.append(
                {
                    "symptom": symptom,
                    "importance": float(
                        importance
                    )
                }
            )

    candidates.sort(
        key=lambda x:
        x["importance"],
        reverse=True
    )

    return candidates[:top_n]


def explain_prediction(
    model_data,
    selected_symptoms,
    prediction
):

    important_symptoms = (
        get_feature_importance(
            model_data,
            selected_symptoms
        )
    )

    return {
        "prediction": str(prediction),
        "selected_symptoms": list(
            selected_symptoms
        ),
        "important_symptoms":
            important_symptoms
    }


# Optional class interface for newer modules
class ExplainabilityEngine:

    def __init__(self, model_data):

        self.model_data = model_data

    def get_feature_importance(
        self,
        selected_symptoms,
        top_n=10
    ):

        return get_feature_importance(
            self.model_data,
            selected_symptoms,
            top_n
        )

    def explain_prediction(
        self,
        selected_symptoms,
        prediction
    ):

        return explain_prediction(
            self.model_data,
            selected_symptoms,
            prediction
        )