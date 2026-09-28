import pandas as pd


class AllergySafetyEngine:

    def __init__(self):
        self.allergen_aliases = {
            "peanut": [
                "peanut",
                "groundnut",
                "peanuts"
            ],

            "milk": [
                "milk",
                "dairy",
                "casein",
                "whey"
            ],

            "egg": [
                "egg",
                "eggs"
            ],

            "fish": [
                "fish",
                "tuna",
                "salmon",
                "prawn",
                "prawns"
            ],

            "shellfish": [
                "shellfish",
                "shrimp",
                "prawn",
                "prawns",
                "crab",
                "lobster"
            ],

            "gluten": [
                "gluten",
                "wheat",
                "barley",
                "rye"
            ],

            "soy": [
                "soy",
                "soya"
            ],

            "tree nuts": [
                "almond",
                "cashew",
                "walnut",
                "pistachio",
                "hazelnut",
                "tree nuts"
            ],

            "coconut": [
                "coconut"
            ]
        }

    def normalize_allergies(self, allergies):

        if allergies is None:
            return []

        if isinstance(allergies, str):

            allergies = allergies.split(",")

        normalized = []

        for allergy in allergies:

            allergy = str(
                allergy
            ).strip().lower()

            if allergy:
                normalized.append(
                    allergy
                )

        return list(
            dict.fromkeys(normalized)
        )

    def get_keywords(self, allergy):

        allergy = str(
            allergy
        ).strip().lower()

        return self.allergen_aliases.get(
            allergy,
            [allergy]
        )

    def contains_allergen(
        self,
        allergen_text,
        allergies
    ):

        if pd.isna(allergen_text):
            return False

        text = str(
            allergen_text
        ).lower()

        for allergy in allergies:

            keywords = self.get_keywords(
                allergy
            )

            for keyword in keywords:

                if keyword in text:
                    return True

        return False

    def filter_safe_foods(
        self,
        food_df,
        allergies
    ):

        allergies = self.normalize_allergies(
            allergies
        )

        if not allergies:
            return food_df.copy()

        safe_df = food_df[
            ~food_df["common_allergens"].apply(
                lambda value:
                    self.contains_allergen(
                        value,
                        allergies
                    )
            )
        ].copy()

        return safe_df.reset_index(
            drop=True
        )

    def get_unsafe_foods(
        self,
        food_df,
        allergies
    ):

        allergies = self.normalize_allergies(
            allergies
        )

        if not allergies:
            return pd.DataFrame(
                columns=food_df.columns
            )

        unsafe_df = food_df[
            food_df["common_allergens"].apply(
                lambda value:
                    self.contains_allergen(
                        value,
                        allergies
                    )
            )
        ].copy()

        return unsafe_df.reset_index(
            drop=True
        )

    def safety_summary(
        self,
        food_df,
        allergies
    ):

        allergies = self.normalize_allergies(
            allergies
        )

        unsafe_df = self.get_unsafe_foods(
            food_df,
            allergies
        )

        safe_df = self.filter_safe_foods(
            food_df,
            allergies
        )

        return {
            "allergies_checked": allergies,
            "total_foods": len(food_df),
            "safe_foods": len(safe_df),
            "unsafe_foods": len(unsafe_df),
            "safety_status":
                "No allergies specified"
                if not allergies
                else "Allergy filtering applied"
        }