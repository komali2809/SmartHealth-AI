import streamlit as st
import pandas as pd

from modules.history import (
    symptom_history_dataframe
)


st.set_page_config(
    page_title="SmartHealth AI - Progress",
    page_icon="📈",
    layout="wide"
)


st.title("📈 Health Progress")

st.caption(
    "Review trends from your saved SmartHealth AI activity."
)


try:

    df = symptom_history_dataframe()

except Exception as error:

    st.error(
        f"Unable to load history: {error}"
    )

    st.stop()


if df.empty:

    st.info(
        "No symptom-analysis history has been saved yet."
    )

    st.write(
        "Go to **Symptom Analysis**, perform an analysis, "
        "and save the result to create progress history."
    )

    st.stop()


st.header("📊 Overview")


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Total Analyses",
        len(df)
    )


with col2:

    st.metric(
        "Unique Model Outputs",
        df["primary_prediction"].nunique()
    )


with col3:

    st.metric(
        "Latest Output",
        str(
            df.iloc[0]["primary_prediction"]
        )
    )


st.divider()


st.header("🧠 Model Output Pattern")


condition_counts = (
    df["primary_prediction"]
    .value_counts()
)


st.bar_chart(
    condition_counts
)


st.divider()


st.header("📋 Analysis History")


display_columns = [
    "created_at",
    "user_name",
    "age",
    "gender",
    "country",
    "state",
    "primary_prediction"
]


available_columns = [
    column
    for column in display_columns
    if column in df.columns
]


st.dataframe(
    df[available_columns],
    use_container_width=True,
    hide_index=True
)


st.warning(
    "Repeated model outputs are not confirmation of a "
    "medical diagnosis. This page only summarizes "
    "application history."
)