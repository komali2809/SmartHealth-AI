import streamlit as st

from modules.symptom_analyzer import SymptomAnalyzer
from modules.explainability import get_feature_importance
from modules.nutrition import calculate_nutrition_profile
from modules.regional_recommendations import RegionalFoodRecommender
from modules.allergy_filter import AllergySafetyEngine
from modules.explainability import get_feature_importance

from database.database import (
    initialize_database,
    save_symptom_analysis
)


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

initialize_database()


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SmartHealth AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "name": "User",
    "age": 20,
    "gender": "Female",
    "weight": 60.0,
    "height": 165.0,
    "activity_level": "moderate",
    "diet_preference": "Vegetarian",
    "allergies": "",
    "country": "India",
    "region": "Andhra Pradesh",
    "last_analysis": None,
    "last_nutrition": None
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# COUNTRY / REGION DATA
# ============================================================

COUNTRY_STATES = {

    "India": [
        "Andhra Pradesh",
        "Arunachal Pradesh",
        "Assam",
        "Bihar",
        "Chhattisgarh",
        "Goa",
        "Gujarat",
        "Haryana",
        "Himachal Pradesh",
        "Jharkhand",
        "Karnataka",
        "Kerala",
        "Madhya Pradesh",
        "Maharashtra",
        "Manipur",
        "Meghalaya",
        "Mizoram",
        "Nagaland",
        "Odisha",
        "Punjab",
        "Rajasthan",
        "Sikkim",
        "Tamil Nadu",
        "Telangana",
        "Tripura",
        "Uttar Pradesh",
        "Uttarakhand",
        "West Bengal",
        "Andaman and Nicobar Islands",
        "Chandigarh",
        "Dadra and Nagar Haveli and Daman and Diu",
        "Delhi",
        "Jammu and Kashmir",
        "Ladakh",
        "Lakshadweep",
        "Puducherry"
    ],

    "United States": [
        "Alabama",
        "Alaska",
        "Arizona",
        "Arkansas",
        "California",
        "Colorado",
        "Connecticut",
        "Florida",
        "Georgia",
        "Illinois",
        "Massachusetts",
        "Michigan",
        "New Jersey",
        "New York",
        "North Carolina",
        "Ohio",
        "Pennsylvania",
        "Texas",
        "Virginia",
        "Washington"
    ],

    "Canada": [
        "Alberta",
        "British Columbia",
        "Manitoba",
        "New Brunswick",
        "Newfoundland and Labrador",
        "Nova Scotia",
        "Ontario",
        "Prince Edward Island",
        "Quebec",
        "Saskatchewan",
        "Northwest Territories",
        "Nunavut",
        "Yukon"
    ],

    "Australia": [
        "New South Wales",
        "Queensland",
        "South Australia",
        "Tasmania",
        "Victoria",
        "Western Australia",
        "Australian Capital Territory",
        "Northern Territory"
    ],

    "United Kingdom": [
        "England",
        "Scotland",
        "Wales",
        "Northern Ireland"
    ]
}


# ============================================================
# LOAD MODELS / ENGINES
# ============================================================

@st.cache_resource
def load_symptom_analyzer():

    return SymptomAnalyzer()


@st.cache_resource
def load_regional_recommender():

    return RegionalFoodRecommender()


@st.cache_resource
def load_allergy_engine():

    return AllergySafetyEngine()


try:

    analyzer = load_symptom_analyzer()

except Exception as error:

    analyzer = None

    st.error(
        "Symptom analysis engine could not be loaded."
    )

    st.exception(error)


try:

    regional_recommender = load_regional_recommender()

except Exception as error:

    regional_recommender = None

    st.error(
        "Regional food recommendation engine could not be loaded."
    )

    st.exception(error)


allergy_engine = load_allergy_engine()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🩺 SmartHealth AI")

st.sidebar.caption(
    "Explainable Health & Wellness Intelligence Platform"
)

st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "🧠 Symptom Analysis",
        "🥗 Nutrition Planner",
        "🍱 Regional Foods",
        "👤 Profile"
    ]
)

st.sidebar.divider()

st.sidebar.caption(
    "⚠️ This application provides model-generated and "
    "informational outputs. It does not provide medical diagnosis "
    "or replace professional medical advice."
)


# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    st.title("🩺 SmartHealth AI")

    st.subheader(
        "Explainable, Personalized Health & Wellness Intelligence"
    )

    st.write(
        "SmartHealth AI combines machine learning, nutrition "
        "analysis, regional food recommendations, allergy filtering "
        "and personalized planning into one application."
    )

    st.divider()

    # --------------------------------------------------------
    # TOP METRICS
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Age",
            st.session_state.age
        )

    with col2:

        st.metric(
            "BMI",
            (
                f"{st.session_state.last_nutrition['bmi']:.2f}"
                if st.session_state.last_nutrition
                else "—"
            )
        )

    with col3:

        st.metric(
            "Country",
            st.session_state.country
        )

    with col4:

        st.metric(
            "Diet",
            st.session_state.diet_preference
        )

    st.divider()

    # --------------------------------------------------------
    # FEATURES
    # --------------------------------------------------------

    st.header("🚀 Platform Capabilities")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            """
            ### 🧠 Explainable Symptom Analysis

            - ML-based symptom pattern analysis
            - Top possible condition patterns
            - Probability information
            - Feature-importance explanation
            - Stored analysis history
            """
        )

    with col2:

        st.markdown(
            """
            ### 🥗 Personalized Nutrition

            - BMI calculation
            - BMR calculation
            - TDEE estimation
            - Regional food recommendations
            - Diet filtering
            - Allergy-aware recommendations
            """
        )

    col3, col4 = st.columns(2)

    with col3:

        st.markdown(
            """
            ### 🌎 Regional Intelligence

            - Country selection
            - State / region selection
            - Regional food database
            - Meal-type filtering
            - Nutrition constraints
            """
        )

    with col4:

        st.markdown(
            """
            ### 🛡️ Safety Layer

            - Allergy filtering
            - Informational health outputs
            - Non-diagnostic ML interpretation
            - Local data storage
            - Sensitive-data awareness
            """
        )

    st.divider()

    st.info(
        "Use the sidebar to start with your profile, "
        "analyze symptoms, or create a personalized nutrition plan."
    )


# ============================================================
# SYMPTOM ANALYSIS
# ============================================================

