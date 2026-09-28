import streamlit as st

from modules.nutrition import (
    calculate_nutrition_profile
)


st.set_page_config(
    page_title="SmartHealth AI - Nutrition",
    page_icon="🥗",
    layout="wide"
)


st.title("🥗 Nutrition Intelligence")

st.caption(
    "Calculate basic nutritional estimates from your profile."
)


st.info(
    "BMI, BMR and TDEE values are estimates for wellness "
    "and educational purposes. They are not medical prescriptions."
)


st.header("👤 Your Information")


col1, col2 = st.columns(2)


with col1:

    age = st.number_input(
        "Age",
        min_value=1,
        max_value=120,
        value=20
    )

    weight = st.number_input(
        "Weight (kg)",
        min_value=1.0,
        max_value=500.0,
        value=60.0,
        step=0.5
    )

    height = st.number_input(
        "Height (cm)",
        min_value=30.0,
        max_value=250.0,
        value=165.0,
        step=0.5
    )


with col2:

    gender = st.selectbox(
        "Gender",
        [
            "Female",
            "Male",
            "Prefer not to say"
        ]
    )

    activity = st.selectbox(
        "Activity Level",
        [
            "Sedentary",
            "Light",
            "Moderate",
            "Very Active",
            "Extra Active"
        ]
    )


if st.button(
    "🔍 Calculate Nutrition Profile",
    use_container_width=True
):

    try:

        result = calculate_nutrition_profile(
            age=age,
            gender=gender,
            weight_kg=weight,
            height_cm=height,
            activity_level=activity
        )

        st.session_state.nutrition_profile = result


    except Exception as error:

        st.error(
            f"Calculation error: {error}"
        )


if "nutrition_profile" in st.session_state:

    result = st.session_state.nutrition_profile

    st.divider()

    st.header("📊 Your Results")


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "BMI",
            result["bmi"]
        )


    with col2:

        st.metric(
            "BMI Category",
            result["bmi_category"]
        )


    with col3:

        st.metric(
            "Estimated BMR",
            f'{result["bmr"]:.0f} kcal/day'
        )


    with col4:

        st.metric(
            "Estimated TDEE",
            f'{result["tdee"]:.0f} kcal/day'
        )


    st.divider()


    st.subheader("📖 What these values mean")


    st.write(
        """
        **BMI** is a height-to-weight screening measure.

        **BMR** is an estimate of the energy your body uses
        at rest.

        **TDEE** is an estimate that accounts for activity level.

        These calculations do not account for every individual
        health or nutritional factor.
        """
    )