import pandas as pd

from database.database import (
    get_symptom_history,
    get_meal_history
)


def symptom_history_dataframe():

    rows = get_symptom_history()

    columns = [
        "id",
        "user_name",
        "age",
        "gender",
        "country",
        "state",
        "symptoms",
        "primary_prediction",
        "created_at"
    ]

    return pd.DataFrame(
        rows,
        columns=columns
    )


def meal_history_dataframe():

    rows = get_meal_history()

    columns = [
        "id",
        "user_name",
        "country",
        "state",
        "diet_type",
        "allergies",
        "target_calories",
        "total_calories",
        "total_protein",
        "meal_plan",
        "created_at"
    ]

    return pd.DataFrame(
        rows,
        columns=columns
    )