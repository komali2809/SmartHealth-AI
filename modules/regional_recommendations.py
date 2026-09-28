from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
REGIONAL_FOOD_PATH = BASE_DIR / "data" / "regional_foods.csv"


class RegionalFoodRecommender:

    def __init__(self):

        if not REGIONAL_FOOD_PATH.exists():
            raise FileNotFoundError(
                f"Regional food dataset not found: {REGIONAL_FOOD_PATH}"
            )

        self.food_df = pd.read_csv(
            REGIONAL_FOOD_PATH,
            encoding="utf-8"
        )

        self.food_df.columns = (
            self.food_df.columns
            .astype(str)
            .str.strip()
        )

        required_columns = [
            "country",
            "state",
            "region",
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

        missing_columns = [
            column
            for column in required_columns
            if column not in self.food_df.columns
        ]

        if missing_columns:
            raise ValueError(
                "Missing columns in regional_foods.csv: "
                + ", ".join(missing_columns)
            )

        numeric_columns = [
            "calories",
            "protein",
            "carbohydrates",
            "fat"
        ]

        for column in numeric_columns:
            self.food_df[column] = pd.to_numeric(
                self.food_df[column],
                errors="coerce"
            )

    @staticmethod
    def normalize_text(value):
        return str(value).strip().lower()

    def recommend(
        self,
        country,
        state,
        diet_type,
        allergies="",
        max_calories=None,
        min_protein=None
    ):

        df = self.food_df.copy()

        country_text = self.normalize_text(country)
        state_text = self.normalize_text(state)
        diet_text = self.normalize_text(diet_type)

        # -------------------------------------------------
        # COUNTRY FILTER
        # -------------------------------------------------

        matching = df[
            df["country"]
            .astype(str)
            .str.strip()
            .str.lower()
            == country_text
        ].copy()

        # -------------------------------------------------
        # STATE FILTER
        # -------------------------------------------------

        if not matching.empty:

            state_matches = matching[
                matching["state"]
                .astype(str)
                .str.strip()
                .str.lower()
                == state_text
            ].copy()

            if not state_matches.empty:
                matching = state_matches

        # -------------------------------------------------
        # DIET FILTER
        # -------------------------------------------------

        if diet_text == "vegan":

            matching = matching[
                matching["diet_type"]
                .astype(str)
                .str.strip()
                .str.lower()
                == "vegan"
            ]

        elif diet_text == "vegetarian":

            matching = matching[
                matching["diet_type"]
                .astype(str)
                .str.strip()
                .str.lower()
                .isin(["vegetarian", "vegan"])
            ]

        elif diet_text == "non-vegetarian":

            matching = matching[
                matching["diet_type"]
                .astype(str)
                .str.strip()
                .str.lower()
                .isin(["non-vegetarian", "vegetarian"])
            ]

        elif diet_text == "eggetarian":

            matching = matching[
                matching["diet_type"]
                .astype(str)
                .str.strip()
                .str.lower()
                .isin(["eggetarian", "vegetarian"])
            ]

        # -------------------------------------------------
        # ALLERGY FILTER
        # -------------------------------------------------

        allergy_list = [
            item.strip().lower()
            for item in str(allergies).split(",")
            if item.strip()
        ]

        if allergy_list:

            def is_safe(row):

                allergens = str(
                    row["common_allergens"]
                ).lower()

                if allergens == "none":
                    return True

                for allergy in allergy_list:

                    if allergy in allergens:
                        return False

                return True

            matching = matching[
                matching.apply(is_safe, axis=1)
            ]

        # -------------------------------------------------
        # CALORIE FILTER
        # -------------------------------------------------

        if max_calories is not None:

            matching = matching[
                matching["calories"] <= float(max_calories)
            ]

        # -------------------------------------------------
        # PROTEIN FILTER
        # -------------------------------------------------

        if min_protein is not None:

            matching = matching[
                matching["protein"] >= float(min_protein)
            ]

        # -------------------------------------------------
        # SORT
        # -------------------------------------------------

        if not matching.empty:

            matching = matching.sort_values(
                by=["protein", "calories"],
                ascending=[False, True]
            )

        return matching.reset_index(drop=True)