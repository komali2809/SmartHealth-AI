import streamlit as st


st.set_page_config(
    page_title="SmartHealth AI - Profile",
    page_icon="👤",
    layout="wide"
)


st.title("👤 User Profile")

st.caption(
    "Enter basic information used for personalization "
    "inside the application."
)


if "profile" not in st.session_state:

    st.session_state.profile = {
        "name": "",
        "age": 18,
        "gender": "Prefer not to say",
        "country": "India",
        "state": "Andhra Pradesh",
        "diet": "Vegetarian",
        "activity": "Moderate"
    }


profile = st.session_state.profile


with st.form("profile_form"):

    name = st.text_input(
        "Name",
        value=profile["name"]
    )

    age = st.number_input(
        "Age",
        min_value=1,
        max_value=120,
        value=int(profile["age"])
    )

    gender = st.selectbox(
        "Gender",
        [
            "Prefer not to say",
            "Female",
            "Male"
        ],
        index=[
            "Prefer not to say",
            "Female",
            "Male"
        ].index(profile["gender"])
    )

    country = st.text_input(
        "Country",
        value=profile["country"]
    )

    state = st.text_input(
        "State / Region",
        value=profile["state"]
    )

    diet = st.selectbox(
        "Diet Preference",
        [
            "Vegetarian",
            "Vegan",
            "Eggetarian",
            "Non-Vegetarian"
        ],
        index=[
            "Vegetarian",
            "Vegan",
            "Eggetarian",
            "Non-Vegetarian"
        ].index(profile["diet"])
    )

    activity = st.selectbox(
        "Activity Level",
        [
            "Sedentary",
            "Light",
            "Moderate",
            "Very Active",
            "Extra Active"
        ],
        index=[
            "Sedentary",
            "Light",
            "Moderate",
            "Very Active",
            "Extra Active"
        ].index(profile["activity"])
    )

    submitted = st.form_submit_button(
        "💾 Save Profile"
    )


if submitted:

    st.session_state.profile = {
        "name": name,
        "age": age,
        "gender": gender,
        "country": country,
        "state": state,
        "diet": diet,
        "activity": activity
    }

    st.success(
        "Profile information saved for this session."
    )


st.divider()

st.info(
    "For privacy, avoid entering highly sensitive personal "
    "or medical information. This profile is intended to "
    "support application personalization."
)