import streamlit as st
from pathlib import Path
import joblib


st.set_page_config(
    page_title="SmartHealth AI - Dashboard",
    page_icon="🏠",
    layout="wide"
)


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "model" / "disease_model.pkl"


st.title("🏠 SmartHealth AI")
st.subheader("AI-Powered Health & Wellness Intelligence Platform")

st.write(
    """
    SmartHealth AI combines symptom analysis, nutrition intelligence,
    regional food recommendations, allergy filtering, meal planning,
    traditional wellness information, and health-history tracking
    in one application.
    """
)


st.divider()


col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "🧠 Symptom Analysis",
        "Available"
    )

with col2:
    st.metric(
        "🥗 Nutrition",
        "Available"
    )

with col3:
    st.metric(
        "🍱 Meal Planning",
        "Available"
    )

with col4:
    st.metric(
        "📚 History",
        "Available"
    )


st.divider()


st.header("🤖 Machine Learning System")


if MODEL_PATH.exists():

    try:

        model_data = joblib.load(
            MODEL_PATH
        )

        model = model_data.get(
            "model"
        )

        symptoms = model_data.get(
            "symptoms",
            []
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Model",
                type(model).__name__
            )

        with col2:
            st.metric(
                "Symptoms",
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

    except Exception as error:

        st.error(
            f"Could not load model information: {error}"
        )

else:

    st.warning(
        "Machine-learning model file was not found."
    )


st.divider()


st.header("🚀 Application Modules")


modules = [
    (
        "🧠 Symptom Analysis",
        "Analyze selected symptoms using the trained ML model."
    ),
    (
        "🥗 Nutrition Intelligence",
        "Calculate BMI, BMR and estimated daily energy requirements."
    ),
    (
        "🌎 Regional Food Recommendations",
        "Filter foods according to region, diet and allergies."
    ),
    (
        "🍱 Personalized Meal Planning",
        "Generate meal plans using nutrition and condition-related rules."
    ),
    (
        "🌿 Traditional Wellness",
        "Retrieve informational Ayurveda and homeopathy knowledge."
    ),
    (
        "📈 Progress",
        "Review application history and model-output patterns."
    )
]


for name, description in modules:

    st.markdown(
        f"### {name}"
    )

    st.write(
        description
    )


st.divider()


st.warning(
    "SmartHealth AI is an educational and wellness-oriented "
    "application. Model outputs are possibilities generated "
    "from the training data and are not medical diagnoses."
)