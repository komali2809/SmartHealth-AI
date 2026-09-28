import streamlit as st

from modules.history import (
    symptom_history_dataframe,
    meal_history_dataframe
)

st.set_page_config(
    page_title="SmartHealth AI - History",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Health History")

st.caption(
    "Review your previous symptom analyses and personalized meal plans."
)

# -------------------------
# Symptom History
# -------------------------

st.header("🧠 Symptom Analysis History")

symptom_df = symptom_history_dataframe()

if symptom_df.empty:

    st.info(
        "No symptom analysis history available yet."
    )

else:

    display_df = symptom_df[
        [
            "created_at",
            "user_name",
            "country",
            "state",
            "symptoms",
            "primary_prediction"
        ]
    ]

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )


st.divider()


# -------------------------
# Meal History
# -------------------------

st.header("🥗 Meal Plan History")

meal_df = meal_history_dataframe()

if meal_df.empty:

    st.info(
        "No meal plans have been saved yet."
    )

else:

    display_df = meal_df[
        [
            "created_at",
            "user_name",
            "country",
            "state",
            "diet_type",
            "allergies",
            "target_calories",
            "total_calories",
            "total_protein"
        ]
    ]

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )


st.divider()

st.info(
    "History is stored locally in SQLite. "
    "Avoid storing highly sensitive medical information "
    "when deploying the application publicly."
)