elif page == "🧠 Symptom Analysis":

    st.title("🧠 Symptom Analysis")

    st.caption(
        "Analyze symptom patterns using the trained machine-learning model."
    )

    if analyzer is None:

        st.error(
            "The symptom analysis model is unavailable."
        )

        st.stop()

    # --------------------------------------------------------
    # USER INFORMATION
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        age = st.number_input(
            "Age",
            min_value=1,
            max_value=120,
            value=int(st.session_state.age),
            key="symptom_age"
        )

    with col2:

        gender = st.selectbox(
            "Gender",
            [
                "Female",
                "Male",
                "Other"
            ],
            index=[
                "Female",
                "Male",
                "Other"
            ].index(
                st.session_state.gender
                if st.session_state.gender
                in ["Female", "Male", "Other"]
                else "Female"
            ),
            key="symptom_gender"
        )

    with col3:

        country = st.selectbox(
            "Country",
            list(COUNTRY_STATES.keys()),
            index=(
                list(COUNTRY_STATES.keys()).index(
                    st.session_state.country
                )
                if st.session_state.country
                in COUNTRY_STATES
                else 0
            ),
            key="symptom_country"
        )

    states = COUNTRY_STATES[country]

    current_state = (
        st.session_state.region
        if st.session_state.region in states
        else states[0]
    )

    state = st.selectbox(
        "State / Region",
        states,
        index=states.index(current_state),
        key="symptom_state"
    )

    # --------------------------------------------------------
    # SYMPTOMS
    # --------------------------------------------------------

    st.subheader("Select your symptoms")

    symptom_options = sorted(
        list(
            dict.fromkeys(
                [
                    str(symptom).strip()
                    for symptom in analyzer.symptoms
                ]
            )
        )
    )

    selected_symptoms = st.multiselect(
        "Symptoms",
        symptom_options,
        help="Select the symptoms you are experiencing."
    )

    st.warning(
        "The results below are model-generated possibilities based "
        "on the training dataset. They are not medical diagnoses."
    )

    analyze_button = st.button(
        "🔍 Analyze Symptoms",
        type="primary",
        use_container_width=True
    )

    if analyze_button:

        if not selected_symptoms:

            st.error(
                "Please select at least one symptom."
            )

        else:

            try:

                result = analyzer.analyze(
                    selected_symptoms,
                    top_n=5
                )

                # Save user details into session state

                st.session_state.age = age
                st.session_state.gender = gender
                st.session_state.country = country
                st.session_state.region = state

                st.session_state.last_analysis = result

                # ------------------------------------------------
                # DATABASE SAVE
                # ------------------------------------------------

                save_symptom_analysis(
                    user_name=st.session_state.get(
                        "name",
                        "User"
                    ),
                    age=age,
                    gender=gender,
                    country=country,
                    state=state,
                    symptoms=result["selected_symptoms"],
                    primary_prediction=result[
                        "primary_prediction"
                    ]
                )

                # ------------------------------------------------
                # PRIMARY RESULT
                # ------------------------------------------------

                st.success(
                    "Symptom analysis completed."
                )

                st.subheader(
                    "Primary Model Prediction"
                )

                st.info(
                    f"**{result['primary_prediction']}**"
                )

                # ------------------------------------------------
                # TOP RESULTS
                # ------------------------------------------------

                st.subheader(
                    "Top Possible Condition Patterns"
                )

                result_data = []

                for item in result["results"]:

                    result_data.append(
                        {
                            "Condition":
                                item["condition"],

                            "Model Probability":
                                (
                                    f"{item['probability'] * 100:.2f}%"
                                    if item["probability"] is not None
                                    else "N/A"
                                )
                        }
                    )

                st.dataframe(
                    result_data,
                    use_container_width=True,
                    hide_index=True
                )

                # ------------------------------------------------
                # EXPLAINABILITY
                # ------------------------------------------------

                st.subheader(
                    "🔎 Why did the model consider these symptoms?"
                )

                try:

                    model_data = analyzer.model_data

                    important_features = (
                        get_feature_importance(
                            model_data,
                            selected_symptoms,
                            top_n=10
                        )
                    )

                    if important_features:

                        explanation_data = []

                        for feature in important_features:

                            explanation_data.append(
                                {
                                    "Symptom":
                                        feature["symptom"],

                                    "Model Feature Importance":
                                        round(
                                            feature["importance"],
                                            4
                                        )
                                }
                            )

                        st.dataframe(
                            explanation_data,
                            use_container_width=True,
                            hide_index=True
                        )

                    else:

                        st.info(
                            "Feature-importance information "
                            "is not available for this model."
                        )

                except Exception as explanation_error:

                    st.info(
                        "Explainability information could not "
                        "be generated."
                    )

                    st.caption(
                        str(explanation_error)
                    )

                # ------------------------------------------------
                # SELECTED SYMPTOMS
                # ------------------------------------------------

                st.subheader(
                    "Selected Symptoms"
                )

                st.write(
                    ", ".join(selected_symptoms)
                )

            except Exception as error:

                st.error(
                    "Unable to complete symptom analysis."
                )

                st.exception(error)


# ============================================================
# NUTRITION PLANNER
# ============================================================

