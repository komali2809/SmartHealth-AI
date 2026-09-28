import pandas as pd

from modules.condition_nutrition import (
    ConditionNutritionEngine
)


class MealPlanner:

    def __init__(
        self,
        food_dataframe
    ):

        self.food_df = food_dataframe.copy()

        required_columns = [
            "food",
            "meal_type",
            "diet_type",
            "calories",
            "protein",
            "carbohydrates",
            "fat"
        ]

        missing = [
            column
            for column in required_columns
            if column not in self.food_df.columns
        ]

        if missing:

            raise ValueError(
                "Meal planner missing columns: "
                + ", ".join(missing)
            )

        for column in [
            "calories",
            "protein",
            "carbohydrates",
            "fat"
        ]:

            self.food_df[column] = pd.to_numeric(
                self.food_df[column],
                errors="coerce"
            )

        self.condition_engine = (
            ConditionNutritionEngine()
        )

    # --------------------------------------------------------
    # FOOD SELECTION
    # --------------------------------------------------------

    def _select_food(
        self,
        meal_type,
        remaining_calories=None,
        used_foods=None
    ):

        used_foods = used_foods or []

        candidates = self.food_df[
            self.food_df[
                "meal_type"
            ].astype(str).str.lower()
            == meal_type.lower()
        ].copy()

        candidates = candidates[
            ~candidates["food"].isin(
                used_foods
            )
        ]

        if candidates.empty:
            return None

        if remaining_calories is not None:

            within_limit = candidates[
                candidates["calories"]
                <= remaining_calories
            ]

            if not within_limit.empty:

                candidates = within_limit

        candidates = candidates.sort_values(
            by="protein",
            ascending=False
        )

        return candidates.iloc[0]

    # --------------------------------------------------------
    # CONDITION-AWARE PLAN
    # --------------------------------------------------------

    def generate_plan(
        self,
        target_calories,
        condition=None,
        meals=None
    ):

        if meals is None:

            meals = [
                "Breakfast",
                "Lunch",
                "Snack",
                "Dinner"
            ]

        target_calories = float(
            target_calories
        )

        if target_calories <= 0:

            raise ValueError(
                "Target calories must be greater than zero."
            )

        # ----------------------------------------------------
        # CONDITION FILTER
        # ----------------------------------------------------

        condition_foods = (
            self.condition_engine.filter_foods(
                self.food_df,
                condition
            )
        )

        if condition_foods.empty:

            condition_foods = self.food_df.copy()

        # ----------------------------------------------------
        # CONDITION RANKING
        # ----------------------------------------------------

        condition_foods = (
            self.condition_engine.rank_foods(
                condition_foods,
                condition
            )
        )

        original_df = self.food_df

        self.food_df = condition_foods

        plan = []

        used_foods = []

        remaining_calories = (
            target_calories
        )

        for meal_type in meals:

            item = self._select_food(
                meal_type=meal_type,
                remaining_calories=remaining_calories,
                used_foods=used_foods
            )

            if item is None:
                continue

            food_name = str(
                item["food"]
            )

            used_foods.append(
                food_name
            )

            calories = float(
                item["calories"]
            )

            protein = float(
                item["protein"]
            )

            carbohydrates = float(
                item["carbohydrates"]
            )

            fat = float(
                item["fat"]
            )

            plan.append(
                {
                    "meal": meal_type,
                    "food": food_name,
                    "calories": calories,
                    "protein": protein,
                    "carbohydrates": carbohydrates,
                    "fat": fat
                }
            )

            remaining_calories -= calories

        self.food_df = original_df

        return pd.DataFrame(plan)

    # --------------------------------------------------------
    # TOTALS
    # --------------------------------------------------------

    @staticmethod
    def calculate_totals(
        plan_df
    ):

        if plan_df.empty:

            return {
                "calories": 0,
                "protein": 0,
                "carbohydrates": 0,
                "fat": 0
            }

        return {

            "calories": round(
                plan_df["calories"].sum(),
                2
            ),

            "protein": round(
                plan_df["protein"].sum(),
                2
            ),

            "carbohydrates": round(
                plan_df["carbohydrates"].sum(),
                2
            ),

            "fat": round(
                plan_df["fat"].sum(),
                2
            )
        }