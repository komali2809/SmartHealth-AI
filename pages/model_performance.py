import streamlit as st
import joblib
import pandas as pd
from pathlib import Path


st.set_page_config(
    page_title="SmartHealth AI - Model Performance",
    page_icon="📊",
    layout="wide"
)


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "model" / "disease-model.pkl"


st.title("📊 Model Performance")
st.caption(
    "View information about the machine-learning model used by SmartHealth AI."
)


if not MODEL_PATH.exists():

    st.error(
        f"Model file not found: {MODEL_PATH}"
    )

    st.stop()


try:

    model_data = joblib.load(
        MODEL_PATH
    )

except Exception as error:

    st.error(
        f"Unable to load model: {error}"
    )

    st.stop()


model = model_data.get(
    "model"
)

symptoms = model_data.get(
    "symptoms",
    []
)


st.header("🤖 Model Information")


col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Model Type",
        type(model).__name__
    )

with col2:
    st.metric(
        "Input Features",
        len(symptoms)
    )

with col3:

    if hasattr(model, "classes_"):
        st.metric(
            "Condition Classes",
            len(model.classes_)
        )
    else:
        st.metric(
            "Condition Classes",
            "N/A"
        )


st.divider()


st.header("🧠 Supported Conditions")


if hasattr(model, "classes_"):

    classes = [
        str(item)
        for item in model.classes_
    ]

    condition_df = pd.DataFrame(
        {
            "Condition": classes
        }
    )

    st.dataframe(
        condition_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "The loaded model does not expose class information."
    )


st.divider()


st.header("🔍 Model Input Features")

st.write(
    "The model receives normalized symptom indicators "
    "as input features."
)


feature_df = pd.DataFrame(
    {
        "Feature": [
            str(symptom)
            for symptom in symptoms
        ]
    }
)

st.dataframe(
    feature_df,
    use_container_width=True,
    hide_index=True
)


st.divider()


st.header("📈 Feature Importance")


if hasattr(
    model,
    "feature_importances_"
):

    importance_df = pd.DataFrame(
        {
            "Symptom": symptoms,
            "Importance": model.feature_importances_
        }
    )

    importance_df = (
        importance_df
        .sort_values(
            "Importance",
            ascending=False
        )
        .head(15)
        .reset_index(drop=True)
    )

    st.bar_chart(
        importance_df.set_index(
            "Symptom"
        )["Importance"]
    )

else:

    st.info(
        "Feature-importance information is not available "
        "for this model."
    )


st.divider()


st.warning(
    "Important: Model performance metrics such as accuracy, "
    "precision, recall, and F1-score should only be reported "
    "after evaluating the model on a separate test dataset. "
    "This page does not invent performance metrics."
)


st.info(
    "SmartHealth AI provides model-generated possibilities "
    "for educational and wellness-oriented use. It is not "
    "a medical diagnosis."
)