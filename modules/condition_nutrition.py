class ConditionNutritionEngine:

    def __init__(self):

        self.rules = {

            "Diabetes": {
                "prioritize": [
                    "high protein",
                    "fiber",
                    "low added sugar"
                ],
                "avoid_keywords": [
                    "sugar",
                    "sweet",
                    "dessert"
                ]
            },

            "Obesity": {
                "prioritize": [
                    "high protein",
                    "lower calorie",
                    "fiber"
                ],
                "avoid_keywords": [
                    "fried",
                    "sugary"
                ]
            },

            "Hypertension": {
                "prioritize": [
                    "lower sodium",
                    "vegetables",
                    "fiber"
                ],
                "avoid_keywords": [
                    "high sodium",
                    "very salty"
                ]
            },

            "Anemia": {
                "prioritize": [
                    "iron-rich foods",
                    "protein",
                    "vitamin C"
                ],
                "avoid_keywords": []
            },

            "Constipation": {
                "prioritize": [
                    "fiber",
                    "hydration",
                    "fruit"
                ],
                "avoid_keywords": []
            },

            "Gastritis": {
                "prioritize": [
                    "mild foods",
                    "lower fat"
                ],
                "avoid_keywords": [
                    "very spicy",
                    "fried"
                ]
            },

            "Heart Disease": {
                "prioritize": [
                    "fiber",
                    "lower saturated fat",
                    "vegetables"
                ],
                "avoid_keywords": [
                    "fried",
                    "high saturated fat"
                ]
            }
        }

    def get_rule(self, condition):

        if not condition:
            return {
                "prioritize": [],
                "avoid_keywords": []
            }

        condition = str(
            condition
        ).strip()

        return self.rules.get(
            condition,
            {
                "prioritize": [],
                "avoid_keywords": []
            }
        )

    def filter_foods(
        self,
        food_df,
        condition
    ):

        if food_df.empty:
            return food_df.copy()

        rule = self.get_rule(
            condition
        )

        result = food_df.copy()

        if "food" not in result.columns:
            return result

        avoid_keywords = rule[
            "avoid_keywords"
        ]

        if avoid_keywords:

            def is_safe(food):

                food_text = str(
                    food
                ).lower()

                return not any(
                    keyword.lower()
                    in food_text
                    for keyword
                    in avoid_keywords
                )

            result = result[
                result["food"].apply(
                    is_safe
                )
            ]

        return result.reset_index(
            drop=True
        )

    def rank_foods(
        self,
        food_df,
        condition
    ):

        if food_df.empty:
            return food_df.copy()

        rule = self.get_rule(
            condition
        )

        prioritize = [
            item.lower()
            for item
            in rule["prioritize"]
        ]

        result = food_df.copy()

        def calculate_score(row):

            score = 0

            food_text = str(
                row.get(
                    "food",
                    ""
                )
            ).lower()

            # -----------------------------
            # Protein
            # -----------------------------

            try:

                protein = float(
                    row.get(
                        "protein",
                        0
                    )
                )

                if (
                    "high protein"
                    in prioritize
                ):

                    score += (
                        protein * 0.5
                    )

            except (
                ValueError,
                TypeError
            ):

                pass

            # -----------------------------
            # Fiber / vegetables / fruit
            # -----------------------------

            if any(
                word in food_text
                for word in [
                    "vegetable",
                    "fruit",
                    "dal",
                    "lentil",
                    "bean",
                    "oat"
                ]
            ):

                if "fiber" in prioritize:
                    score += 5

                if (
                    "vegetables"
                    in prioritize
                ):
                    score += 5

                if "fruit" in prioritize:
                    score += 5

            # -----------------------------
            # Iron-rich foods
            # -----------------------------

            if (
                "iron-rich foods"
                in prioritize
            ):

                if any(
                    word in food_text
                    for word in [
                        "spinach",
                        "leafy",
                        "lentil",
                        "bean",
                        "chickpea",
                        "millet"
                    ]
                ):

                    score += 8

            # -----------------------------
            # Lower calorie
            # -----------------------------

            try:

                calories = float(
                    row.get(
                        "calories",
                        0
                    )
                )

                if (
                    "lower calorie"
                    in prioritize
                ):

                    score += max(
                        0,
                        500 - calories
                    ) / 50

            except (
                ValueError,
                TypeError
            ):

                pass

            return score

        result[
            "_condition_score"
        ] = result.apply(
            calculate_score,
            axis=1
        )

        result = result.sort_values(
            "_condition_score",
            ascending=False
        )

        return result.drop(
            columns=[
                "_condition_score"
            ]
        ).reset_index(
            drop=True
        )