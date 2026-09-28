def calculate_bmi(weight_kg, height_cm):

    if weight_kg <= 0:
        raise ValueError("Weight must be greater than zero.")

    if height_cm <= 0:
        raise ValueError("Height must be greater than zero.")

    height_m = height_cm / 100

    return weight_kg / (height_m ** 2)


def bmi_category(bmi):

    if bmi < 18.5:
        return "Underweight"

    elif bmi < 25:
        return "Normal range"

    elif bmi < 30:
        return "Overweight"

    else:
        return "Obesity range"


def calculate_bmr(
    age,
    gender,
    weight_kg,
    height_cm
):

    if age <= 0:
        raise ValueError(
            "Age must be greater than zero."
        )

    if weight_kg <= 0:
        raise ValueError(
            "Weight must be greater than zero."
        )

    if height_cm <= 0:
        raise ValueError(
            "Height must be greater than zero."
        )

    gender = gender.lower().strip()

    if gender == "male":

        return (
            10 * weight_kg
            + 6.25 * height_cm
            - 5 * age
            + 5
        )

    elif gender == "female":

        return (
            10 * weight_kg
            + 6.25 * height_cm
            - 5 * age
            - 161
        )

    else:

        male = (
            10 * weight_kg
            + 6.25 * height_cm
            - 5 * age
            + 5
        )

        female = (
            10 * weight_kg
            + 6.25 * height_cm
            - 5 * age
            - 161
        )

        return (male + female) / 2


def calculate_tdee(
    bmr,
    activity_level
):

    activity_factors = {

        "sedentary": 1.20,

        "light": 1.375,

        "moderate": 1.55,

        "very_active": 1.725,

        "extra_active": 1.90
    }

    activity = (
        activity_level
        .lower()
        .strip()
    )

    factor = activity_factors.get(
        activity,
        1.20
    )

    return bmr * factor


def calculate_nutrition_profile(
    age,
    gender,
    weight_kg,
    height_cm,
    activity_level
):

    bmi = calculate_bmi(
        weight_kg,
        height_cm
    )

    bmr = calculate_bmr(
        age,
        gender,
        weight_kg,
        height_cm
    )

    tdee = calculate_tdee(
        bmr,
        activity_level
    )

    return {

        "bmi": round(
            bmi,
            2
        ),

        "bmi_category":
            bmi_category(bmi),

        "bmr": round(
            bmr,
            2
        ),

        "tdee": round(
            tdee,
            2
        )
    }