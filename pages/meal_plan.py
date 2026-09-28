import streamlit as st

from modules.nutrition import calculate_nutrition_profile
from modules.regional_recommendations import RegionalFoodRecommender
from modules.allergy_filter import AllergySafetyEngine
from modules.meal_planner import MealPlanner
from database.database import save_meal_plan


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SmartHealth AI - Meal Planner",
    page_icon="🍱",
    layout="wide"
)


# ============================================================
# SESSION STATE DEFAULTS
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
# LOAD FOOD / SAFETY ENGINES
# ============================================================

@st.cache_resource
def load_regional_recommender():

    return RegionalFoodRecommender()


@st.cache_resource
def load_allergy_engine():

    return AllergySafetyEngine()


try:

    regional_recommender = load_regional_recommender()

except Exception as error:

    st.error(
        "Regional food recommendation engine could not be loaded."
    )

    st.exception(error)

    st.stop()


allergy_engine = load_allergy_engine()


# ============================================================
# TITLE
# ============================================================

st.title("🍱 Personalized Meal Planner")

st.caption(
    "Generate a nutrition-aware meal plan using your "
    "nutrition profile, region, diet, allergies and latest "
    "symptom-analysis context."
)


# ============================================================
# IMPORTANT SAFETY INFORMATION
# ============================================================

st.warning(
    "⚠️ This planner provides general nutrition information. "
    "The symptom-analysis result is treated only as model-generated "
    "context and not as a medical diagnosis or treatment plan."
)


# ============================================================
# STEP 1 — PERSONAL INFORMATION
# ============================================================

st.header("1️⃣ Personal Information")

col1, col2, col3 = st.columns(3)


with col1:

    age = st.number_input(
        "Age",
        min_value=1,
        max_value=120,
        value=int(st.session_state.age),
        key="meal_age"
    )


with col2:

    gender_options = [
        "Female",
        "Male",
        "Other"
    ]

    current_gender = st.session_state.gender

    if current_gender not in gender_options:
        current_gender = "Female"

    gender = st.selectbox(
        "Gender",
        gender_options,
        index=gender_options.index(
            current_gender
        ),
        key="meal_gender"
    )


with col3:

    activity_options = [
        "sedentary",
        "light",
        "moderate",
        "very_active",
        "extra_active"
    ]

    current_activity = (
        st.session_state.activity_level
    )

    if current_activity not in activity_options:
        current_activity = "moderate"

    activity_level = st.selectbox(
        "Activity Level",
        activity_options,
        index=activity_options.index(
            current_activity
        ),
        key="meal_activity"
    )


col4, col5 = st.columns(2)


with col4:

    weight = st.number_input(
        "Weight (kg)",
        min_value=1.0,
        max_value=300.0,
        value=float(st.session_state.weight),
        step=0.5,
        key="meal_weight"
    )


with col5:

    height = st.number_input(
        "Height (cm)",
        min_value=50.0,
        max_value=250.0,
        value=float(st.session_state.height),
        step=0.5,
        key="meal_height"
    )


# ============================================================
# STEP 2 — LOCATION
# ============================================================

st.header("2️⃣ Location & Food Preferences")

col1, col2 = st.columns(2)


with col1:

    countries = list(
        COUNTRY_STATES.keys()
    )

    current_country = st.session_state.country

    if current_country not in countries:
        current_country = "India"

    country = st.selectbox(
        "Country",
        countries,
        index=countries.index(
            current_country
        ),
        key="meal_country"
    )


with col2:

    states = COUNTRY_STATES[country]

    current_state = st.session_state.region

    if current_state not in states:
        current_state = states[0]

    state = st.selectbox(
        "State / Region",
        states,
        index=states.index(
            current_state
        ),
        key="meal_state"
    )


diet_options = [
    "Vegetarian",
    "Vegan",
    "Eggetarian",
    "Non-Vegetarian"
]

current_diet = st.session_state.diet_preference

if current_diet not in diet_options:
    current_diet = "Vegetarian"

diet = st.selectbox(
    "Diet Preference",
    diet_options,
    index=diet_options.index(
        current_diet
    ),
    key="meal_diet"
)


allergies = st.text_input(
    "Food Allergies",
    value=st.session_state.allergies,
    placeholder="Example: peanut, milk, egg",
    help="Enter multiple allergies separated by commas."
)


# ============================================================
# STEP 3 — CALCULATE NUTRITION PROFILE
# ============================================================

st.header("3️⃣ Nutrition Profile")

calculate_button = st.button(
    "📊 Calculate My Nutrition Profile",
    type="secondary",
    use_container_width=True
)