elif page == "🥗 Nutrition Planner":

    st.title("🥗 Nutrition Planner")

    st.caption(
        "Estimate your energy requirements and nutrition profile."
    )

    # --------------------------------------------------------
    # PERSONAL DATA
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        age = st.number_input(
            "Age",
            min_value=1,
            max_value=120,
            value=int(st.session_state.age),
            key="nutrition_age"
        )

    with col2:

        gender = st.selectbox(
            "Gender",
            [
                "Female",
                "Male",
                "Other"
            ],
            key="nutrition_gender"
        )

    with col3:

        activity_level = st.selectbox(
            "Activity Level",
            [
                "sedentary",
                "light",
                "moderate",
                "very_active",
                "extra_active"
            ],
            index=2,
            key="nutrition_activity"
        )

    col4, col5 = st.columns(2)

    with col4:

        weight = st.number_input(
            "Weight (kg)",
            min_value=1.0,
            max_value=300.0,
            value=float(st.session_state.weight),
            step=0.5,
            key="nutrition_weight"
        )

    with col5:

        height = st.number_input(
            "Height (cm)",
            min_value=50.0,
            max_value=250.0,
            value=float(st.session_state.height),
            step=0.5,
            key="nutrition_height"
        )

    calculate_button = st.button(
        "📊 Calculate Nutrition Profile",
        type="primary",
        use_container_width=True
    )

    if calculate_button:

        try:

            profile = calculate_nutrition_profile(
                age=age,
                gender=gender,
                weight_kg=weight,
                height_cm=height,
                activity_level=activity_level
            )

            st.session_state.age = age
            st.session_state.gender = gender
            st.session_state.weight = weight
            st.session_state.height = height
            st.session_state.activity_level = activity_level

            st.session_state.last_nutrition = profile

            st.success(
                "Nutrition profile calculated."
            )

        except Exception as error:

            st.error(
                "Unable to calculate nutrition profile."
            )

            st.exception(error)

    # --------------------------------------------------------
    # DISPLAY NUTRITION PROFILE
    # --------------------------------------------------------

    if st.session_state.last_nutrition:

        profile = st.session_state.last_nutrition

        st.divider()

        st.subheader(
            "Your Nutrition Profile"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "BMI",
                profile["bmi"]
            )

        with col2:

            st.metric(
                "BMI Category",
                profile["bmi_category"]
            )

        with col3:

            st.metric(
                "BMR",
                f"{profile['bmr']:.0f} kcal"
            )

        with col4:

            st.metric(
                "Estimated TDEE",
                f"{profile['tdee']:.0f} kcal"
            )

        st.info(
            "BMI, BMR and TDEE are general estimates and should "
            "not be treated as individualized medical prescriptions."
        )


# ============================================================
# REGIONAL FOODS
# ============================================================

elif page == "🍱 Regional Foods":

    st.title("🍱 Regional Food Intelligence")

    st.caption(
        "Find food options based on location, diet, allergies "
        "and nutrition requirements."
    )

    if regional_recommender is None:

        st.error(
            "Regional food recommendation engine is unavailable."
        )

        st.stop()

    # --------------------------------------------------------
    # LOCATION
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        country = st.selectbox(
            "Country",
            list(COUNTRY_STATES.keys()),
            index=(
                list(COUNTRY_STATES.keys()).index(
                    st.session_state.country
                )
                if st.session_state.country
                in COUNTRY_STATES
                else 0
            ),
            key="regional_country"
        )

    states = COUNTRY_STATES[country]

    with col2:

        current_state = (
            st.session_state.region
            if st.session_state.region in states
            else states[0]
        )

        state = st.selectbox(
            "State / Region",
            states,
            index=states.index(current_state),
            key="regional_state"
        )

    # --------------------------------------------------------
    # DIET
    # --------------------------------------------------------

    diet = st.selectbox(
        "Diet Preference",
        [
            "Vegetarian",
            "Vegan",
            "Eggetarian",
            "Non-Vegetarian"
        ],
        key="regional_diet"
    )

    allergies = st.text_input(
        "Allergies",
        value=st.session_state.allergies,
        placeholder="Example: peanut, milk, egg",
        help="Separate multiple allergies with commas."
    )

    col1, col2 = st.columns(2)

    with col1:

        calorie_limit = st.number_input(
            "Maximum Calories",
            min_value=0.0,
            value=0.0,
            step=50.0
        )

    with col2:

        protein_limit = st.number_input(
            "Minimum Protein (g)",
            min_value=0.0,
            value=0.0,
            step=5.0
        )

    recommend_button = st.button(
        "🔎 Find Suitable Foods",
        type="primary",
        use_container_width=True
    )

    if recommend_button:

        try:

            st.session_state.country = country
            st.session_state.region = state
            st.session_state.diet_preference = diet
            st.session_state.allergies = allergies

            recommendations = (
                regional_recommender.recommend(
                    country=country,
                    state=state,
                    diet_type=diet,
                    allergies=allergies,
                    max_calories=(
                        calorie_limit
                        if calorie_limit > 0
                        else None
                    ),
                    min_protein=(
                        protein_limit
                        if protein_limit > 0
                        else None
                    )
                )
            )

            st.subheader(
                "Recommended Foods"
            )

            if recommendations.empty:

                st.warning(
                    "No matching foods were found for the "
                    "selected filters."
                )

            else:

                display_columns = [
                    "food",
                    "meal_type",
                    "diet_type",
                    "calories",
                    "protein",
                    "carbohydrates",
                    "fat",
                    "common_allergens",
                    "availability"
                ]

                available_columns = [
                    column
                    for column in display_columns
                    if column in recommendations.columns
                ]

                st.dataframe(
                    recommendations[
                        available_columns
                    ],
                    use_container_width=True,
                    hide_index=True
                )

                # ------------------------------------------------
                # SAFETY SUMMARY
                # ------------------------------------------------

                summary = (
                    allergy_engine.safety_summary(
                        regional_recommender.food_df,
                        allergies
                    )
                )

                st.subheader(
                    "🛡️ Allergy Safety Summary"
                )

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "Allergies Checked",
                        len(
                            summary[
                                "allergies_checked"
                            ]
                        )
                    )

                with col2:

                    st.metric(
                        "Safe Foods",
                        summary["safe_foods"]
                    )

                with col3:

                    st.metric(
                        "Filtered Foods",
                        summary["unsafe_foods"]
                    )

                if allergies.strip():

                    st.info(
                        "Foods containing detected allergen "
                        "keywords were filtered from the recommendations."
                    )

        except Exception as error:

            st.error(
                "Unable to generate food recommendations."
            )

            st.exception(error)


