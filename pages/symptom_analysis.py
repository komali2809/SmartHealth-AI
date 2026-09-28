import streamlit as st
import joblib
from pathlib import Path

from modules.symptom_analyzer import SymptomAnalyzer
from modules.explainability import get_feature_importance
from modules.safety import HealthSafetyEngine
from database.database import save_symptom_analysis


st.set_page_config(
    page_title="SmartHealth AI - Symptom Analysis",
    page_icon="🧠",
    layout="wide"
)


BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    BASE_DIR
    / "model"
    / "disease-model.pkl"
)


st.title("🧠 Symptom Analysis")

st.caption(
    "Analyze selected symptoms using the SmartHealth AI "
    "machine-learning model."
)


st.warning(
    "The results shown here are model-generated possibilities "
    "based on the application's training data. They are not "
    "medical diagnoses."
)


# ---------------------------------------------------------
# LOAD MODEL
# ---------------------------------------------------------

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
        f"Could not load the model: {error}"
    )

    st.stop()


model = model_data["model"]
symptoms = model_data["symptoms"]


# ---------------------------------------------------------
# USER INFORMATION
# ---------------------------------------------------------

st.header("👤 Basic Information")

col1, col2, col3, col4 = st.columns(4)

with col1:
    user_name = st.text_input(
        "Name",
        value="Guest"
    )

with col2:
    age = st.number_input(
        "Age",
        min_value=1,
        max_value=120,
        value=21
    )

with col3:
    gender = st.selectbox(
        "Gender",
        ["Female", "Male", "Other"]
    )

with col4:
    country = st.text_input(
        "Country",
        value="India"
    )

state = st.text_input(
    "State",
    value="Andhra Pradesh"
)


# ---------------------------------------------------------
# SYMPTOM SELECTION
# ---------------------------------------------------------

st.header("🔎 Select Symptoms")

st.write(
    "Select the symptoms you are currently experiencing."
)


selected_symptoms = st.multiselect(
    "Symptoms",
    options=symptoms,
    format_func=lambda x: str(x).replace(
        "_",
        " "
    ).title()
)


# ---------------------------------------------------------
# ANALYZE
# ---------------------------------------------------------

if st.button(
    "🧠 Analyze Symptoms",
    use_container_width=True
):

    if not selected_symptoms:

        st.error(
            "Please select at least one symptom."
        )

        st.stop()

    try:

        analyzer = SymptomAnalyzer()

        result = analyzer.analyze(
            selected_symptoms,
            top_n=5
        )

        st.session_state.last_analysis = result


        # -------------------------------------------------
        # SAVE TO DATABASE
        # -------------------------------------------------

        save_symptom_analysis(
            user_name=user_name,
            age=age,
            gender=gender,
            country=country,
            state=state,
            symptoms=selected_symptoms,
            primary_prediction=result[
                "primary_prediction"
            ]
        )

        st.success(
            "Symptom analysis completed and saved to history."
        )


    except Exception as error:

        st.error(
            f"Analysis failed: {error}"
        )

        st.stop()


# ---------------------------------------------------------
# DISPLAY RESULTS
# ---------------------------------------------------------

if "last_analysis" in st.session_state:

    result = st.session_state.last_analysis

    st.divider()

    st.header("📊 Analysis Results")


    primary_prediction = result[
        "primary_prediction"
    ]


    # -----------------------------------------------------
    # PRIMARY OUTPUT
    # -----------------------------------------------------

    st.subheader(
        "Primary Model Output"
    )

    st.info(
        primary_prediction
    )


    # -----------------------------------------------------
    # TOP RESULTS
    # -----------------------------------------------------

    st.subheader(
        "🔬 Top Possible Condition Patterns"
    )

    results = result.get(
        "results",
        []
    )


    for index, item in enumerate(
        results,
        start=1
    ):

        condition = item[
            "condition"
        ]

        probability = item[
            "probability"
        ]


        if probability is not None:

            probability_percent = (
                probability * 100
            )

            st.write(
                f"**{index}. {condition}**"
            )

            st.progress(
                min(
                    max(
                        probability,
                        0.0
                    ),
                    1.0
                )
            )

            st.caption(
                f"Model probability: "
                f"{probability_percent:.2f}%"
            )

        else:

            st.write(
                f"**{index}. {condition}**"
            )


    # -----------------------------------------------------
    # SELECTED SYMPTOMS
    # -----------------------------------------------------

    st.subheader(
        "📝 Selected Symptoms"
    )

    for symptom in result[
        "selected_symptoms"
    ]:

        st.write(
            f"• {str(symptom).replace('_', ' ').title()}"
        )


    # -----------------------------------------------------
    # EXPLAINABILITY
    # -----------------------------------------------------

    st.divider()

    st.subheader(
        "🔍 Model Explainability"
    )


    try:

        importance = get_feature_importance(
            model_data,
            result["selected_symptoms"],
            top_n=10
        )


        if importance:

            for item in importance:

                st.write(
                    f"**{item['symptom']}**"
                )

                st.progress(
                    min(
                        max(
                            item["importance"],
                            0.0
                        ),
                        1.0
                    )
                )

        else:

            st.info(
                "No feature-importance information "
                "was available for the selected symptoms."
            )


    except Exception as error:

        st.info(
            f"Explainability information unavailable: {error}"
        )


    # -----------------------------------------------------
    # SAFETY
    # -----------------------------------------------------

    st.divider()

    st.warning(
        HealthSafetyEngine.get_disclaimer()
    )

    st.info(
        HealthSafetyEngine.emergency_warning()
    )