if calculate_button:

    try:

        nutrition_profile = calculate_nutrition_profile(
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

        st.session_state.country = country
        st.session_state.region = state
        st.session_state.diet_preference = diet
        st.session_state.allergies = allergies

        st.session_state.last_nutrition = (
            nutrition_profile
        )

        st.success(
            "Nutrition profile calculated successfully."
        )

    except Exception as error:

        st.error(
            "Could not calculate nutrition profile."
        )

        st.exception(error)


# ============================================================
# DISPLAY NUTRITION PROFILE
# ============================================================

if st.session_state.last_nutrition:

    profile = st.session_state.last_nutrition

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

else:

    # Calculate automatically for meal planning
    try:

        profile = calculate_nutrition_profile(
            age=age,
            gender=gender,
            weight_kg=weight,
            height_cm=height,
            activity_level=activity_level
        )

        st.session_state.last_nutrition = profile

    except Exception:

        profile = None


# ============================================================
# STEP 4 — TARGET CALORIES
# ============================================================

st.header("4️⃣ Daily Calorie Target")

if profile:

    estimated_tdee = float(
        profile["tdee"]
    )

    st.write(
        f"Estimated daily energy requirement: "
        f"**{estimated_tdee:.0f} kcal/day**"
    )

    target_calories = st.number_input(
        "Target Calories",
        min_value=500.0,
        max_value=6000.0,
        value=float(
            round(estimated_tdee)
        ),
        step=50.0,
        key="meal_target_calories"
    )

else:

    target_calories = st.number_input(
        "Target Calories",
        min_value=500.0,
        max_value=6000.0,
        value=2000.0,
        step=50.0,
        key="meal_target_calories_fallback"
    )


# ============================================================
# STEP 5 — SYMPTOM / CONDITION CONTEXT
# ============================================================

st.header("5️⃣ Health Context")

latest_analysis = st.session_state.get(
    "last_analysis"
)

condition = None


if latest_analysis:

    condition = latest_analysis.get(
        "primary_prediction"
    )

    selected_symptoms = latest_analysis.get(
        "selected_symptoms",
        []
    )

    st.success(
        f"Latest model context: **{condition}**"
    )

    if selected_symptoms:

        st.write(
            "**Symptoms considered:** "
            + ", ".join(selected_symptoms)
        )

    st.caption(
        "This context is used to adjust general food "
        "selection and ranking. It is not treated as a diagnosis."
    )

else:

    st.info(
        "No symptom analysis has been completed in this session."
    )

    st.write(
        "You can still generate a general personalized "
        "nutrition plan."
    )


# ============================================================
# STEP 6 — PREVIEW FOOD FILTERING
# ============================================================

st.header("6️⃣ Food Safety & Regional Filtering")

try:

    filtered_foods = regional_recommender.recommend(
        country=country,
        state=state,
        diet_type=diet,
        allergies=allergies,
        max_calories=None,
        min_protein=None
    )

except Exception as error:

    st.error(
        "Unable to filter regional foods."
    )

    st.exception(error)

    filtered_foods = None


if filtered_foods is not None:

    if filtered_foods.empty:

        st.warning(
            "No foods are currently available for "
            "the selected country, region, diet and allergy filters."
        )

    else:

        summary = allergy_engine.safety_summary(
            regional_recommender.food_df,
            allergies
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Available Foods",
                len(filtered_foods)
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


# ============================================================
# STEP 7 — GENERATE MEAL PLAN
# ============================================================

st.header("7️⃣ Generate Personalized Meal Plan")

st.write(
    "The planner combines:"
)

st.markdown(
    """
    - 🧠 Latest symptom-analysis context
    - 📊 BMI / BMR / TDEE
    - 🌎 Country and region
    - 🥗 Diet preference
    - 🛡️ Allergy filtering
    - 🍱 Available regional foods
    - 🔢 Daily calorie target
    """
)


generate_button = st.button(
    "🍱 Generate Personalized Meal Plan",
    type="primary",
    use_container_width=True
)


if generate_button:

    if filtered_foods is None or filtered_foods.empty:

        st.error(
            "No suitable foods are available for the selected filters."
        )

    else:

        try:

            # ------------------------------------------------
            # CREATE MEAL PLANNER
            # ------------------------------------------------

            planner = MealPlanner(
                filtered_foods
            )

            # ------------------------------------------------
            # GENERATE CONDITION-AWARE PLAN
            # ------------------------------------------------

            plan = planner.generate_plan(
                target_calories=target_calories,
                condition=condition,
                meals=[
                    "Breakfast",
                    "Lunch",
                    "Snack",
                    "Dinner"
                ]
            )

            # ------------------------------------------------
            # CALCULATE TOTALS
            # ------------------------------------------------

            totals = planner.calculate_totals(
                plan
            )

            if plan.empty:

                st.warning(
                    "The system could not generate a meal plan "
                    "with the selected constraints."
                )

            else:

                # ------------------------------------------------
                # SAVE SESSION PROFILE
                # ------------------------------------------------

                st.session_state.name = (
                    st.session_state.get(
                        "name",
                        "User"
                    )
                )

                st.session_state.age = age
                st.session_state.gender = gender
                st.session_state.weight = weight
                st.session_state.height = height
                st.session_state.activity_level = (
                    activity_level
                )

                st.session_state.country = country
                st.session_state.region = state
                st.session_state.diet_preference = diet
                st.session_state.allergies = allergies

                # ------------------------------------------------
                # RESULT
                # ------------------------------------------------

                st.success(
                    "🎉 Personalized meal plan generated successfully!"
                )

                if condition:

                    st.info(
                        f"🧠 Nutrition context used: "
                        f"**{condition}**"
                    )

                else:

                    st.info(
                        "ℹ️ No symptom-analysis context was "
                        "available, so this is a general "
                        "personalized nutrition plan."
                    )

                # ------------------------------------------------
                # MEAL PLAN TABLE
                # ------------------------------------------------

                st.subheader(
                    "🍽️ Your Meal Plan"
                )

                st.dataframe(
                    plan,
                    use_container_width=True,
                    hide_index=True
                )

                # ------------------------------------------------
                # NUTRITION TOTALS
                # ------------------------------------------------

                st.subheader(
                    "📊 Daily Nutrition Summary"
                )

                col1, col2, col3, col4 = st.columns(4)

                with col1:

                    st.metric(
                        "Calories",
                        f"{totals['calories']:.0f} kcal"
                    )

                with col2:

                    st.metric(
                        "Protein",
                        f"{totals['protein']:.1f} g"
                    )

                with col3:

                    st.metric(
                        "Carbohydrates",
                        f"{totals['carbohydrates']:.1f} g"
                    )

                with col4:

                    st.metric(
                        "Fat",
                        f"{totals['fat']:.1f} g"
                    )

                # ------------------------------------------------
                # TARGET COMPARISON
                # ------------------------------------------------

                difference = (
                    totals["calories"]
                    - target_calories
                )

                st.subheader(
                    "🎯 Calorie Target Comparison"
                )

                if difference < 0:

                    st.info(
                        f"The generated plan is approximately "
                        f"{abs(difference):.0f} kcal below "
                        f"your selected target."
                    )

                elif difference > 0:

                    st.info(
                        f"The generated plan is approximately "
                        f"{difference:.0f} kcal above "
                        f"your selected target."
                    )

                else:

                    st.success(
                        "The generated plan is very close "
                        "to your selected calorie target."
                    )

                # ------------------------------------------------
                # CONDITION EXPLANATION
                # ------------------------------------------------

                if condition:

                    st.subheader(
                        "🧠 Why the Plan Was Adjusted"
                    )

                    st.write(
                        f"The meal planner used **{condition}** "
                        "as the current model-generated health "
                        "context when ranking available foods."
                    )

                    st.caption(
                        "The system does not claim that these foods "
                        "treat or cure the condition. The adjustment "
                        "is a general nutrition-ranking feature."
                    )

                # ------------------------------------------------
                # ALLERGY SAFETY
                # ------------------------------------------------

                st.subheader(
                    "🛡️ Allergy Safety"
                )

                if allergies.strip():

                    st.success(
                        "Allergy filtering was applied before "
                        "the meal plan was generated."
                    )

                    st.write(
                        f"Allergies checked: **{allergies}**"
                    )

                else:

                    st.info(
                        "No food allergies were entered."
                    )

                # ------------------------------------------------
                # SAVE TO DATABASE
                # ------------------------------------------------

                save_meal_plan(
                    user_name=st.session_state.get(
                        "name",
                        "User"
                    ),
                    country=country,
                    state=state,
                    diet_type=diet,
                    allergies=allergies,
                    target_calories=target_calories,
                    total_calories=totals[
                        "calories"
                    ],
                    total_protein=totals[
                        "protein"
                    ],
                    meal_plan=plan.to_json(
                        orient="records"
                    )
                )

                st.success(
                    "💾 Meal plan saved to Health History."
                )

        except Exception as error:

            st.error(
                "Unable to generate the personalized meal plan."
            )

            st.exception(error)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "SmartHealth AI • Personalized nutrition planning • "
    "Allergy-aware filtering • Regional food intelligence"
)