# ============================================================
# PROFILE
# ============================================================

elif page == "👤 Profile":

    st.title("👤 Profile")

    st.caption(
        "Manage information used for personalization."
    )

    name = st.text_input(
        "Name",
        value=st.session_state.name
    )

    age = st.number_input(
        "Age",
        min_value=1,
        max_value=120,
        value=int(st.session_state.age)
    )

    gender = st.selectbox(
        "Gender",
        [
            "Female",
            "Male",
            "Other"
        ],
        index=(
            ["Female", "Male", "Other"].index(
                st.session_state.gender
            )
            if st.session_state.gender
            in ["Female", "Male", "Other"]
            else 0
        )
    )

    weight = st.number_input(
        "Weight (kg)",
        min_value=1.0,
        max_value=300.0,
        value=float(st.session_state.weight),
        step=0.5
    )

    height = st.number_input(
        "Height (cm)",
        min_value=50.0,
        max_value=250.0,
        value=float(st.session_state.height),
        step=0.5
    )

    country = st.selectbox(
        "Country",
        list(COUNTRY_STATES.keys()),
        index=(
            list(COUNTRY_STATES.keys()).index(
                st.session_state.country
            )
            if st.session_state.country
            in COUNTRY_STATES
            else 0
        )
    )

    states = COUNTRY_STATES[country]

    current_state = (
        st.session_state.region
        if st.session_state.region in states
        else states[0]
    )

    state = st.selectbox(
        "State / Region",
        states,
        index=states.index(current_state)
    )

    diet = st.selectbox(
        "Diet Preference",
        [
            "Vegetarian",
            "Vegan",
            "Eggetarian",
            "Non-Vegetarian"
        ],
        index=(
            [
                "Vegetarian",
                "Vegan",
                "Eggetarian",
                "Non-Vegetarian"
            ].index(
                st.session_state.diet_preference
            )
            if st.session_state.diet_preference
            in [
                "Vegetarian",
                "Vegan",
                "Eggetarian",
                "Non-Vegetarian"
            ]
            else 0
        )
    )

    allergies = st.text_input(
        "Allergies",
        value=st.session_state.allergies,
        placeholder="Example: peanut, milk"
    )

    if st.button(
        "💾 Save Profile",
        type="primary",
        use_container_width=True
    ):

        st.session_state.name = name
        st.session_state.age = age
        st.session_state.gender = gender
        st.session_state.weight = weight
        st.session_state.height = height
        st.session_state.country = country
        st.session_state.region = state
        st.session_state.diet_preference = diet
        st.session_state.allergies = allergies

        st.success(
            "Profile saved successfully."
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "SmartHealth AI • ML + Nutrition Intelligence + "
    "Regional Recommendations + Allergy Safety"
)